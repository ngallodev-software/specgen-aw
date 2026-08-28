"""Stable programmatic surface for SpecGen application and host integrations.

The API composes existing SpecGen authorities; it does not introduce a second
model, persistence layer, or execution lifecycle.
"""

from .agent_workflow import compile_target as compile_agent_workflow_target
from .agent_workflow import write_target as write_agent_workflow_target
from .application import create_candidate, load_document, record_event, write_document
from .canonical import snapshot_digest
from .compiler import finalize_candidate
from .contracts import agent_workflow_compatibility, known_contracts
from .diff import semantic_delta
from .drift import repository_drift
from .elicitation import assess
from .evals import evaluation_intent
from .history import append_event
from .modes import mode_descriptions, mode_names
from .render import render_markdown
from .repository import analyze_repository
from .validate import validate

__all__ = (
    "agent_workflow_compatibility",
    "analyze_repository",
    "append_event",
    "assess",
    "compile_agent_workflow_target",
    "evaluation_intent",
    "finalize_candidate",
    "known_contracts",
    "mode_descriptions",
    "mode_names",
    "render_markdown",
    "repository_drift",
    "semantic_delta",
    "snapshot_digest",
    "validate",
    "write_agent_workflow_target",
    "create_candidate",
    "load_document",
    "record_event",
    "write_document",
)
