from __future__ import annotations
import hashlib
from pathlib import Path
from typing import Any
from jsonschema import Draft202012Validator
from .contracts import repo_root
from .evals import evaluation_intent
from .validate import validate

AW_VERSION = "0.9.0"


def _schema(name: str) -> dict[str, Any]:
    import json
    return json.loads((repo_root()/"compat"/"agent-workflow"/AW_VERSION/"schemas"/name).read_text())


def _check(schema_name: str, value: dict[str, Any]) -> None:
    errors = sorted(Draft202012Validator(_schema(schema_name)).iter_errors(value), key=lambda e: list(e.path))
    if errors:
        raise ValueError(f"generated Agent-Workflow artifact violates {schema_name}: {errors[0].message}")


def _run_id(spec_id: str, task_id: str) -> str:
    return "specgen-" + hashlib.sha256(f"{spec_id}:{task_id}".encode()).hexdigest()[:16]


def compile_prompt_pack(document: dict[str, Any]) -> tuple[dict[str, Any], dict[str, str]]:
    if not validate(document).valid:
        raise ValueError("cannot compile invalid canonical snapshot")
    tasks = {t["id"]: t for t in document.get("implementation", {}).get("tasks", []) if t.get("lifecycle", "active") != "retired"}
    phases = []
    prompts: dict[str, str] = {}
    assigned: set[str] = set()
    for index, phase in enumerate(document.get("implementation", {}).get("phases", []), 1):
        if phase.get("lifecycle", "active") == "retired": continue
        ids = phase.get("task_ids") or phase.get("tasks") or []
        if not ids and len(document.get("implementation", {}).get("phases", [])) == 1:
            ids = list(tasks)
        phase_tasks = []
        for task_id in ids:
            if task_id not in tasks: continue
            assigned.add(task_id); task = tasks[task_id]
            prompt_path = f"prompts/{task_id}.md"
            reqs = set(task.get("requirement_ids", []))
            statements = [r["statement"] for r in document.get("requirements", []) if r.get("id") in reqs]
            prompts[prompt_path] = "# " + task.get("title", task_id) + "\n\n" + "\n".join(f"- {x}" for x in statements) + "\n"
            entry = {"id": task_id, "tier": task.get("tier", "implementation"), "agent_run_id": _run_id(document["id"], task_id), "prompt": prompt_path, "dependencies": task.get("dependencies", [])}
            rc = task.get("result_contract")
            if isinstance(rc, dict) and rc.get("schema"):
                entry["result_contract"] = {"schema": rc["schema"], "required": bool(rc.get("required", True))}
            phase_tasks.append(entry)
        if phase_tasks:
            phases.append({"id": phase.get("id", index), "name": phase.get("name") or phase.get("description") or f"Phase {index}", "directory": phase.get("directory", f"phase-{index}"), "tasks": phase_tasks, "mandatory_order": [x["id"] for x in phase_tasks]})
    unassigned = [x for x in tasks if x not in assigned]
    if unassigned:
        raise ValueError(f"Agent-Workflow compile requires every task assigned to a phase: {', '.join(unassigned)}")
    pack = {"schema": "agent-workflow/prompt-pack/v1", "pack_id": document["id"], "workflow": {"name": "agent-workflow", "minimum_version": AW_VERSION}, "phases": phases}
    _check("pack.schema.json", pack)
    return pack, prompts


def compile_evaluation_plan(document: dict[str, Any]) -> dict[str, Any] | None:
    intent = evaluation_intent(document)
    active = intent["evaluations"]
    if not active:
        return None
    commands=[]; scorers=[]; oracle_refs={}
    for item in active:
        if item.get("scorer"): scorers.append(item["scorer"])
        if item.get("command"):
            commands.append({"id": item["id"], "argv": item["command"], "timeout_seconds": item.get("timeout_seconds",300), "result_format":"exit-code"})
        if item.get("oracle") in {"hidden", "external"}:
            ref = item.get("metadata", {}).get("oracle_ref")
            if not isinstance(ref, dict) or not isinstance(ref.get("id"), str) or not isinstance(ref.get("sha256"), str):
                raise ValueError(
                    f"Agent-Workflow evaluation lowering cannot represent {item['oracle']} oracle "
                    f"{item['id']} without metadata.oracle_ref containing id and sha256"
                )
            oracle_refs[item["id"]] = {"id": ref["id"], "sha256": ref["sha256"]}
    plan = {"schema":"agent-workflow/evaluation-plan/v1","dataset_split":"validation","task_ids":[t["id"] for t in document.get("implementation",{}).get("tasks",[]) if t.get("lifecycle","active")!="retired"],"repetitions":1,"timeout_seconds":300,"scorers": sorted(set(scorers)) or ["acceptance"],"sandbox":"docker"}
    if commands: plan["acceptance_commands"] = commands
    if oracle_refs: plan["oracle_refs"] = oracle_refs
    _check("evaluation-plan.schema.json", plan)
    return plan
