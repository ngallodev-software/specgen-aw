from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from .canonical import canonical_json
from .validate import validate


def load_events(path: str | Path) -> tuple[dict[str, Any], ...]:
    log = Path(path)
    if not log.exists():
        return ()
    events: list[dict[str, Any]] = []
    for number, line in enumerate(log.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"event log line {number} is not a JSON object")
        result = validate(value)
        if not result.valid:
            raise ValueError(f"event log line {number} fails validation")
        events.append(value)
    return tuple(events)


def append_event(path: str | Path, event: dict[str, Any]) -> None:
    result = validate(event)
    if not result.valid:
        raise ValueError("authoring event fails validation")

    events = load_events(path)
    if events:
        spec_id = events[0]["spec_id"]
        if event["spec_id"] != spec_id:
            raise ValueError(f"event spec_id {event['spec_id']!r} does not match log spec_id {spec_id!r}")
        expected = events[-1]["sequence"] + 1
        if event["sequence"] != expected:
            raise ValueError(f"event sequence must be {expected}, got {event['sequence']}")
        ids = {item["id"] for item in events}
        if event["id"] in ids:
            raise ValueError(f"duplicate authoring event id {event['id']!r}")
        for superseded in event.get("supersedes_event_ids", []):
            if superseded not in ids:
                raise ValueError(f"cannot supersede unknown event {superseded!r}")
    elif event["sequence"] != 1:
        raise ValueError("first authoring event sequence must be 1")

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = (canonical_json(event) + "\n").encode("utf-8")
    fd = os.open(target, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o644)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)
