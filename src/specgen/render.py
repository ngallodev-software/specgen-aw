from __future__ import annotations

import json
from typing import Any


def _items(values: list[str]) -> list[str]:
    return [f"- {value}" for value in values] or ["- _None._"]


def _entity_heading(item: dict[str, Any], fallback: str) -> str:
    title = item.get("name") or item.get("title") or item.get("statement") or item.get("criterion") or fallback
    return f"### `{item.get('id', fallback)}` — {title}"


def _render_entities(title: str, items: list[dict[str, Any]]) -> list[str]:
    lines = [f"## {title}", ""]
    if not items:
        return lines + ["_None._", ""]
    for item in items:
        lines += [_entity_heading(item, title), ""]
        for key, value in item.items():
            if key in {"id", "name", "title"}:
                continue
            if isinstance(value, list):
                text = ", ".join(str(v) for v in value) if value else "—"
            elif isinstance(value, dict):
                text = f"`{json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))}`"
            else:
                text = str(value)
            lines.append(f"- **{key.replace('_', ' ').title()}:** {text}")
        lines.append("")
    return lines


def render_markdown(spec: dict[str, Any]) -> str:
    if spec.get("schema") != "specgen/spec/v1alpha2":
        raise ValueError("render currently supports specgen/spec/v1alpha2 only")

    snapshot = spec["snapshot"]
    state = spec["state"]
    intent = spec["intent"]
    scope = spec["scope"]
    lines = [
        f"# {spec['title']}",
        "",
        f"> Spec `{spec['id']}` · version `{spec['version']}` · snapshot `{snapshot['id']}` · {state['kind']} · {spec['status']}",
        "",
        "## Snapshot",
        "",
        f"- **Created:** {snapshot['created_at']}",
        f"- **Sequence:** {snapshot['sequence']}",
        f"- **Parent:** {snapshot.get('parent_snapshot_id', '—')}",
        f"- **Digest:** {snapshot.get('content_digest', '—')}",
        f"- **Authoring events:** {', '.join(snapshot.get('authoring_event_ids', [])) or '—'}",
        "",
        "## Intent",
        "",
        intent.get("problem", ""),
        "",
        "### Objectives",
        "",
        *_items(intent.get("objectives", [])),
        "",
        "### Outcomes",
        "",
        *_items(intent.get("outcomes", [])),
        "",
        "### Non-goals",
        "",
        *_items(intent.get("non_goals", [])),
        "",
        "## Context",
        "",
        f"`{json.dumps(spec.get('context', {}), ensure_ascii=False, sort_keys=True, separators=(',', ':'))}`",
        "",
        "## Scope",
        "",
        "### Included",
        "",
        *_items(scope.get("included", [])),
        "",
        "### Excluded",
        "",
        *_items(scope.get("excluded", [])),
        "",
        "### Protected",
        "",
        *_items(scope.get("protected", [])),
        "",
        "### Constraints",
        "",
        *_items(scope.get("constraints", [])),
        "",
    ]

    lines += _render_entities("Requirements", spec.get("requirements", []))
    lines += _render_entities("Interfaces", spec.get("interfaces", []))
    lines += _render_entities("Data contracts", spec.get("data_contracts", []))
    lines += _render_entities("Decisions", spec.get("decisions", []))
    lines += _render_entities("Acceptance criteria", spec.get("acceptance_criteria", []))
    lines += _render_entities("Evaluations", spec.get("evaluations", []))
    lines += _render_entities("Implementation tasks", spec.get("implementation", {}).get("tasks", []))
    lines += _render_entities("Implementation phases", spec.get("implementation", {}).get("phases", []))
    lines += _render_entities("Risks", spec.get("risks", []))
    lines += _render_entities("Unresolved questions", spec.get("unresolved_questions", []))
    lines += _render_entities("Preservation claims", spec.get("preservation", {}).get("claims", []))
    lines += _render_entities("Provenance sources", spec.get("provenance", {}).get("sources", []))

    lines += [
        "## Extensions",
        "",
        f"`{json.dumps(spec.get('extensions', {}), ensure_ascii=False, sort_keys=True, separators=(',', ':'))}`",
        "",
        "## Traceability",
        "",
    ]
    trace = spec.get("traceability", [])
    if trace:
        for link in trace:
            relation = link.get("relation", "relates_to")
            lines.append(f"- `{link['from']}` — **{relation}** → `{link['to']}`")
    else:
        lines.append("_None._")
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"
