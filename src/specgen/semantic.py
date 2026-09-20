"""Bounded semantic-assessment contracts for optional TypeSafe-style clients.

This module deliberately contains no TypeSafe SDK dependency.  It defines the
SpecGen-owned state/question/receipt boundary so an optional adapter can supply
typed semantic evidence without acquiring canonical-spec authority.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Literal, Protocol, Sequence

Primitive = Literal["choice", "noul", "score"]


@dataclass(frozen=True)
class SemanticQuestion:
    id: str
    primitive: Primitive
    instruction: str
    choices: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "id": self.id,
            "primitive": self.primitive,
            "instruction": self.instruction,
        }
        if self.choices:
            value["choices"] = list(self.choices)
        return value


class SemanticDecisionClient(Protocol):
    """Adapter boundary implemented by an optional semantic-decision provider."""

    def evaluate(
        self,
        *,
        state: dict[str, Any],
        questions: Sequence[SemanticQuestion],
    ) -> dict[str, Any]: ...


QUESTION_SETS: dict[str, tuple[SemanticQuestion, ...]] = {
    "evidence.relevance/v1": (
        SemanticQuestion(
            "relevance",
            "score",
            "Score how relevant the candidate repository evidence is to understanding the supplied requirement on an ordered 0-to-1 scale, where 0 means unrelated and 1 means directly material.",
        ),
        SemanticQuestion(
            "materially_supports_requirement",
            "noul",
            "Estimate the probability that the candidate repository evidence materially supports a factual claim needed to understand the supplied requirement. Do not treat mere connectivity or keyword overlap as support.",
        ),
    ),
    "unresolved_issue.authority/v1": (
        SemanticQuestion(
            "resolution_source",
            "choice",
            "Choose the source that should resolve the supplied unresolved issue. Repository evidence may explain existing behavior but cannot authorize a new product decision.",
            ("repository_answerable", "user_decision", "external_research", "already_supported", "unclear"),
        ),
    ),
    "requirement.quality/v1": (
        SemanticQuestion("specificity", "score", "Score how specifically the requirement describes the behavior or constraint it intends to establish."),
        SemanticQuestion("testability", "score", "Score how directly the requirement can be verified from the supplied acceptance and evaluation evidence."),
        SemanticQuestion("scope_clarity", "score", "Score how clearly the requirement's intended scope and boundaries are expressed."),
        SemanticQuestion("evidence_support", "score", "Score how strongly the supplied cited evidence supports the requirement's claims about the existing system."),
        SemanticQuestion("compatibility_coverage", "score", "Score how clearly relevant preservation or compatibility obligations are represented for this requirement."),
        SemanticQuestion("materially_ambiguous", "noul", "Estimate the probability that the requirement has material ambiguity that could lead competent implementers to different observable behavior."),
        SemanticQuestion("contains_hidden_decision", "noul", "Estimate the probability that implementing the requirement requires an unstated user, product, policy, or compatibility decision."),
    ),
    "requirement.relationship/v1": (
        SemanticQuestion("semantically_equivalent", "noul", "Estimate the probability that the two supplied requirements express materially equivalent obligations."),
        SemanticQuestion("materially_overlapping", "noul", "Estimate the probability that the two supplied requirements materially overlap even if they are not equivalent."),
        SemanticQuestion("contradictory", "noul", "Estimate the probability that satisfying both supplied requirements as written creates a semantic contradiction."),
        SemanticQuestion("preservation_tension", "noul", "Estimate the probability that the two supplied requirements create tension between requested change and preservation or compatibility obligations."),
    ),
}


def _canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def project_requirement_quality(document: dict[str, Any], requirement: dict[str, Any]) -> dict[str, Any]:
    rid = requirement["id"]
    acceptance = [item for item in document.get("acceptance_criteria", []) if rid in item.get("requirement_ids", [])]
    evaluations = [item for item in document.get("evaluations", []) if rid in item.get("requirement_ids", [])]
    protected = list(document.get("scope", {}).get("protected", []))
    return {
        "requirement": requirement,
        "acceptance_criteria": acceptance,
        "evaluations": evaluations,
        "protected_scope": protected,
    }


def project_unresolved_issue(issue: dict[str, Any], *, evidence_refs: Sequence[dict[str, Any]] = ()) -> dict[str, Any]:
    return {"issue": issue, "repository_evidence": list(evidence_refs)}


def project_evidence_relevance(requirement: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    return {"requirement": requirement, "candidate_evidence": evidence}


def project_requirement_relationship(left: dict[str, Any], right: dict[str, Any], *, protected_scope: Sequence[str] = ()) -> dict[str, Any]:
    return {"left_requirement": left, "right_requirement": right, "protected_scope": list(protected_scope)}


def evaluate_shadow(
    client: SemanticDecisionClient,
    *,
    decision_id: str,
    state: dict[str, Any],
) -> dict[str, Any]:
    """Collect advisory semantic evidence without applying business policy."""
    questions = QUESTION_SETS[decision_id]
    response = client.evaluate(state=state, questions=questions)
    return {
        "schema": "specgen/semantic-decision-receipt/v1alpha1",
        "decision_id": decision_id,
        "question_set_version": decision_id.rsplit("/", 1)[-1],
        "state_digest": _canonical_hash(state),
        "questions_digest": _canonical_hash([item.as_dict() for item in questions]),
        "advisory_only": True,
        "answers": response,
    }


def shadow_assessment(
    document: dict[str, Any],
    client: SemanticDecisionClient,
) -> dict[str, Any]:
    """Evaluate the initial bounded question sets for a canonical document.

    The returned sidecar is derived advisory evidence. It is never read by
    validation/finalization and therefore cannot change canonical authority.
    """
    receipts: list[dict[str, Any]] = []
    requirements = [
        item for item in document.get("requirements", [])
        if item.get("lifecycle", "active") == "active"
    ]
    protected_scope = list(document.get("scope", {}).get("protected", []))

    for requirement in requirements:
        receipts.append(evaluate_shadow(
            client,
            decision_id="requirement.quality/v1",
            state=project_requirement_quality(document, requirement),
        ))

    for index, left in enumerate(requirements):
        for right in requirements[index + 1:]:
            receipts.append(evaluate_shadow(
                client,
                decision_id="requirement.relationship/v1",
                state=project_requirement_relationship(left, right, protected_scope=protected_scope),
            ))

    for issue in document.get("unresolved_questions", []):
        if issue.get("lifecycle", "active") == "active":
            receipts.append(evaluate_shadow(
                client,
                decision_id="unresolved_issue.authority/v1",
                state=project_unresolved_issue(issue),
            ))

    return {
        "schema": "specgen/semantic-assessment/v1alpha1",
        "spec": {
            "id": document["id"],
            "snapshot_id": document["snapshot"]["id"],
            "digest": _canonical_hash(document),
        },
        "mode": "shadow",
        "advisory_only": True,
        "receipts": receipts,
    }
