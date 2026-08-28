from __future__ import annotations
from typing import Any


def evaluation_intent(document: dict[str, Any]) -> dict[str, Any]:
    items = []
    for item in document.get("evaluations", []):
        if item.get("lifecycle", "active") == "retired":
            continue
        metadata = item.get("metadata", {}) if isinstance(item.get("metadata"), dict) else {}
        oracle = item.get("oracle", metadata.get("oracle", "public"))
        out = {
            "id": item["id"],
            "kind": item["kind"],
            "requirement_ids": sorted(item.get("requirement_ids", [])),
            "acceptance_ids": sorted(item.get("acceptance_ids", [])),
            "oracle": oracle,
        }
        for key in ("scorer", "command", "timeout_seconds"):
            value = item.get(key, metadata.get(key))
            if value is not None:
                out[key] = value
        if metadata:
            out["metadata"] = metadata
        items.append(out)
    return {"schema": "specgen/evaluation-intent/v1alpha1", "spec_id": document["id"], "evaluations": items}
