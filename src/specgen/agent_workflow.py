from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator, exceptions as jsonschema_exceptions

from .canonical import snapshot_digest
from .contract_bundle import require as bundle_requirement
from .contract_bundle import validate as bundle_validate
from .elicitation import assess
from .evals import evaluation_intent
from .validate import validate

AW_VERSION = "0.9.1"
AW_STANDARD_REQUIRES = (
    "completion_report",
    "durable_agent_run",
    "independent_phase_gate",
    "isolated_worktree",
    "persistent_log",
    "source_baseline",
)
AW_SCORERS = frozenset(
    {
        "acceptance_commands",
        "completion_presence",
        "evidence_fidelity",
        "oracle_leak",
        "patch_applicability",
        "regression_guard",
        "repository_cleanliness",
        "schema_validity",
        "static_quality_delta",
        "writable_scope",
    }
)
_ALLOWED_EVALUATION_METADATA = frozenset(
    {"command", "oracle", "oracle_ref", "scorer", "timeout_seconds"}
)


def _schema(name: str) -> dict[str, Any]:
    schema_id = {
        "pack.schema.json": "agent-workflow/prompt-pack/v2",
        "evaluation-plan.schema.json": "agent-workflow/evaluation-plan/v1",
        "source-baseline.schema.json": "agent-workflow/source-baseline/v1",
        "agent-role-v1.schema.json": "agent-workflow/agent-role/v1",
        "task-result.schema.json": "agent-workflow/task-result/v1",
    }.get(name)
    if schema_id is None:
        raise ValueError(f"unsupported Agent-Workflow schema: {name}")
    from specgen_contracts.bundle import schema

    return schema(schema_id)


def _check(schema_name: str, value: dict[str, Any]) -> None:
    schema_id = {
        "pack.schema.json": "agent-workflow/prompt-pack/v2",
        "evaluation-plan.schema.json": "agent-workflow/evaluation-plan/v1",
        "source-baseline.schema.json": "agent-workflow/source-baseline/v1",
        "agent-role-v1.schema.json": "agent-workflow/agent-role/v1",
        "task-result.schema.json": "agent-workflow/task-result/v1",
    }[schema_name]
    errors = bundle_validate(schema_id, value)
    if errors:
        raise ValueError(
            f"generated Agent-Workflow artifact violates {schema_name}: {errors[0]['message']}"
        )


def _run_id(spec_id: str, task_id: str) -> str:
    return "specgen-" + hashlib.sha256(f"{spec_id}:{task_id}".encode()).hexdigest()[:16]


def _resource_token(value: str) -> str:
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip(".-") or "item"
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:8]
    return f"{stem}-{digest}"


