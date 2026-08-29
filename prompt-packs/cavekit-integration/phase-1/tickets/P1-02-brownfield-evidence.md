# P1-02 — Brownfield evidence and parity proposals

## Objective

Implement the bounded four-stage brownfield adapter described in `SPEC.md`,
adapting Cavekit `skills/brownfield-adoption/SKILL.md`, `commands/sketch.md`,
`agents/drafter.md`, `agents/surveyor.md`, and `commands/scan.md`.

## Required behavior

- Read-only source inventory and immutable evidence references with hashes.
- Proposed domains, entry points, contracts, observed behaviors, gaps, and
  compatibility obligations remain separate from canonical spec data.
- Parity classifications are `observed`, `compatible`, `mismatch`, `missing`,
  `intentionally_changed`, or `unverified`, each with evidence and disposition.
- Promotion requires explicit approval and preserves authoring history.

## Likely files

`src/specgen/repository.py`, `src/specgen/brownfield.py`, `src/specgen/api.py`,
`src/specgen/cli.py`, `schemas/spec/`, `skills/specgen-brownfield/SKILL.md`,
and tests.

## Do not do

Do not claim semantic conclusions from filenames alone, write source files, or
make Cavekit a runtime dependency.

## Writable paths

Only ticket-scoped SpecGen source, schemas, tests, skills, and completion
evidence; analyzed repositories are read-only.

## Acceptance criteria

Fixtures prove evidence hashes, parity classifications, separation of observed
and desired behavior, and explicit approval before promotion.

## Stop conditions

Stop when source evidence is contradictory or a proposed promotion lacks an
authorized decision.
