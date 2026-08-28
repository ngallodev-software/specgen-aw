# ADR-0006 — Authoring modes are policy profiles; Agent-Workflow is an opinionated profile

> Document version: 0.1.5 · Applies to SpecGen 0.1.5

- Status: accepted
- Date: 2026-08-27

## Decision

SpecGen authoring uses named policy profiles rather than separate canonical schemas. Initial modes are `express`, `guided`, `strict`, and `agent-workflow`.

`agent-workflow` is intentionally opinionated. It requires phased implementation structure, task-to-requirement coverage, structured task result contracts, requirement-level evaluation intent, and resolution of open ambiguity before finalization. It prepares a portable canonical snapshot for later lowering into pinned Agent-Workflow public contracts; it does not embed Agent-Workflow runtime state into the canonical spec.

Mode output is versioned as `specgen/elicitation-plan/v1alpha1`.

## Rationale

Authoring modes change how aggressively SpecGen asks questions and what completeness guardrails block finalization. They do not change specification meaning. Keeping policy outside `specgen/spec/v1alpha2` preserves portability and avoids an Agent-Workflow-shaped core model.

The Agent-Workflow profile exists because prompt-pack/phased implementation handoff benefits from earlier, stricter shaping than generic specification authoring.

## Consequences

- A snapshot may be valid under the canonical schema but not ready under a strict authoring mode.
- Mode-specific guardrails must be deterministic and inspectable.
- Future Agent-Workflow adapter work must consume the canonical snapshot and pinned public contracts, not mode-private runtime state.
- Adding a mode is a public authoring-policy change and must update the elicitation-plan contract if its name is serialized.
