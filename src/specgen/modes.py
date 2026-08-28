from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AuthoringMode:
    name: str
    description: str
    strict: bool = False
    agent_workflow: bool = False


_MODES = {
    "express": AuthoringMode(
        "express",
        "Ask only questions required to produce a valid canonical snapshot.",
    ),
    "guided": AuthoringMode(
        "guided",
        "Surface important ambiguity, verification, and implementation gaps without blocking drafts.",
    ),
    "strict": AuthoringMode(
        "strict",
        "Require unresolved ambiguity and verification gaps to be resolved before finalization.",
        strict=True,
    ),
    "agent-workflow": AuthoringMode(
        "agent-workflow",
        "Strict, phased implementation authoring shaped for later Agent-Workflow prompt-pack and evaluation-plan compilation.",
        strict=True,
        agent_workflow=True,
    ),
}


def mode(name: str) -> AuthoringMode:
    try:
        return _MODES[name]
    except KeyError as exc:
        raise ValueError(f"unknown authoring mode: {name}") from exc


def mode_names() -> tuple[str, ...]:
    return tuple(_MODES)


def mode_descriptions() -> dict[str, str]:
    return {name: value.description for name, value in _MODES.items()}
