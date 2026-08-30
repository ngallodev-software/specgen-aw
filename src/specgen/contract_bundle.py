"""Narrow adapter to the separately released shared contract bundle.

SpecGen owns canonical authoring and compilation.  The bundle owns the native
Agent-Workflow schema bytes and their validation/digest semantics.
"""

from __future__ import annotations

from typing import Any

from specgen_contracts import BUNDLE_VERSION, validate as bundle_validate
from specgen_contracts.bundle import schema_digest


def validate(schema_id: str, document: Any) -> list[dict[str, Any]]:
    """Return bundle diagnostics for a native Agent-Workflow artifact."""

    return bundle_validate(schema_id, document)


def require(schema_id: str) -> tuple[str, str]:
    """Return the exact bundle and schema digest declarations for an artifact."""

    return BUNDLE_VERSION, schema_digest(schema_id)
