# ADR-0002: Agent-Workflow is a versioned target, not a core dependency

- Status: accepted
- Date: 2026-08-27

## Context

Agent-Workflow 0.9.0 exposes prompt-pack, evaluation-plan, source-baseline, task-result, logical-role, plugin, and stable public JSON seams directly relevant to generated implementation specifications. Coupling SpecGen to Agent-Workflow Python internals would prevent independent use and make both projects evolve in lockstep.

## Decision

SpecGen remains independently installable and authoritative for specification semantics. Agent-Workflow integration uses exact documented schema/public-JSON contracts through an isolated adapter. Compatibility is pinned and tested by target version/schema ID.

## Consequences

- Agent-Workflow installation is unnecessary for normal authoring/rendering.
- Unknown breaking Agent-Workflow contracts fail closed.
- Selected upstream schemas may be vendored as immutable compatibility fixtures.
- Agent-Workflow lifecycle/review/acceptance state is not reimplemented in SpecGen.