def _active(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [item for item in items if item.get("lifecycle", "active") != "retired"]


def _require_agent_workflow_ready(document: dict[str, Any]) -> None:
    plan = assess(document, "agent-workflow")
    if plan["ready"]:
        return
    blockers = [item["id"] for item in plan["questions"] if item["severity"] == "blocker"]
    suffix = f": {', '.join(blockers)}" if blockers else ""
    raise ValueError(f"Agent-Workflow compilation requires an agent-workflow-ready specification{suffix}")


def _safe_top_level_directory(value: str) -> str:
    path = PurePosixPath(value)
    if (
        not value
        or path.is_absolute()
        or len(path.parts) != 1
        or any(part in {"", ".", ".."} for part in path.parts)
        or path.as_posix() != value
    ):
        raise ValueError(f"Agent-Workflow phase directory must be a safe top-level POSIX path: {value}")
    return value


def _phase_directory(phase: dict[str, Any], index: int) -> str:
    explicit = phase.get("directory")
    if explicit is not None:
        if not isinstance(explicit, str):
            raise ValueError(f"phase {phase['id']} directory must be a string")
        return _safe_top_level_directory(explicit)
    return f"phase-{index:02d}-{_resource_token(str(phase['id']))}"


def _requirement_maps(document: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    requirements = {item["id"]: item for item in _active(document.get("requirements", []))}
    acceptance = {item["id"]: item for item in _active(document.get("acceptance_criteria", []))}
    return requirements, acceptance


def _evaluation_requirement_ids(item: dict[str, Any], acceptance: dict[str, dict[str, Any]]) -> set[str]:
    requirement_ids = set(item.get("requirement_ids", []))
    for acceptance_id in item.get("acceptance_ids", []):
        criterion = acceptance.get(acceptance_id)
        if criterion:
            requirement_ids.update(criterion.get("requirement_ids", []))
    return requirement_ids


def _target_tasks_for_evaluation(
    item: dict[str, Any],
    tasks: dict[str, dict[str, Any]],
    acceptance: dict[str, dict[str, Any]],
) -> list[str]:
    requirement_ids = _evaluation_requirement_ids(item, acceptance)
    return sorted(
        task_id
        for task_id, task in tasks.items()
        if requirement_ids.intersection(task.get("requirement_ids", []))
    )


def _result_contract_resource(task: dict[str, Any]) -> tuple[dict[str, Any], dict[str, str]]:
    contract = task.get("result_contract")
    if not isinstance(contract, dict):
        raise ValueError(f"Agent-Workflow task {task['id']} is missing a structured result contract")
    unsupported = sorted(set(contract) - {"schema", "required"})
    if unsupported:
        raise ValueError(
            f"Agent-Workflow result contract for {task['id']} contains unsupported fields: "
            + ", ".join(unsupported)
        )
    schema = contract.get("schema")
    if isinstance(schema, str):
        if schema != "agent-workflow/task-result/v1":
            raise ValueError(
                f"Agent-Workflow result contract for {task['id']} references unsupported schema {schema!r}; "
                "the target requires packaged schema bytes"
            )
        schema_value = _schema("task-result.schema.json")
        path = "result-contracts/agent-workflow-task-result-v1.schema.json"
    elif isinstance(schema, dict):
        schema_value = schema
        path = f"result-contracts/{_resource_token(task['id'])}.schema.json"
    else:
        raise ValueError(
            f"Agent-Workflow result contract for {task['id']} must contain a schema object or "
            "the agent-workflow/task-result/v1 schema ID"
        )
    try:
        Draft202012Validator.check_schema(schema_value)
    except jsonschema_exceptions.SchemaError as exc:
        raise ValueError(f"invalid result JSON Schema for task {task['id']}: {exc.message}") from exc
    pending = [schema_value]
    while pending:
        current = pending.pop()
        if isinstance(current, dict):
            for key, value in current.items():
                if key in {"$ref", "$dynamicRef"} and isinstance(value, str) and not value.startswith("#"):
                    raise ValueError(
                        f"result JSON Schema for task {task['id']} contains external reference {value!r}; "
                        "package-local multi-schema result contracts are not yet representable"
                    )
                pending.append(value)
        elif isinstance(current, list):
            pending.extend(current)
    resource = json.dumps(schema_value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    return {"schema": path, "required": bool(contract.get("required", True))}, {path: resource}


def _source_evidence_lines(document: dict[str, Any], repository_analysis: dict[str, Any] | None) -> list[str]:
    if repository_analysis is None:
        return []
    evidence_by_path = {
        item["path"]: item
        for item in repository_analysis.get("evidence", [])
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    }
    lines: list[str] = []
    for source in document.get("provenance", {}).get("sources", []):
        if source.get("kind") != "repository":
            continue
        locator = source.get("locator")
        if not isinstance(locator, str):
            continue
        normalized = locator.replace("\\", "/").lstrip("./")
        evidence = evidence_by_path.get(normalized)
        if evidence:
            lines.append(f"- {evidence['id']}: `{normalized}` ({evidence['digest']})")
    return sorted(set(lines))


def _task_prompt(
    document: dict[str, Any],
    task: dict[str, Any],
    result_contract_path: str,
    repository_analysis: dict[str, Any] | None,
) -> str:
    requirements, acceptance = _requirement_maps(document)
    requirement_ids = list(task.get("requirement_ids", []))
    criteria = [
        item
        for item in acceptance.values()
        if set(item.get("requirement_ids", [])).intersection(requirement_ids)
    ]
    evaluations = [
        item
        for item in _active(document.get("evaluations", []))
        if set(item.get("requirement_ids", [])).intersection(requirement_ids)
        or set(item.get("acceptance_ids", [])).intersection(item_["id"] for item_ in criteria)
    ]
    lines = [
        f"# {task.get('title', task['id'])}",
        "",
        f"- Task ID: `{task['id']}`",
        f"- Tier: `{task.get('tier', 'implementation')}`",
    ]
    lines.append(
        f"- Target application: `{document['target_application_id']}`"
        if document.get("target_application_id")
        else "- Target application: not declared (new or not-yet-existing application)"
    )
    role = task.get("role") or task.get("role_hint")
    if isinstance(role, str) and role:
        lines.append(f"- Logical role hint: `{role}`")
    dependencies = list(task.get("dependencies", []))
    lines.append(f"- Dependencies: {', '.join(f'`{item}`' for item in dependencies) if dependencies else 'none'}")
    lines.extend(["", "## Authorized requirements"])
    for requirement_id in requirement_ids:
        requirement = requirements.get(requirement_id)
        if requirement:
            lines.append(f"- `{requirement_id}` — {requirement['statement']}")
    lines.extend(["", "## Acceptance"])
    if criteria:
        for criterion in criteria:
            lines.append(f"- `{criterion['id']}` — {criterion['criterion']}")
    else:
        lines.append("- No task-specific acceptance criterion was found; do not invent one.")
    lines.extend(["", "## Evaluation / test intent"])
    if evaluations:
        for evaluation in evaluations:
            oracle = evaluation.get("oracle") or evaluation.get("metadata", {}).get("oracle", "public")
            lines.append(f"- `{evaluation['id']}` — kind `{evaluation['kind']}`, oracle `{oracle}`")
            if oracle in {"hidden", "external"}:
                lines.append("  - Treat the oracle as opaque; do not seek or reconstruct hidden oracle contents.")
    else:
        lines.append("- No task-specific evaluation is available; stop rather than fabricating verification intent.")
    expected = task.get("expected_outputs", task.get("outputs"))
    lines.extend(["", "## Expected outputs"])
    if expected is None:
        lines.append("- Produce only the implementation outputs authorized by the requirements and acceptance criteria above.")
    else:
        lines.append("```json")
        lines.append(json.dumps(expected, indent=2, sort_keys=True, ensure_ascii=False))
        lines.append("```")
    lines.extend(
        [
            "",
            "## Structured result",
            f"Write the task result using `{result_contract_path}`; Agent-Workflow owns collection and validation of `result.json`.",
        ]
    )
    if repository_analysis is not None:
        baseline = repository_analysis["baseline"]
        lines.extend(
            [
                "",
                "## Source context",
                f"- Repository baseline: `{baseline['revision']}` ({baseline['kind']}; dirty={str(baseline['dirty']).lower()})",
            ]
        )
        lines.extend(_source_evidence_lines(document, repository_analysis) or ["- No explicitly referenced repository evidence paths were attached to this task context."])
    lines.extend(
        [
            "",
            "## Execution guardrails",
            "- Writable scope: modify only repository paths necessary to satisfy the authorized requirements; Agent-Workflow owns worktree and writable-scope enforcement.",
            "- Acceptance: report against the linked criteria and do not broaden scope to make acceptance easier.",
            "- Test behavior: follow the repository/specification testing policy and the evaluation intent above; do not add tests merely to increase test count.",
            "- Stop conditions: stop and report blocked if required source evidence, permissions, dependencies, or specification decisions are missing or contradictory.",
            "",
        ]
    )
    return "\n".join(lines)


def _phase_resources(
    phase: dict[str, Any], directory: str, task_ids: list[str], tasks: dict[str, dict[str, Any]]
) -> dict[str, str]:
    summary = phase.get("description") or phase.get("name") or f"Phase {phase['id']}"
    readme = [f"# {phase.get('name') or phase['id']}", "", str(summary), "", "## Tasks"]
    master = [f"# Phase {phase['id']} implementation prompt", "", str(summary), "", "Execute only the declared tasks and dependencies in `pack.yaml`.", "", "## Task order / dependencies"]
    for task_id in task_ids:
        task = tasks[task_id]
        deps = task.get("dependencies", [])
        readme.append(f"- `{task_id}` — {task.get('title', task_id)}")
        master.append(f"- `{task_id}` depends on {', '.join(f'`{item}`' for item in deps) if deps else 'nothing'}.")
    readme.append("")
    master.extend(["", "Agent-Workflow owns execution, worktrees, review, completion, and acceptance state.", ""])
    return {
        f"{directory}/README.md": "\n".join(readme),
        f"{directory}/MASTER_IMPLEMENTATION_PROMPT.md": "\n".join(master),
    }


def _root_pack_resources(document: dict[str, Any], has_source_baseline: bool) -> dict[str, str]:
    digest = snapshot_digest(document)
    baseline_note = "`source-baseline.json` is present and bound to the analyzed Git revision." if has_source_baseline else "No source baseline is emitted because no repository analysis was supplied."
    return {
        "README.md": (
            f"# {document['title']} — Agent-Workflow target\n\n"
            f"Generated from SpecGen `{document['id']}` snapshot `{document['snapshot']['id']}` ({digest}).\n\n"
            + (f"Target application: `{document['target_application_id']}`.\n\n"
               if document.get("target_application_id")
               else "Target application: not declared (new or not-yet-existing application semantics).\n\n")
            +
            "`pack.yaml` is the Agent-Workflow execution manifest. The canonical SpecGen snapshot remains the specification authority.\n\n"
            f"{baseline_note}\n"
        ),
        "EXECUTION_PROTOCOL.md": (
            "# Execution protocol\n\n"
            "Agent-Workflow owns execution state, worktrees, completion collection, review, and acceptance.\n\n"
            "1. Validate the prompt pack with the Agent-Workflow 0.9.1 public pack interface.\n"
            "2. Honor task dependencies and task-local writable/acceptance/test/stop guardrails.\n"
            "3. Treat result-contract schemas as required structured handoff contracts.\n"
            "4. Treat hidden/external oracle material as opaque and use only the digest-bound target reference.\n"
            "5. Never edit generated target artifacts to redefine canonical SpecGen requirements.\n"
        ),
        "DELEGATION_RUNBOOK.md": (
            "# Delegation runbook\n\n"
            "Use Agent-Workflow's public prompt-pack and delegation surfaces. SpecGen does not launch workers or own lifecycle state.\n\n"
            "Before delegation, verify the pack, source baseline when present, dependencies, result schemas, and evaluation plan.\n"
            "If a generated target cannot represent the canonical specification faithfully, return to SpecGen rather than patching execution artifacts by hand.\n"
        ),
        "templates/TICKET_COMPLETION.md": (
            "# Ticket completion\n\n"
            "Report the implementation summary, changed outputs, acceptance evidence, unresolved blockers, and the structured `result.json` required by the task result contract.\n"
        ),
        "templates/PHASE_GATE_REPORT.md": (
            "# Phase gate report\n\n"
            "Summarize completed tasks, acceptance/evaluation evidence, unresolved blockers, and whether the next declared phase is eligible to proceed. Agent-Workflow remains the gate authority.\n"
        ),
        "templates/source-baseline.example.json": json.dumps(
            {
                "schema": "agent-workflow/source-baseline/v1",
                "generated_at": "<canonical-snapshot-created-at>",
                "components": {
                    "primary": {
                        "path": ".",
                        "head": "<git-head>",
                        "branch": "<git-branch>",
                        "dirty": False,
                    }
                },
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
    }


def compile_prompt_pack(
    document: dict[str, Any], repository_analysis: dict[str, Any] | None = None
) -> tuple[dict[str, Any], dict[str, str]]:
    _require_agent_workflow_ready(document)
    tasks = {
        task["id"]: task
        for task in _active(document.get("implementation", {}).get("tasks", []))
    }
    active_phases = _active(document.get("implementation", {}).get("phases", []))
    phases: list[dict[str, Any]] = []
    resources: dict[str, str] = {}
    assigned: set[str] = set()

    for index, phase in enumerate(active_phases, 1):
        ids = phase.get("task_ids") or phase.get("tasks") or []
        if not ids and len(active_phases) == 1:
            ids = list(tasks)
        if not isinstance(ids, list):
            raise ValueError(f"phase {phase['id']} task assignment must be an array")
        phase_task_ids: list[str] = []
        phase_tasks: list[dict[str, Any]] = []
        directory = _phase_directory(phase, index)
        for raw_task_id in ids:
            task_id = str(raw_task_id)
            if task_id not in tasks:
                raise ValueError(f"Agent-Workflow phase {phase['id']} references unknown or retired task {task_id}")
            if task_id in assigned:
                raise ValueError(f"Agent-Workflow task {task_id} is assigned to more than one phase")
            task = tasks[task_id]
            missing_dependencies = sorted(set(task.get("dependencies", [])) - tasks.keys())
            if missing_dependencies:
                raise ValueError(
                    f"Agent-Workflow task {task_id} depends on non-active target tasks: "
                    + ", ".join(missing_dependencies)
                )
            assigned.add(task_id)
            phase_task_ids.append(task_id)
            result_contract, contract_resources = _result_contract_resource(task)
            for path, content in contract_resources.items():
                existing = resources.get(path)
                if existing is not None and existing != content:
                    raise ValueError(f"conflicting generated result-contract resource: {path}")
                resources[path] = content
            prompt_path = f"{directory}/tickets/{_resource_token(task_id)}.md"
            resources[prompt_path] = _task_prompt(
                document, task, result_contract["schema"], repository_analysis
            )
            entry: dict[str, Any] = {
                "id": task_id,
                "tier": str(task.get("tier", "implementation")),
                "agent_run_id": _run_id(document["id"], task_id),
                "prompt": prompt_path,
                "dependencies": list(task.get("dependencies", [])),
                "result_contract": result_contract,
            }
            for key in ("task_type", "backlog_id"):
                value = task.get(key)
                if value is not None:
                    entry[key] = value
            phase_tasks.append(entry)
        if not phase_tasks:
            raise ValueError(f"Agent-Workflow phase {phase['id']} has no active tasks")
        phase_entry: dict[str, Any] = {
            "id": phase["id"],
            "name": phase.get("name") or phase.get("description") or f"Phase {index}",
            "directory": directory,
            "tasks": phase_tasks,
        }
        explicit_order = phase.get("mandatory_order")
        if explicit_order is not None:
            if not isinstance(explicit_order, list):
                raise ValueError(f"phase {phase['id']} mandatory_order must be an array")
            unknown = sorted(set(str(item) for item in explicit_order) - set(phase_task_ids))
            if unknown:
                raise ValueError(
                    f"phase {phase['id']} mandatory_order references tasks outside the phase: "
                    + ", ".join(unknown)
                )
            phase_entry["mandatory_order"] = [str(item) for item in explicit_order]
        resources.update(_phase_resources(phase, directory, phase_task_ids, tasks))
        phases.append(phase_entry)

    unassigned = sorted(set(tasks) - assigned)
    if unassigned:
        raise ValueError(
            "Agent-Workflow compile requires every active task assigned to exactly one phase: "
            + ", ".join(unassigned)
        )
    pack: dict[str, Any] = {
        "schema": "agent-workflow/prompt-pack/v2",
        "pack_id": document["id"],
        "workflow": {
            "name": "agent-workflow",
            "minimum_version": AW_VERSION,
            "requires": [
                *AW_STANDARD_REQUIRES,
                f"contract-bundle=={bundle_requirement('agent-workflow/prompt-pack/v2')[0]}",
                *(
                    f"contract-schema-digest:{schema_id}={bundle_requirement(schema_id)[1]}"
                    for schema_id in (
                        "agent-workflow/prompt-pack/v2",
                        "agent-workflow/evaluation-plan/v1",
                        "agent-workflow/source-baseline/v1",
                        "agent-workflow/agent-role/v1",
                        "agent-workflow/task-result/v1",
                    )
                ),
            ],
        },
        "phases": phases,
        "bundle_provenance": {
            "bundle_version": bundle_requirement("agent-workflow/prompt-pack/v2")[0],
            "schema_id": "agent-workflow/prompt-pack/v2",
            "schema_digest": bundle_requirement("agent-workflow/prompt-pack/v2")[1],
        },
    }
    _check("pack.schema.json", pack)
    return pack, resources


def _git(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ValueError(f"cannot verify repository Git state at {root}: {' '.join(args)}") from exc
    return result.stdout.strip()


def compile_source_baseline(
    document: dict[str, Any],
    repository_analysis: dict[str, Any],
    repository_root: str | Path | None = None,
) -> dict[str, Any]:
    result = validate(repository_analysis)
    if not result.valid or repository_analysis.get("schema") != "specgen/repository-analysis/v1alpha1":
        raise ValueError("Agent-Workflow source baseline requires a valid repository-analysis/v1alpha1 artifact")
    blockers = [
        item["id"]
        for item in repository_analysis.get("contradictions", [])
        if item.get("severity") == "blocker"
    ]
    if blockers:
        raise ValueError(
            "Agent-Workflow source baseline cannot compile from repository analysis with blockers: "
            + ", ".join(blockers)
        )
    binding = repository_analysis.get("spec")
    expected_binding = {
        "id": document["id"],
        "snapshot_id": document["snapshot"]["id"],
        "digest": snapshot_digest(document),
    }
    if binding != expected_binding:
        raise ValueError("repository analysis is not bound to the exact canonical snapshot being compiled")
    baseline = repository_analysis["baseline"]
    if baseline.get("kind") != "git":
        raise ValueError(
            "Agent-Workflow source-baseline/v1 requires Git head/branch semantics; "
            "a SpecGen directory-digest baseline cannot be lowered faithfully"
        )
    root_value = repository_root or repository_analysis.get("repository", {}).get("path")
    if not isinstance(root_value, (str, Path)):
        raise ValueError("repository root is required to verify Agent-Workflow source baseline state")
    root = Path(root_value).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"repository root is not a directory: {root}")
    head = _git(root, "rev-parse", "HEAD")
    branch = _git(root, "rev-parse", "--abbrev-ref", "HEAD")
    dirty = bool(_git(root, "status", "--porcelain"))
    if head != baseline["revision"] or dirty != bool(baseline["dirty"]):
        raise ValueError("repository state drifted since SpecGen analysis; regenerate repository analysis before compiling")
    for evidence in repository_analysis.get("evidence", []):
        relative = evidence.get("path")
        digest = evidence.get("digest")
        if not isinstance(relative, str) or not isinstance(digest, str):
            continue
        source = root / relative
        if not source.is_file():
            raise ValueError(f"repository evidence disappeared since analysis: {relative}")
        actual = "sha256:" + hashlib.sha256(source.read_bytes()).hexdigest()
        if actual != digest:
            raise ValueError(
                f"repository evidence drifted since analysis: {relative}; regenerate repository analysis before compiling"
            )
    target_context = repository_analysis.get("target_context")
    if isinstance(target_context, dict):
        expected = target_context.get("expected_version")
        if expected is not None and expected != AW_VERSION:
            raise ValueError(
                f"repository analysis targets Agent-Workflow {expected}, but this SpecGen release compiles {AW_VERSION}"
            )
        if target_context.get("version_matches") is False:
            raise ValueError("repository analysis reports Agent-Workflow development-source version drift")
    value = {
        "schema": "agent-workflow/source-baseline/v1",
        "generated_at": document["snapshot"]["created_at"],
        "components": {
            "primary": {
                "path": ".",
                "head": head,
                "branch": branch,
                "dirty": dirty,
            }
        },
    }
    _check("source-baseline.schema.json", value)
    return value


def _repository_sources(document: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        source
        for source in document.get("provenance", {}).get("sources", [])
        if source.get("kind") == "repository"
    ]


def compile_evaluation_plan(document: dict[str, Any]) -> dict[str, Any] | None:
    _require_agent_workflow_ready(document)
    intent = evaluation_intent(document)
    active = intent["evaluations"]
    if not active:
        return None
    tasks = {
        task["id"]: task
        for task in _active(document.get("implementation", {}).get("tasks", []))
    }
    _, acceptance = _requirement_maps(document)
    commands: list[dict[str, Any]] = []
    oracle_refs: dict[str, dict[str, str]] = {}
    item_scorers: list[str | None] = []

    for item in active:
        metadata = item.get("metadata", {}) if isinstance(item.get("metadata"), dict) else {}
        unsupported_metadata = sorted(set(metadata) - _ALLOWED_EVALUATION_METADATA)
        if unsupported_metadata:
            raise ValueError(
                f"Agent-Workflow evaluation lowering cannot preserve metadata on {item['id']}: "
                + ", ".join(unsupported_metadata)
            )
        scorer = item.get("scorer")
        item_scorers.append(str(scorer) if scorer is not None else None)
        if scorer is not None and scorer not in AW_SCORERS:
            raise ValueError(
                f"Agent-Workflow 0.9.1 does not support scorer {scorer!r} requested by {item['id']}"
            )
        command = item.get("command")
        if item.get("timeout_seconds") is not None and not command:
            raise ValueError(f"evaluation {item['id']} declares timeout_seconds without an executable command")
        if scorer == "acceptance_commands" and not command:
            raise ValueError(
                f"evaluation {item['id']} requests acceptance_commands scoring without an acceptance command"
            )
        if command:
            commands.append(
                {
                    "id": item["id"],
                    "argv": command,
                    "timeout_seconds": item.get("timeout_seconds", 300),
                    "result_format": "exit-code",
                }
            )
        if not command and scorer is None:
            raise ValueError(
                f"Agent-Workflow evaluation lowering cannot execute {item['id']} without a command or supported scorer"
            )
        if item.get("oracle") in {"hidden", "external"}:
            ref = metadata.get("oracle_ref")
            if (
                not isinstance(ref, dict)
                or not isinstance(ref.get("id"), str)
                or not isinstance(ref.get("sha256"), str)
                or not re.fullmatch(r"[0-9a-f]{64}", ref["sha256"])
            ):
                raise ValueError(
                    f"Agent-Workflow evaluation lowering cannot represent {item['oracle']} oracle "
                    f"{item['id']} without metadata.oracle_ref containing id and lowercase sha256"
                )
            target_task_ids = _target_tasks_for_evaluation(item, tasks, acceptance)
            if not target_task_ids:
                raise ValueError(
                    f"Agent-Workflow oracle {item['id']} cannot be associated with an implementation task"
                )
            target_ref = {"id": ref["id"], "sha256": ref["sha256"]}
            for task_id in target_task_ids:
                previous = oracle_refs.get(task_id)
                if previous is not None and previous != target_ref:
                    raise ValueError(
                        f"Agent-Workflow task {task_id} would require multiple incompatible oracle references"
                    )
                oracle_refs[task_id] = target_ref

    if len(active) > 1 and len(set(item_scorers)) > 1:
        raise ValueError(
            "Agent-Workflow evaluation-plan/v1 carries scorers globally; distinct per-evaluation scorer assignments "
            "cannot be lowered without changing meaning"
        )
    scorers: set[str] = {scorer for scorer in item_scorers if scorer is not None}
    if commands:
        scorers.add("acceptance_commands")
    if not scorers:
        raise ValueError("Agent-Workflow evaluation plan requires at least one representable scorer")
    plan: dict[str, Any] = {
        "schema": "agent-workflow/evaluation-plan/v1",
        "dataset_split": "validation",
        "task_ids": list(tasks),
        "repetitions": 1,
        "timeout_seconds": max([300, *(item["timeout_seconds"] for item in commands)]),
        "scorers": sorted(scorers),
        "sandbox": "docker",
    }
    if commands:
        plan["acceptance_commands"] = commands
    if oracle_refs:
        plan["oracle_refs"] = oracle_refs
    _check("evaluation-plan.schema.json", plan)
    return plan


def compile_target(
    document: dict[str, Any],
    *,
    repository_analysis: dict[str, Any] | None = None,
    repository_root: str | Path | None = None,
) -> dict[str, str]:
    _require_agent_workflow_ready(document)
    if _repository_sources(document) and repository_analysis is None:
        raise ValueError(
            "canonical specification contains repository provenance; Agent-Workflow compilation requires "
            "--repository-analysis so source context is not silently discarded"
        )
    if repository_root is not None and repository_analysis is None:
        raise ValueError("repository_root is only valid with repository_analysis")

    source_baseline = None
    if repository_analysis is not None:
        source_baseline = compile_source_baseline(document, repository_analysis, repository_root)

    pack, resources = compile_prompt_pack(document, repository_analysis)
    plan = compile_evaluation_plan(document)
    files = dict(resources)
    files.update(_root_pack_resources(document, source_baseline is not None))
    files["pack.yaml"] = json.dumps(pack, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if plan is not None:
        files["evaluation-plan.json"] = json.dumps(plan, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if source_baseline is not None:
        files["source-baseline.json"] = (
            json.dumps(source_baseline, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
        )
    checksum_lines = []
    for path in sorted(files):
        checksum = hashlib.sha256(files[path].encode("utf-8")).hexdigest()
        checksum_lines.append(f"{checksum}  {path}")
    files["MANIFEST.sha256"] = "\n".join(checksum_lines) + "\n"
    return files


def write_target(output: str | Path, files: dict[str, str]) -> Path:
    root = Path(output)
    if root.is_symlink():
        raise ValueError(f"Agent-Workflow output root must be a real directory: {root}")
    if root.exists() and not root.is_dir():
        raise ValueError(f"Agent-Workflow output is not a directory: {root}")
    if root.exists() and any(root.iterdir()):
        raise ValueError(
            f"Agent-Workflow output directory must be empty to prevent stale target artifacts: {root}"
        )
    root.mkdir(parents=True, exist_ok=True)
    for relative, content in sorted(files.items()):
        path = PurePosixPath(relative)
        if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
            raise ValueError(f"unsafe generated Agent-Workflow target path: {relative}")
        target = root.joinpath(*path.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return root
