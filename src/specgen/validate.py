from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable

from jsonschema import Draft202012Validator, FormatChecker

from .canonical import snapshot_digest
from .contracts import load_contract


@dataclass(frozen=True)
class Diagnostic:
    severity: str
    code: str
    message: str
    path: str = "$"

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class ValidationResult:
    diagnostics: tuple[Diagnostic, ...]

    @property
    def valid(self) -> bool:
        return not any(item.severity == "error" for item in self.diagnostics)

    def as_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "diagnostics": [item.as_dict() for item in self.diagnostics],
        }


def _path(parts: Iterable[Any]) -> str:
    result = "$"
    for part in parts:
        result += f"[{part}]" if isinstance(part, int) else f".{part}"
    return result


def _schema_diagnostics(document: dict[str, Any]) -> list[Diagnostic]:
    contract_id = document.get("schema")
    if not isinstance(contract_id, str):
        return [Diagnostic("error", "schema.missing", "document must declare a string schema")]
    try:
        schema = load_contract(contract_id)
    except ValueError as exc:
        return [Diagnostic("error", "schema.unsupported", str(exc), "$.schema")]

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        Diagnostic("error", "schema.invalid", error.message, _path(error.absolute_path))
        for error in sorted(validator.iter_errors(document), key=lambda item: list(item.absolute_path))
    ]


def _iter_entities(spec: dict[str, Any]) -> Iterable[tuple[str, dict[str, Any]]]:
    fields = (
        "requirements",
        "interfaces",
        "data_contracts",
        "decisions",
        "acceptance_criteria",
        "evaluations",
        "risks",
        "unresolved_questions",
        "traceability",
    )
    for field in fields:
        for index, item in enumerate(spec.get(field, [])):
            if isinstance(item, dict) and isinstance(item.get("id"), str):
                yield f"$.{field}[{index}]", item
    implementation = spec.get("implementation", {})
    if isinstance(implementation, dict):
        for field in ("tasks", "phases"):
            for index, item in enumerate(implementation.get(field, [])):
                if isinstance(item, dict) and isinstance(item.get("id"), str):
                    yield f"$.implementation.{field}[{index}]", item
    preservation = spec.get("preservation", {})
    if isinstance(preservation, dict):
        for index, item in enumerate(preservation.get("claims", [])):
            if isinstance(item, dict) and isinstance(item.get("id"), str):
                yield f"$.preservation.claims[{index}]", item
    provenance = spec.get("provenance", {})
    if isinstance(provenance, dict):
        for index, item in enumerate(provenance.get("sources", [])):
            if isinstance(item, dict) and isinstance(item.get("id"), str):
                yield f"$.provenance.sources[{index}]", item


