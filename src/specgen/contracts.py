from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


CONTRACT_PATHS: dict[str, str] = {
    "specgen/spec/v1alpha1": "schemas/spec/v1alpha1.schema.json",
    "specgen/spec/v1alpha2": "schemas/spec/v1alpha2.schema.json",
    "specgen/authoring-event/v1alpha1": "schemas/spec/authoring-event-v1alpha1.schema.json",
    "specgen/compat/agent-workflow/v1alpha1": "schemas/compat/agent-workflow-v1alpha1.schema.json",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def known_contracts() -> tuple[str, ...]:
    return tuple(sorted(CONTRACT_PATHS))


def contract_path(contract_id: str) -> Path:
    try:
        relative = CONTRACT_PATHS[contract_id]
    except KeyError as exc:
        raise ValueError(f"unsupported contract: {contract_id}") from exc
    return repo_root() / relative


@lru_cache(maxsize=None)
def load_contract(contract_id: str) -> dict[str, Any]:
    path = contract_path(contract_id)
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("$id") != contract_id:
        raise ValueError(f"contract id mismatch in {path}: {value.get('$id')!r}")
    return value
