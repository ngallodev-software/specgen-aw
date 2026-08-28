from __future__ import annotations

from typing import Any

from .modes import AuthoringMode, mode as resolve_mode
from .validate import validate


def _active(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [item for item in items if item.get("lifecycle", "active") == "active"]


def _question(
    qid: str,
    kind: str,
    prompt: str,
    *,
    severity: str = "question",
    paths: list[str] | None = None,
    refs: list[str] | None = None,
    guardrail: str | None = None,
) -> dict[str, Any]:
    value: dict[str, Any] = {
        "id": qid,
        "kind": kind,
        "severity": severity,
        "prompt": prompt,
        "affected_paths": paths or [],
        "affected_refs": refs or [],
    }
    if guardrail:
        value["guardrail"] = guardrail
    return value


def _coverage_questions(document: dict[str, Any], profile: AuthoringMode) -> list[dict[str, Any]]:
    questions: list[dict[str, Any]] = []
    requirements = _active(document.get("requirements", []))
    acceptance = _active(document.get("acceptance_criteria", []))
    evaluations = _active(document.get("evaluations", []))
    tasks = _active(document.get("implementation", {}).get("tasks", []))
    phases = _active(document.get("implementation", {}).get("phases", []))

    acceptance_by_req: set[str] = set()
    for item in acceptance:
        acceptance_by_req.update(item.get("requirement_ids", []))
    evaluation_by_req: set[str] = set()
    for item in evaluations:
        evaluation_by_req.update(item.get("requirement_ids", []))
    task_by_req: set[str] = set()
    for item in tasks:
        task_by_req.update(item.get("requirement_ids", []))

    if profile.name != "express":
        for req in requirements:
            rid = req["id"]
            if rid not in acceptance_by_req:
                questions.append(_question(
                    f"Q-acceptance-{rid}", "verification",
                    f"What observable acceptance criterion proves {rid}?",
                    paths=["/acceptance_criteria"], refs=[rid],
                ))

    if profile.strict:
        for req in requirements:
            rid = req["id"]
            if not req.get("verification_refs") and rid not in evaluation_by_req:
                questions.append(_question(
                    f"Q-verification-{rid}", "verification",
                    f"How will {rid} be verified before the specification is finalized?",
                    severity="blocker", paths=[f"/requirements/{rid}"], refs=[rid],
                ))
        for item in _active(document.get("unresolved_questions", [])):
            questions.append(_question(
                f"Q-resolve-{item['id']}", "clarification",
                item.get("description") or item.get("name") or f"Resolve {item['id']}.",
                severity="blocker", paths=["/unresolved_questions"], refs=[item["id"]],
            ))

    if profile.agent_workflow:
        guardrail = "agent-workflow phased implementation"
        if not phases:
            questions.append(_question(
                "Q-aw-phases", "implementation",
                "Define implementation phases suitable for ordered Agent-Workflow execution.",
                severity="blocker", paths=["/implementation/phases"], guardrail=guardrail,
            ))
        if not tasks:
            questions.append(_question(
                "Q-aw-tasks", "implementation",
                "Decompose the implementation into explicit Agent-Workflow tasks.",
                severity="blocker", paths=["/implementation/tasks"], guardrail=guardrail,
            ))
        for task in tasks:
            tid = task["id"]
            if not task.get("requirement_ids"):
                questions.append(_question(
                    f"Q-aw-task-requirement-{tid}", "implementation",
                    f"Which requirement or invariant authorizes task {tid}?",
                    severity="blocker", paths=[f"/implementation/tasks/{tid}"], refs=[tid], guardrail=guardrail,
                ))
            if not task.get("result_contract"):
                questions.append(_question(
                    f"Q-aw-result-{tid}", "compatibility",
                    f"Define the structured result contract expected from Agent-Workflow task {tid}.",
                    severity="blocker", paths=[f"/implementation/tasks/{tid}/result_contract"], refs=[tid], guardrail=guardrail,
                ))
        for req in requirements:
            rid = req["id"]
            if rid not in task_by_req:
                questions.append(_question(
                    f"Q-aw-task-coverage-{rid}", "implementation",
                    f"Which implementation task carries requirement {rid}?",
                    severity="blocker", paths=["/implementation/tasks"], refs=[rid], guardrail=guardrail,
                ))
            if rid not in evaluation_by_req:
                questions.append(_question(
                    f"Q-aw-eval-{rid}", "verification",
                    f"Define evaluation intent for {rid} so it can later lower into an Agent-Workflow evaluation plan.",
                    severity="blocker", paths=["/evaluations"], refs=[rid], guardrail=guardrail,
                ))

    return questions


def assess(document: dict[str, Any], mode_name: str = "guided") -> dict[str, Any]:
    profile = resolve_mode(mode_name)
    result = validate(document)
    questions: list[dict[str, Any]] = []

    for index, diagnostic in enumerate(result.diagnostics, start=1):
        if diagnostic.severity == "error":
            questions.append(_question(
                f"Q-contract-{index}", "repair", diagnostic.message,
                severity="blocker", paths=[diagnostic.path], guardrail="canonical contract",
            ))

    if result.valid:
        questions.extend(_coverage_questions(document, profile))

    blockers = sum(1 for item in questions if item["severity"] == "blocker")
    return {
        "schema": "specgen/elicitation-plan/v1alpha1",
        "mode": profile.name,
        "ready": result.valid and blockers == 0,
        "blocker_count": blockers,
        "questions": questions,
        "guardrails": _guardrails(profile),
    }


def _guardrails(profile: AuthoringMode) -> list[str]:
    values = [
        "canonical snapshot must validate before finalization",
        "unknowns remain explicit rather than inferred silently",
    ]
    if profile.strict:
        values.extend([
            "active requirements require explicit verification intent",
            "unresolved questions block finalization",
        ])
    if profile.agent_workflow:
        values.extend([
            "implementation is decomposed into ordered phases and tasks",
            "every active requirement is carried by an implementation task",
            "every task declares a structured result contract",
            "every active requirement carries evaluation intent",
            "Agent-Workflow runtime state is not embedded in the canonical spec",
            "later compilation must target pinned Agent-Workflow public contracts only",
        ])
    return values
