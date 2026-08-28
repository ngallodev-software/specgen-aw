from __future__ import annotations

from copy import deepcopy
from typing import Any

from .canonical import snapshot_digest
from .elicitation import assess
from .validate import validate


def finalize_candidate(document: dict[str, Any], mode_name: str = "guided") -> dict[str, Any]:
    candidate = deepcopy(document)
    snapshot = candidate.setdefault("snapshot", {})
    snapshot.pop("content_digest", None)

    validation = validate(candidate)
    if not validation.valid:
        raise ValueError("candidate does not satisfy the canonical contract")

    plan = assess(candidate, mode_name)
    if not plan["ready"]:
        raise ValueError(
            f"candidate is not ready in {mode_name} mode: {plan['blocker_count']} blocker(s)"
        )

    snapshot["content_digest"] = snapshot_digest(candidate)
    final_validation = validate(candidate)
    if not final_validation.valid:
        raise ValueError("finalized candidate failed canonical validation")
    return candidate
