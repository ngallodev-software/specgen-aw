from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Any

from .canonical import digest, snapshot_digest
from .elicitation import assess
from .repository import analyze_repository
from .validate import validate


def codebase_memory_capability() -> dict[str, Any]:
    """Describe optional codebase-memory-mcp availability without requiring it."""

    executable = shutil.which("codebase-memory-mcp")
    if executable is None:
        return {
            "available": False,
            "binary": None,
            "version": None,
            "mcp_registration": "unknown",
            "cli_fallback": False,
        }

    version: str | None = None
    try:
        result = subprocess.run(
            [executable, "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=2,
        )
        text = (result.stdout or result.stderr).strip()
        if text:
            version = text.splitlines()[0].strip()
    except (OSError, subprocess.TimeoutExpired):
        pass

    return {
        "available": True,
        "binary": executable,
        "version": version,
        "mcp_registration": "unknown",
        "cli_fallback": True,
    }


def _question(
    qid: str,
    kind: str,
    prompt: str,
    rationale: str,
    *,
    priority: str = "important",
    refs: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "id": qid,
        "kind": kind,
        "priority": priority,
        "prompt": prompt,
        "rationale": rationale,
        "affected_refs": refs or [],
    }


def _user_questions(spec: dict[str, Any] | None) -> list[dict[str, Any]]:
    questions: list[dict[str, Any]] = []
    if spec is None:
        return [
            _question(
                "BQ-0001",
                "intent",
                "What existing behavior needs to change, and what outcome should be different for the user or operator?",
                "Code can reveal current behavior but cannot authorize the desired product change.",
                priority="blocker",
            ),
            _question(
                "BQ-0002",
                "preservation",
                "What existing behavior, interface, compatibility promise, or operational property must not regress?",
                "Brownfield specifications need explicit preservation boundaries before implementation scope is chosen.",
            ),
            _question(
                "BQ-0003",
                "scope",
                "Are there components, integrations, migrations, or cleanup work that are explicitly out of scope?",
                "Repository connectivity can make adjacent work look relevant even when it is not authorized.",
            ),
            _question(
                "BQ-0004",
                "verification",
                "What observable evidence would convince you that the change is complete?",
                "The agent can discover existing tests but cannot decide the intended acceptance bar on the user's behalf.",
            ),
        ]

    intent = spec.get("intent", {})
    scope = spec.get("scope", {})
    if not str(intent.get("problem", "")).strip():
        questions.append(_question(
            "BQ-0001", "intent",
            "What current behavior or limitation is the specification intended to change?",
            "A repository can explain the present system, not the desired problem statement.",
            priority="blocker",
        ))
    if not intent.get("objectives"):
        questions.append(_question(
            "BQ-0002", "intent",
            "What concrete outcome should this brownfield change achieve?",
            "Implementation research should be steered by an authorized outcome rather than repository structure alone.",
            priority="blocker",
        ))
    if not scope.get("included"):
        questions.append(_question(
            "BQ-0003", "scope",
            "What behavior or system area is definitely in scope?",
            "A narrow starting boundary prevents broad graph exploration from becoming accidental scope.",
        ))
    if not scope.get("protected"):
        questions.append(_question(
            "BQ-0004", "preservation",
            "Which existing behaviors or compatibility boundaries must be preserved while making this change?",
            "Preservation is a first-class brownfield requirement and should not be inferred solely from current code.",
        ))
    if not spec.get("acceptance_criteria"):
        questions.append(_question(
            "BQ-0005", "verification",
            "What externally observable result should be used as the first acceptance criterion?",
            "Existing tests provide evidence but do not automatically define the intended acceptance contract.",
        ))
    return questions


def _focus_areas(spec: dict[str, Any] | None, analysis: dict[str, Any]) -> list[dict[str, Any]]:
    areas: list[dict[str, Any]] = []

    def add(kind: str, label: str, *, path: str | None = None, refs: list[str] | None = None) -> None:
        value: dict[str, Any] = {
            "id": f"FOCUS-{len(areas)+1:04d}",
            "kind": kind,
            "label": label,
            "affected_refs": refs or [],
        }
        if path:
            value["path"] = path
        areas.append(value)

    if spec is not None:
        for item in spec.get("requirements", []):
            if item.get("lifecycle", "active") == "active":
                label = item.get("description") or item.get("name") or item["id"]
                add("requirement", str(label), refs=[item["id"]])
        for item in spec.get("interfaces", []):
            if item.get("lifecycle", "active") == "active":
                add(
                    "interface",
                    str(item.get("name") or item.get("description") or item["id"]),
                    path=item.get("path"),
                    refs=[item["id"]],
                )
        for item in spec.get("data_contracts", []):
            if item.get("lifecycle", "active") == "active":
                add(
                    "data_contract",
                    str(item.get("name") or item.get("description") or item["id"]),
                    path=item.get("path"),
                    refs=[item["id"]],
                )
        for text in spec.get("scope", {}).get("included", []):
            if isinstance(text, str) and text.strip():
                add("scope", text.strip())

    for conflict in analysis.get("contradictions", []):
        add(
            "contradiction",
            conflict["message"],
            path=conflict.get("path"),
            refs=[conflict["spec_ref"]] if conflict.get("spec_ref") else [],
        )

    return areas[:50]


def _research_tasks(enhanced: bool) -> list[dict[str, Any]]:
    if not enhanced:
        return [
            {
                "id": "RESEARCH-0001",
                "objective": "Use the deterministic repository analysis and explicitly referenced files to establish the current-system boundary.",
                "preferred_tools": ["specgen repo analyze", "repository file read/search"],
                "stop_when": "The relevant durable declarations, explicit references, contradictions, and likely implementation area are identified.",
            },
            {
                "id": "RESEARCH-0002",
                "objective": "Inspect only the source files needed to answer unresolved spec questions; record semantic conclusions as agent inference, not deterministic repository discovery.",
                "preferred_tools": ["targeted repository search", "targeted source read"],
                "stop_when": "Each material conclusion is backed by a file/symbol reference or remains explicitly unresolved.",
            },
        ]

    return [
        {
            "id": "RESEARCH-0001",
            "objective": "Confirm the indexed project and graph shape once before issuing structural queries.",
            "preferred_tools": ["list_projects", "index_status", "index_repository", "get_graph_schema"],
            "stop_when": "The target repository is indexed at the intended path/revision and the graph labels/relationships are understood.",
        },
        {
            "id": "RESEARCH-0002",
            "objective": "Get a single architecture overview, then identify the smallest components, routes, packages, or entry points plausibly connected to the requested behavior.",
            "preferred_tools": ["get_architecture", "search_graph", "search_code"],
            "stop_when": "A short candidate set of relevant symbols/components is established; do not inventory the whole repository.",
        },
        {
            "id": "RESEARCH-0003",
            "objective": "Trace behavior around the candidate symbols with shallow call paths before reading source broadly.",
            "preferred_tools": ["trace_path", "search_graph", "query_graph"],
            "stop_when": "Callers, callees, boundary interfaces, and likely data-flow seams needed for the spec are understood; start at depth 1-2 and expand only when evidence requires it.",
        },
        {
            "id": "RESEARCH-0004",
            "objective": "Read only decisive code and declarations for the narrowed symbols, plus tests/consumers that establish observable current behavior.",
            "preferred_tools": ["get_code_snippet", "search_code", "query_graph"],
            "stop_when": "Every important behavioral claim has a concrete path/symbol evidence reference and unnecessary source reading has stopped.",
        },
        {
            "id": "RESEARCH-0005",
            "objective": "Assess blast radius and preservation risk without turning connectivity into authorized scope.",
            "preferred_tools": ["query_graph", "trace_path", "detect_changes"],
            "stop_when": "Direct consumers, shared contracts, persistence/config boundaries, and high-risk preservation points are identified; use detect_changes only when an actual git diff exists.",
        },
        {
            "id": "RESEARCH-0006",
            "objective": "Convert findings into a concise agent-assisted brownfield analysis and separate observations, strong inferences, tentative conclusions, and user decisions.",
            "preferred_tools": ["specgen/brownfield-analysis/v1alpha1"],
            "stop_when": "The artifact contains only spec-relevant findings and unresolved questions, with evidence references sufficient for review.",
        },
    ]


def brownfield_plan(
    root: str | Path,
    spec: dict[str, Any] | None = None,
    mode: str = "guided",
) -> dict[str, Any]:
    root = Path(root).resolve()
    analysis = analyze_repository(root, spec, mode)
    capability = codebase_memory_capability()
    enhanced = bool(capability["available"])

    plan: dict[str, Any] = {
        "schema": "specgen/brownfield-plan/v1alpha1",
        "repository": analysis["repository"],
        "baseline": analysis["baseline"],
        "mode": mode,
        "strategy": "codebase-memory-assisted" if enhanced else "evidence-first",
        "codebase_memory": capability,
        "repository_analysis": {
            "digest": digest(analysis),
            "evidence_count": len(analysis["evidence"]),
            "interface_count": len(analysis["interfaces"]),
            "data_contract_count": len(analysis["data_contracts"]),
            "contradiction_count": len(analysis["contradictions"]),
            "blocker_count": sum(1 for item in analysis["contradictions"] if item["severity"] == "blocker"),
        },
        "focus_areas": _focus_areas(spec, analysis),
        "user_questions": _user_questions(spec),
        "research_tasks": _research_tasks(enhanced),
        "analysis_contract": "specgen/brownfield-analysis/v1alpha1",
        "guardrails": [
            "ask the user for intent, policy, priority, and acceptance decisions; investigate code-answerable implementation questions instead of asking them",
            "start from declared scope and deterministic evidence, then narrow graph queries before reading source",
            "do not treat graph connectivity as authorization to expand scope",
            "distinguish observed code facts from agent inference and from user-authorized decisions",
            "record paths and symbols for material findings; do not copy large source excerpts into specification artifacts",
            "preserve the deterministic repository-analysis artifact separately from agent-assisted semantic analysis",
            "stop research when the remaining uncertainty requires a user decision rather than more code exploration",
        ],
    }
    if spec is not None:
        readiness = assess(spec, mode)
        plan["spec"] = {
            "id": spec["id"],
            "snapshot_id": spec["snapshot"]["id"],
            "digest": snapshot_digest(spec),
            "ready": readiness["ready"],
            "blocker_count": readiness["blocker_count"],
        }

    result = validate(plan)
    if not result.valid:
        first = result.diagnostics[0]
        raise ValueError(f"generated brownfield plan failed contract: {first.path}: {first.message}")
    return plan
