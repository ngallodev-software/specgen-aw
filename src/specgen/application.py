"""Small application conveniences over SpecGen's canonical contracts.

These helpers create/load canonical documents and append authoring events without
introducing mutable application state or another specification model.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from .history import append_event, load_events
from .validate import validate


def load_document(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("document root must be a JSON object")
    return value


def write_document(path: str | Path, document: dict[str, Any]) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return target


def create_candidate(
    spec_id: str,
    title: str,
    *,
    version: str = "0.1.0",
    created_at: str,
    snapshot_id: str | None = None,
    problem: str = "",
) -> dict[str, Any]:
    """Create the smallest valid v1alpha2 draft without inventing product decisions.

    ``created_at`` is explicit so callers, agents, and tests control provenance and
    reproducibility instead of receiving an implicit wall-clock timestamp.
    """

    document: dict[str, Any] = {
        "schema": "specgen/spec/v1alpha2",
        "id": spec_id,
        "title": title,
        "version": version,
        "status": "draft",
        "state": {"kind": "current"},
        "snapshot": {
            "id": snapshot_id or f"{spec_id}:snapshot:1",
            "sequence": 1,
            "created_at": created_at,
        },
        "intent": {"problem": problem, "objectives": [], "non_goals": []},
        "scope": {"included": [], "excluded": []},
        "requirements": [],
        "acceptance_criteria": [],
        "evaluations": [],
        "implementation": {"tasks": [], "phases": []},
        "unresolved_questions": [],
        "traceability": [],
        "preservation": {"claims": []},
        "provenance": {"sources": []},
    }
    result = validate(document)
    if not result.valid:
        first = result.diagnostics[0]
        raise ValueError(f"cannot create canonical candidate: {first.path}: {first.message}")
    return document


def record_event(
    path: str | Path,
    *,
    spec_id: str,
    recorded_at: str,
    kind: str,
    actor: str,
    payload: dict[str, Any],
    event_id: str | None = None,
    affected_refs: Iterable[str] = (),
    supersedes_event_ids: Iterable[str] = (),
) -> dict[str, Any]:
    """Construct and append one validated event to the single-writer authoring log."""

    prior = load_events(path)
    if prior and prior[0]["spec_id"] != spec_id:
        raise ValueError(f"event log belongs to spec {prior[0]['spec_id']!r}, not {spec_id!r}")
    sequence = len(prior) + 1
    event: dict[str, Any] = {
        "schema": "specgen/authoring-event/v1alpha1",
        "id": event_id or f"{spec_id}:event:{sequence}",
        "spec_id": spec_id,
        "sequence": sequence,
        "recorded_at": recorded_at,
        "kind": kind,
        "actor": actor,
        "payload": payload,
    }
    affected = list(affected_refs)
    superseded = list(supersedes_event_ids)
    if affected:
        event["affected_refs"] = affected
    if superseded:
        event["supersedes_event_ids"] = superseded
    result = validate(event)
    if not result.valid:
        first = result.diagnostics[0]
        raise ValueError(f"cannot record authoring event: {first.path}: {first.message}")
    append_event(path, event)
    return event
