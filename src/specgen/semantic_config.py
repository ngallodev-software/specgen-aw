"""Configuration for optional semantic-decision providers."""
from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import tomllib
from typing import Any


@dataclass(frozen=True)
class SemanticConfig:
    enabled: bool = False
    provider: str = "typesafe"
    mode: str = "shadow"
    model: str | None = None


def _candidate_paths(explicit: str | Path | None) -> list[Path]:
    if explicit is not None:
        return [Path(explicit)]
    env = os.environ.get("SPECGEN_CONFIG")
    if env:
        return [Path(env)]
    return [Path("config.toml"), Path.home() / ".config" / "specgen" / "config.toml"]


def load_semantic_config(path: str | Path | None = None) -> SemanticConfig:
    """Load optional semantic configuration without requiring TypeSafe to be installed."""
    selected = next((p for p in _candidate_paths(path) if p.is_file()), None)
    if selected is None:
        return SemanticConfig()
    with selected.open("rb") as handle:
        raw: dict[str, Any] = tomllib.load(handle)
    semantic = raw.get("semantic", {})
    if not isinstance(semantic, dict):
        raise ValueError("[semantic] must be a TOML table")
    provider = str(semantic.get("provider", "typesafe"))
    mode = str(semantic.get("mode", "shadow"))
    if provider != "typesafe":
        raise ValueError(f"unsupported semantic provider: {provider!r}")
    if mode != "shadow":
        raise ValueError("only semantic mode 'shadow' is currently supported")
    provider_cfg = semantic.get("typesafe", {})
    if not isinstance(provider_cfg, dict):
        raise ValueError("[semantic.typesafe] must be a TOML table")
    model = provider_cfg.get("model")
    return SemanticConfig(
        enabled=bool(semantic.get("enabled", False)),
        provider=provider,
        mode=mode,
        model=str(model) if model is not None else None,
    )


def configured_semantic_client(config: SemanticConfig):
    """Construct the configured provider lazily; deterministic paths never import its SDK."""
    if not config.enabled:
        raise RuntimeError("semantic_decisions_disabled")
    if config.provider != "typesafe":
        raise RuntimeError(f"unsupported_semantic_provider:{config.provider}")
    from .typesafe_adapter import TypeSafeSemanticDecisionClient
    return TypeSafeSemanticDecisionClient(model=config.model)
