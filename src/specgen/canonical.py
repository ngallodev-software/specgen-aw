from __future__ import annotations

import copy
import hashlib
import json
from typing import Any


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def canonical_bytes(value: Any) -> bytes:
    return canonical_json(value).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def snapshot_digest(spec: dict[str, Any]) -> str:
    normalized = copy.deepcopy(spec)
    snapshot = normalized.get("snapshot")
    if isinstance(snapshot, dict):
        snapshot.pop("content_digest", None)
    return digest(normalized)