def _spec_diagnostics(spec: dict[str, Any]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    entities = list(_iter_entities(spec))
    by_id: dict[str, str] = {}
    for path, item in entities:
        item_id = item["id"]
        previous = by_id.get(item_id)
        if previous:
            diagnostics.append(Diagnostic("error", "id.duplicate", f"duplicate id {item_id!r}; first seen at {previous}", f"{path}.id"))
        else:
            by_id[item_id] = path

    requirements = {item.get("id") for item in spec.get("requirements", []) if isinstance(item, dict)}
    acceptance = {item.get("id") for item in spec.get("acceptance_criteria", []) if isinstance(item, dict)}
    evaluations = {item.get("id") for item in spec.get("evaluations", []) if isinstance(item, dict)}
    tasks = {
        item.get("id")
        for item in spec.get("implementation", {}).get("tasks", [])
        if isinstance(item, dict)
    }
    provenance = {
        item.get("id")
        for item in spec.get("provenance", {}).get("sources", [])
        if isinstance(item, dict)
    }
    all_ids = set(by_id)
    preservation_ids = {
        item.get("id")
        for item in spec.get("preservation", {}).get("claims", [])
        if isinstance(item, dict)
    }
    content_ids = all_ids - provenance - preservation_ids

    def check_refs(values: Any, allowed: set[Any], path: str, code: str) -> None:
        if not isinstance(values, list):
            return
        for index, ref in enumerate(values):
            if ref not in allowed:
                diagnostics.append(Diagnostic("error", code, f"unknown reference {ref!r}", f"{path}[{index}]"))

    for index, item in enumerate(spec.get("requirements", [])):
        if not isinstance(item, dict):
            continue
        path = f"$.requirements[{index}]"
        check_refs(item.get("source_refs"), provenance, f"{path}.source_refs", "ref.provenance")
        check_refs(item.get("provenance_refs"), provenance, f"{path}.provenance_refs", "ref.provenance")
        check_refs(item.get("verification_refs"), acceptance | evaluations, f"{path}.verification_refs", "ref.verification")
        if item.get("lifecycle", "active") == "active" and not item.get("verification_refs"):
            diagnostics.append(Diagnostic("warning", "coverage.verification", f"active requirement {item.get('id')!r} has no verification_refs", path))

    for field in ("interfaces", "data_contracts", "decisions", "evaluations", "risks", "unresolved_questions"):
        for index, item in enumerate(spec.get(field, [])):
            if isinstance(item, dict):
                check_refs(item.get("provenance_refs"), provenance, f"$.{field}[{index}].provenance_refs", "ref.provenance")

    for index, item in enumerate(spec.get("acceptance_criteria", [])):
        if not isinstance(item, dict):
            continue
        path = f"$.acceptance_criteria[{index}]"
        check_refs(item.get("requirement_ids"), requirements, f"{path}.requirement_ids", "ref.requirement")
        check_refs(item.get("provenance_refs"), provenance, f"{path}.provenance_refs", "ref.provenance")

    for index, item in enumerate(spec.get("evaluations", [])):
        if not isinstance(item, dict):
            continue
        path = f"$.evaluations[{index}]"
        check_refs(item.get("requirement_ids"), requirements, f"{path}.requirement_ids", "ref.requirement")
        check_refs(item.get("acceptance_ids"), acceptance, f"{path}.acceptance_ids", "ref.acceptance")

    for index, item in enumerate(spec.get("implementation", {}).get("tasks", [])):
        if not isinstance(item, dict):
            continue
        path = f"$.implementation.tasks[{index}]"
        check_refs(item.get("requirement_ids"), requirements, f"{path}.requirement_ids", "ref.requirement")
        check_refs(item.get("dependencies"), tasks, f"{path}.dependencies", "ref.task")
        check_refs(item.get("provenance_refs"), provenance, f"{path}.provenance_refs", "ref.provenance")
        if item.get("id") in set(item.get("dependencies") or []):
            diagnostics.append(Diagnostic("error", "task.self_dependency", "task cannot depend on itself", f"{path}.dependencies"))

    for index, item in enumerate(spec.get("implementation", {}).get("phases", [])):
        if isinstance(item, dict):
            check_refs(item.get("provenance_refs"), provenance, f"$.implementation.phases[{index}].provenance_refs", "ref.provenance")

    dependency_map = {
        item.get("id"): tuple(item.get("dependencies") or [])
        for item in spec.get("implementation", {}).get("tasks", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(task_id: str) -> bool:
        if task_id in visiting:
            return True
        if task_id in visited:
            return False
        visiting.add(task_id)
        cyclic = any(ref in dependency_map and visit(ref) for ref in dependency_map.get(task_id, ()))
        visiting.remove(task_id)
        visited.add(task_id)
        return cyclic

    for task_id in dependency_map:
        if visit(task_id):
            diagnostics.append(Diagnostic("error", "task.dependency_cycle", f"task dependency cycle includes {task_id!r}", by_id.get(task_id, "$.implementation.tasks")))
            break

    for index, link in enumerate(spec.get("traceability", [])):
        if not isinstance(link, dict):
            continue
        for key in ("from", "to"):
            ref = link.get(key)
            if ref not in content_ids:
                diagnostics.append(Diagnostic("error", "ref.trace", f"unknown content reference {ref!r}", f"$.traceability[{index}].{key}"))

    for index, claim in enumerate(spec.get("preservation", {}).get("claims", [])):
        if not isinstance(claim, dict):
            continue
        path = f"$.preservation.claims[{index}]"
        source_ref = claim.get("source_ref")
        if source_ref not in provenance:
            diagnostics.append(Diagnostic("error", "ref.preservation_source", f"unknown provenance source {source_ref!r}", f"{path}.source_ref"))
        check_refs(claim.get("target_refs"), content_ids, f"{path}.target_refs", "ref.preservation_target")
        status = claim.get("status")
        if status == "represented" and not claim.get("target_refs"):
            diagnostics.append(Diagnostic("error", "preservation.unmapped", "represented claim requires at least one target_ref", path))
        if status == "intentionally_excluded" and not str(claim.get("rationale", "")).strip():
            diagnostics.append(Diagnostic("error", "preservation.rationale", "intentionally excluded claim requires rationale", path))

    snapshot = spec.get("snapshot", {})
    if isinstance(snapshot, dict):
        snapshot_id = snapshot.get("id")
        sequence = snapshot.get("sequence")
        parent = snapshot.get("parent_snapshot_id")
        if sequence == 1 and parent:
            diagnostics.append(Diagnostic("error", "snapshot.parent", "sequence 1 snapshot cannot declare parent_snapshot_id", "$.snapshot.parent_snapshot_id"))
        if isinstance(sequence, int) and sequence > 1 and not parent:
            diagnostics.append(Diagnostic("error", "snapshot.parent", "snapshot sequence greater than 1 requires parent_snapshot_id", "$.snapshot"))
        if parent and parent == snapshot_id:
            diagnostics.append(Diagnostic("error", "snapshot.parent", "snapshot cannot be its own parent", "$.snapshot.parent_snapshot_id"))
        declared = snapshot.get("content_digest")
        if declared and declared != snapshot_digest(spec):
            diagnostics.append(Diagnostic("error", "snapshot.digest", "content_digest does not match canonical snapshot digest", "$.snapshot.content_digest"))

    state = spec.get("state", {})
    if isinstance(state, dict) and state.get("kind") == "proposed":
        if state.get("base_snapshot_id") == spec.get("snapshot", {}).get("id"):
            diagnostics.append(Diagnostic("error", "state.base_snapshot", "proposed state base_snapshot_id must identify the prior snapshot, not the proposed snapshot", "$.state.base_snapshot_id"))

    return diagnostics


def validate(document: dict[str, Any]) -> ValidationResult:
    diagnostics = _schema_diagnostics(document)
    if diagnostics:
        return ValidationResult(tuple(diagnostics))
    if document.get("schema") == "specgen/spec/v1alpha2":
        diagnostics.extend(_spec_diagnostics(document))
    return ValidationResult(tuple(diagnostics))
