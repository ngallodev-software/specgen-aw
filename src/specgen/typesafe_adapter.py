"""Optional official TypeSafe SDK adapter for SpecGen semantic shadow decisions.

Importing this module performs no network activity and does not require the SDK.
The SDK is imported only when ``TypeSafeSemanticDecisionClient`` is constructed.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from .semantic import SemanticQuestion


def _typesafe_questions(questions: Sequence[SemanticQuestion]) -> dict[str, object]:
    """Lower SpecGen's bounded question contract to TypeSafe system_one input."""
    result: dict[str, object] = {}
    for question in questions:
        if question.primitive == "choice":
            result[question.id] = {
                "type": "choice",
                "question": question.instruction,
                "choices": list(question.choices),
            }
        elif question.primitive == "noul":
            result[question.id] = {
                "type": "noul",
                "question": question.instruction,
            }
        elif question.primitive == "score":
            result[question.id] = {
                "type": "score",
                "question": question.instruction,
                "min": 0.0,
                "max": 1.0,
            }
        else:  # pragma: no cover - SemanticQuestion constrains this already.
            raise ValueError(f"unsupported semantic primitive: {question.primitive}")
    return result


def _normalize_response(response: Any) -> dict[str, object]:
    answers = getattr(response, "answers", None)
    if not isinstance(answers, Mapping):
        raise ValueError("TypeSafe response has no answer mapping")

    normalized: dict[str, object] = {}
    for name, answer in answers.items():
        if hasattr(answer, "choice"):
            normalized[str(name)] = {
                "type": "choice",
                "choice": answer.choice,
                "confidence": answer.confidence,
                "probabilities": dict(answer.probabilities),
            }
        elif hasattr(answer, "noul"):
            normalized[str(name)] = {"type": "noul", "probability": answer.noul}
        elif hasattr(answer, "score"):
            normalized[str(name)] = {
                "type": "score",
                "score": answer.score,
                "confidence": answer.confidence,
                "probabilities": {str(key): value for key, value in answer.probabilities.items()},
            }
        else:
            raise ValueError("TypeSafe response has unsupported answer type")
    return normalized


class TypeSafeSemanticDecisionClient:
    """SemanticDecisionClient backed by the official ``typesafe-sdk`` package."""

    def __init__(self, *, model: str | None = None) -> None:
        try:
            from typesafe_sdk import TypeSafeClient
        except ImportError as exc:
            raise RuntimeError(
                "typesafe_sdk_unavailable; install SpecGen with the 'typesafe' extra"
            ) from exc
        self._client = TypeSafeClient()
        self._model = model

    def evaluate(
        self,
        *,
        state: dict[str, Any],
        questions: Sequence[SemanticQuestion],
    ) -> dict[str, Any]:
        response = self._client.system_one(
            state=state,
            questions=_typesafe_questions(questions),
            model=self._model,
        )
        return dict(_normalize_response(response))
