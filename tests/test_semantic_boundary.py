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


def test_shadow_assessment_collects_quality_relationship_and_authority_receipts():
    from specgen.semantic import shadow_assessment

    document = {
        "id": "SPEC-1",
        "snapshot": {"id": "SNAP-1"},
        "scope": {"protected": ["public API"]},
        "requirements": [
            {"id": "REQ-1", "description": "Preserve API"},
            {"id": "REQ-2", "description": "Add command"},
        ],
        "acceptance_criteria": [],
        "evaluations": [],
        "unresolved_questions": [{"id": "UQ-1", "description": "Choose compatibility policy"}],
    }
    result = shadow_assessment(document, FakeClient())
    assert result["schema"] == "specgen/semantic-assessment/v1alpha1"
    assert result["advisory_only"] is True
    assert [r["decision_id"] for r in result["receipts"]] == [
        "requirement.quality/v1",
        "requirement.quality/v1",
        "requirement.relationship/v1",
        "unresolved_issue.authority/v1",
    ]


def test_typesafe_adapter_lowers_questions_and_normalizes_answers(monkeypatch):
    import sys
    import types
    from specgen.semantic import QUESTION_SETS
    from specgen.typesafe_adapter import TypeSafeSemanticDecisionClient

    class Answer:
        score = 0.75
        confidence = 0.8
        probabilities = {0.0: 0.1, 1.0: 0.9}

    class Response:
        answers = {"specificity": Answer()}

    class Client:
        def system_one(self, *, state, questions, model=None):
            assert questions["specificity"]["type"] == "score"
            assert model == "test-model"
            return Response()

    module = types.SimpleNamespace(TypeSafeClient=Client)
    monkeypatch.setitem(sys.modules, "typesafe_sdk", module)
    client = TypeSafeSemanticDecisionClient(model="test-model")
    answers = client.evaluate(state={"x": 1}, questions=QUESTION_SETS["requirement.quality/v1"][:1])
    assert answers["specificity"]["type"] == "score"
    assert answers["specificity"]["score"] == 0.75
