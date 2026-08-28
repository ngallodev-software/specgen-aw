from __future__ import annotations

from pathlib import Path
from typing import Any

from .repository import _sha256, repository_baseline


def repository_drift(analysis: dict[str, Any], root: str | Path) -> dict[str, Any]:
    if analysis.get("schema") != "specgen/repository-analysis/v1alpha1":
        raise ValueError("drift requires specgen/repository-analysis/v1alpha1")
    root = Path(root).resolve()
    current = repository_baseline(root)
    changes: list[dict[str, str]] = []
    baseline = analysis["baseline"]
    if baseline.get("revision") != current.get("revision"):
        changes.append({
            "kind": "baseline_revision", "path": ".",
            "expected": str(baseline.get("revision", "")), "observed": str(current.get("revision", "")),
        })
    for item in analysis.get("evidence", []):
        relative = item["path"]
        path = root / relative
        if not path.is_file():
            changes.append({"kind": "missing", "path": relative, "expected": item["digest"]})
            continue
        observed = _sha256(path)
        if observed != item["digest"]:
            changes.append({"kind": "modified", "path": relative, "expected": item["digest"], "observed": observed})
    return {
        "schema": "specgen/repository-drift/v1alpha1",
        "drifted": bool(changes),
        "baseline": baseline,
        "current": current,
        "changes": changes,
    }
