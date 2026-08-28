from __future__ import annotations

from typing import Any

from .canonical import canonical_json

_IGNORED_TOP_LEVEL = {"snapshot"}


def _equal(left: Any, right: Any) -> bool:
    return canonical_json(left) == canonical_json(right)


def _keyed_list(value: list[Any]) -> bool:
    return bool(value) and all(isinstance(item, dict) and isinstance(item.get("id"), str) for item in value)


def _diff(path: str, before: Any, after: Any, changes: list[dict[str, Any]]) -> None:
    if _equal(before, after):
        return
    if isinstance(before, dict) and isinstance(after, dict):
        for key in sorted(set(before) | set(after)):
            child = f"{path}.{key}"
            if key not in before:
                changes.append({"kind": "added", "path": child, "after": after[key]})
            elif key not in after:
                changes.append({"kind": "removed", "path": child, "before": before[key]})
            else:
                _diff(child, before[key], after[key], changes)
        return
    if isinstance(before, list) and isinstance(after, list) and (_keyed_list(before) or _keyed_list(after)):
        left = {item["id"]: item for item in before}
        right = {item["id"]: item for item in after}
        for entity_id in sorted(set(left) | set(right)):
            child = f"{path}[{entity_id}]"
            if entity_id not in left:
                changes.append({"kind": "added", "path": child, "entity_id": entity_id, "after": right[entity_id]})
            elif entity_id not in right:
                changes.append({"kind": "removed", "path": child, "entity_id": entity_id, "before": left[entity_id]})
            else:
                _diff(child, left[entity_id], right[entity_id], changes)
        return
    changes.append({"kind": "modified", "path": path, "before": before, "after": after})


def semantic_delta(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    if before.get("schema") != "specgen/spec/v1alpha2" or after.get("schema") != "specgen/spec/v1alpha2":
        raise ValueError("diff currently supports specgen/spec/v1alpha2 only")
    if before.get("id") != after.get("id"):
        raise ValueError("cannot diff snapshots from different spec ids")

    left = {key: value for key, value in before.items() if key not in _IGNORED_TOP_LEVEL}
    right = {key: value for key, value in after.items() if key not in _IGNORED_TOP_LEVEL}
    changes: list[dict[str, Any]] = []
    _diff("$", left, right, changes)
    return {
        "schema": "specgen/semantic-delta/v1alpha1",
        "spec_id": before["id"],
        "from_snapshot_id": before["snapshot"]["id"],
        "to_snapshot_id": after["snapshot"]["id"],
        "changes": changes,
    }
