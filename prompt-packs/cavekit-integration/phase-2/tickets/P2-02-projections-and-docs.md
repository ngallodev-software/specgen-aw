# P2-02 — Deterministic projections and documentation

## Objective

Render coverage matrices, parity reports, review findings, gate receipts, and
waiver status from structured records. Update `README.md`, `docs/USAGE.md`,
`docs/AGENT_WORKFLOW_INTEGRATION.md`, `docs/VERSIONING.md`, and both SpecGen
skills to document only verified behavior.

## Required checks

Round-trip/projection tests must prove rendered Markdown cannot change authority
without validated import. Include explicit Cavekit attribution as methodology
reference, not dependency or copied runtime.

## Writable paths

Only ticket-scoped projections, documentation, skills, tests, and completion
evidence.

## Acceptance criteria

Projection tests prove deterministic output and documentation matches the
implemented CLI/API behavior.

## Stop conditions

Stop if a document claims an unimplemented capability or treats Markdown as
authority.
