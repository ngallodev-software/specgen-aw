#!/usr/bin/env python3
"""Live qualification harness for SpecGen's optional TypeSafe SDK adapter.

Requires an intentional TYPESAFE_API_KEY and `pip install -e '.[typesafe]'`.
It never prints credentials or raw authorization material.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import time

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from specgen.semantic import QUESTION_SETS, evaluate_shadow, shadow_assessment
from specgen.semantic_config import configured_semantic_client, load_semantic_config


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def shape_check(decision_id: str, answers: dict) -> None:
    expected = {q.id: q.primitive for q in QUESTION_SETS[decision_id]}
    if set(answers) != set(expected):
        fail(f"{decision_id}: answer keys {sorted(answers)} != {sorted(expected)}")
    for key, primitive in expected.items():
        answer = answers[key]
        if answer.get("type") != primitive:
            fail(f"{decision_id}/{key}: expected {primitive}, got {answer.get('type')!r}")
        if primitive == "choice" and answer.get("choice") not in next(q for q in QUESTION_SETS[decision_id] if q.id == key).choices:
            fail(f"{decision_id}/{key}: invalid choice {answer.get('choice')!r}")
        if primitive == "noul" and not isinstance(answer.get("probability"), (int, float)):
            fail(f"{decision_id}/{key}: missing numeric probability")
        if primitive == "score" and not isinstance(answer.get("score"), (int, float)):
            fail(f"{decision_id}/{key}: missing numeric score")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--config", default=str(REPO / "config.toml"), help="configured SpecGen config.toml")
    p.add_argument("--output", default=str(REPO / "typesafe-live-receipt.json"))
    args = p.parse_args()

    if not os.environ.get("TYPESAFE_API_KEY"):
        fail("TYPESAFE_API_KEY is not set")
    config = load_semantic_config(args.config)
    if not config.enabled or config.provider != "typesafe" or config.mode != "shadow":
        fail("config must enable provider=typesafe in mode=shadow")

    started = time.time()
    client = configured_semantic_client(config)
    cases = {
        "evidence.relevance/v1": {
            "requirement": {"id": "REQ-LIVE", "description": "Preserve the public login endpoint behavior."},
            "candidate_evidence": {"path": "src/auth.py", "summary": "Defines the public login endpoint and status handling."},
        },
        "unresolved_issue.authority/v1": {
            "issue": {"id": "UQ-LIVE", "description": "Should the product add anonymous login?"},
            "repository_evidence": [],
        },
        "requirement.quality/v1": {
            "requirement": {"id": "REQ-LIVE", "description": "Preserve the public login endpoint behavior."},
            "acceptance_criteria": [{"id": "AC-LIVE", "description": "Existing login integration tests continue to pass."}],
            "evaluations": [{"id": "EV-LIVE", "command": "pytest tests/test_login.py"}],
            "protected_scope": ["public authentication API"],
        },
        "requirement.relationship/v1": {
            "left_requirement": {"id": "REQ-A", "description": "Preserve existing login response codes."},
            "right_requirement": {"id": "REQ-B", "description": "Return HTTP 200 for every failed login."},
            "protected_scope": ["public authentication API"],
        },
    }
    receipts = []
    for decision_id, state in cases.items():
        receipt = evaluate_shadow(client, decision_id=decision_id, state=state)
        shape_check(decision_id, receipt["answers"])
        receipts.append(receipt)
        print(f"PASS {decision_id}: {len(receipt['answers'])} typed answers")

    # Exercise the real sidecar composition over multiple calls.
    document = {
        "id": "SPEC-LIVE-QUALIFICATION",
        "snapshot": {"id": "SNAP-LIVE"},
        "scope": {"protected": ["public authentication API"]},
        "requirements": [
            {"id": "REQ-A", "description": "Preserve existing login response codes."},
            {"id": "REQ-B", "description": "Return HTTP 200 for every failed login."},
        ],
        "acceptance_criteria": [],
        "evaluations": [],
        "unresolved_questions": [{"id": "UQ-LIVE", "description": "Should anonymous login be added?"}],
    }
    assessment = shadow_assessment(document, client)
    if assessment.get("schema") != "specgen/semantic-assessment/v1alpha1" or assessment.get("advisory_only") is not True:
        fail("semantic sidecar authority/schema invariant failed")
    if not str(assessment.get("spec", {}).get("digest", "")).startswith("sha256:"):
        fail("semantic sidecar is not canonical-digest-bound")

    output = {
        "schema": "specgen/typesafe-live-qualification/v1",
        "ok": True,
        "provider": config.provider,
        "mode": config.mode,
        "model_override": config.model,
        "elapsed_seconds": round(time.time() - started, 3),
        "decision_receipts": receipts,
        "assessment": assessment,
    }
    out = Path(args.output)
    out.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS semantic sidecar: {len(assessment['receipts'])} receipts")
    print(f"WROTE {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
