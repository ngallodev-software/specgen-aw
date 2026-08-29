# P2-01 — API and CLI integration

## Objective

Expose the new authorities through the existing SpecGen facade and CLI without
creating a second model. Preserve `specgen repo analyze`, `brownfield plan`,
`author assess/finalize`, and Agent-Workflow compile behavior.

## Required checks

Run `specgen contracts`, `specgen modes`, schema validation, brownfield analysis,
parity proposal, coverage assessment, and Agent-Workflow compilation fixtures.
Update only documented, implemented surfaces.

## Writable paths

Only ticket-scoped `src/specgen/`, `schemas/`, and tests.

## Acceptance criteria

Existing commands retain behavior while the new typed authorities are reachable
through the supported API/CLI and reject invalid or unapproved transitions.

## Stop conditions

Stop if integration requires a second canonical model or breaks existing
v1alpha2/Agent-Workflow contracts.
