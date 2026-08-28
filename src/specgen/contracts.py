from __future__ import annotations

import json
from functools import lru_cache
from importlib.metadata import PackageNotFoundError, distribution
from pathlib import Path
from typing import Any


CONTRACT_PATHS: dict[str, str] = {
    "specgen/spec/v1alpha1": "schemas/spec/v1alpha1.schema.json",
    "specgen/spec/v1alpha2": "schemas/spec/v1alpha2.schema.json",
    "specgen/authoring-event/v1alpha1": "schemas/spec/authoring-event-v1alpha1.schema.json",
    "specgen/semantic-delta/v1alpha1": "schemas/spec/semantic-delta-v1alpha1.schema.json",
    "specgen/elicitation-plan/v1alpha1": "schemas/spec/elicitation-plan-v1alpha1.schema.json",
    "specgen/repository-analysis/v1alpha1": "schemas/spec/repository-analysis-v1alpha1.schema.json",
    "specgen/repository-drift/v1alpha1": "schemas/spec/repository-drift-v1alpha1.schema.json",
    "specgen/evaluation-intent/v1alpha1": "schemas/spec/evaluation-intent-v1alpha1.schema.json",
    "specgen/agent-workflow-compatibility/v1alpha1": "schemas/compat/agent-workflow-v1alpha1.schema.json",
}


@lru_cache(maxsize=1)
def repo_root() -> Path:
    """Locate canonical runtime assets in a source checkout or installed distribution."""

    source = Path(__file__).resolve().parents[2]
    if (source / "schemas" / "spec" / "v1alpha2.schema.json").is_file():
        return source
    try:
        dist = distribution("specgen")
    except PackageNotFoundError as exc:
        raise RuntimeError("cannot locate SpecGen runtime contract assets") from exc
    for entry in dist.files or ():
        candidate = Path(dist.locate_file(entry)).resolve()
        if (
            candidate.name == "v1alpha2.schema.json"
            and candidate.parent.name == "spec"
            and candidate.parent.parent.name == "schemas"
            and candidate.parent.parent.parent.name == "specgen"
        ):
            installed = candidate.parents[2]
            if (installed / "compat" / "agent-workflow" / "compatibility.json").is_file():
                return installed
    raise RuntimeError("installed SpecGen distribution is missing runtime contract assets")


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


@lru_cache(maxsize=1)
def agent_workflow_compatibility() -> dict[str, Any]:
    path = repo_root() / "compat" / "agent-workflow" / "compatibility.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema") != "specgen/agent-workflow-compatibility/v1alpha1":
        raise ValueError(f"unexpected Agent-Workflow compatibility contract in {path}")
    return value
