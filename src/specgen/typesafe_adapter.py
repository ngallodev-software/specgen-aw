"""Optional official TypeSafe SDK adapter for SpecGen semantic shadow decisions."""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from .semantic import SemanticQuestion


def _load_sdk():
    try:
        from typesafe_sdk import Choice, Noul, Score, TypeSafeClient
    except ImportError as exc:
        raise RuntimeError(
            "typesafe_sdk_unavailable; install SpecGen with the 'typesafe' extra"
        ) from exc
    return Choice, Noul, Score, TypeSafeClient


def _typesafe_questions(questions: Sequence[SemanticQuestion], *, sdk=None) -> dict[str, object]:
    """Lower bounded SpecGen questions to official SDK primitive objects."""
    Choice, Noul, Score, _ = sdk or _load_sdk()
    result: dict[str, object] = {}
    for question in questions:
        if question.primitive == "choice":
            result[question.id] = Choice(
                instructions=question.instruction,
                criteria={choice: None for choice in question.choices},
            )
        elif question.primitive == "noul":
            result[question.id] = Noul(instructions=question.instruction)
        elif question.primitive == "score":
            result[question.id] = Score(
                instructions=question.instruction,
                criteria=["0.0: absent or unsupported", "0.5: mixed or partial", "1.0: strong or direct"],
            )
        else:  # pragma: no cover
            raise ValueError(f"unsupported semantic primitive: {question.primitive}")
    return result


def _number(value: Any) -> float | int | None:
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def _normalize_response(response: Any) -> dict[str, object]:
    answers = getattr(response, "answers", None)
    if not isinstance(answers, Mapping):
        raise ValueError("TypeSafe response has no answer mapping")
    normalized: dict[str, object] = {}
    for name, answer in answers.items():
        probabilities = getattr(answer, "probabilities", None)
        confidence = _number(getattr(answer, "confidence", None))
        if hasattr(answer, "choice"):
            item: dict[str, object] = {"type": "choice", "choice": getattr(answer, "choice")}
            if confidence is not None:
                item["confidence"] = confidence
            if isinstance(probabilities, Mapping):
                item["probabilities"] = {str(k): v for k, v in probabilities.items()}
            normalized[str(name)] = item
        elif hasattr(answer, "noul") or hasattr(answer, "probability"):
            probability = getattr(answer, "noul", getattr(answer, "probability", None))
            if _number(probability) is None:
                raise ValueError(f"TypeSafe Noul answer {name!r} has no numeric probability")
            normalized[str(name)] = {"type": "noul", "probability": probability}
        elif hasattr(answer, "score"):
            score = getattr(answer, "score")
            if _number(score) is None:
                raise ValueError(f"TypeSafe Score answer {name!r} has no numeric score")
            item = {"type": "score", "score": score}
            if confidence is not None:
                item["confidence"] = confidence
            if isinstance(probabilities, Mapping):
                item["probabilities"] = {str(k): v for k, v in probabilities.items()}
            normalized[str(name)] = item
        else:
            raise ValueError(f"TypeSafe response has unsupported answer type for {name!r}")
    return normalized


class TypeSafeSemanticDecisionClient:
    """SemanticDecisionClient backed by the optional official ``typesafe-sdk`` package."""

    def __init__(self, *, model: str | None = None) -> None:
        # Verify availability at construction, but do not create a network client yet.
        self._sdk = _load_sdk()
        self._model = model

    def evaluate(self, *, state: dict[str, Any], questions: Sequence[SemanticQuestion]) -> dict[str, Any]:
        _, _, _, TypeSafeClient = self._sdk
        kwargs: dict[str, Any] = {
            "state": state,
            "questions": _typesafe_questions(questions, sdk=self._sdk),
        }
        if self._model is not None:
            kwargs["model"] = self._model
        # Scope transport resources to one request and rely on the SDK for transport-level retries.
        with TypeSafeClient() as client:
            response = client.system_one(**kwargs)
        return dict(_normalize_response(response))
