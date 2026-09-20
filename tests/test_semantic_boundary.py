from specgen.semantic import (
    QUESTION_SETS,
    evaluate_shadow,
    project_requirement_quality,
)


class FakeClient:
    def evaluate(self, *, state, questions):
        return {question.id: {"value": 0.5} for question in questions}


def test_semantic_question_sets_are_bounded_and_typed():
    assert set(QUESTION_SETS) == {
        "evidence.relevance/v1",
        "unresolved_issue.authority/v1",
        "requirement.quality/v1",
        "requirement.relationship/v1",
    }
    for questions in QUESTION_SETS.values():
        assert questions
        assert all(question.primitive in {"choice", "noul", "score"} for question in questions)
        assert all(question.instruction.strip() for question in questions)


def test_shadow_receipt_is_advisory_and_digest_bound():
    receipt = evaluate_shadow(FakeClient(), decision_id="requirement.quality/v1", state={"requirement": {"id": "REQ-1"}})
    assert receipt["advisory_only"] is True
    assert receipt["decision_id"] == "requirement.quality/v1"
    assert receipt["state_digest"].startswith("sha256:")
    assert receipt["questions_digest"].startswith("sha256:")


def test_requirement_projector_keeps_related_evidence_bounded():
    document = {
        "scope": {"protected": ["public API"]},
        "acceptance_criteria": [{"id": "AC-1", "requirement_ids": ["REQ-1"]}, {"id": "AC-2", "requirement_ids": ["REQ-2"]}],
        "evaluations": [{"id": "EV-1", "requirement_ids": ["REQ-1"]}],
    }
    state = project_requirement_quality(document, {"id": "REQ-1", "description": "Preserve API behavior"})
    assert [item["id"] for item in state["acceptance_criteria"]] == ["AC-1"]
    assert [item["id"] for item in state["evaluations"]] == ["EV-1"]
    assert state["protected_scope"] == ["public API"]
