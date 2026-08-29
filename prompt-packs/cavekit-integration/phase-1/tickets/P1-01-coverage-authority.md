# P1-01 — Criterion coverage and dependency authority

## Objective

Add criterion-level coverage and an acyclic task DAG using SpecGen’s existing
canonical schema discipline. Adapt Cavekit’s `agents/architect.md`,
`commands/map.md`, `internal/site/frontier.go:ReadyTasks`,
`internal/site/parser.go:Task`, and `internal/site/tracking.go` semantics.

## Required behavior

- Stable criterion IDs map requirements to task IDs, validation methods, receipts,
  and evidence.
- Unwaived criteria without task and validation owners fail planning/compilation.
- Dependencies are explicit IDs; cycles, unknown IDs, and impossible frontiers
  fail closed.
- Rendered coverage matrices are views only.

## Likely files

`schemas/spec/`, `src/specgen/canonical.py`, `src/specgen/elicitation.py`,
`src/specgen/compiler.py`, `src/specgen/agent_workflow.py`, and targeted tests.

## Do not do

Do not parse Cavekit Markdown as authority or change the v1alpha2 meaning
without an explicit schema decision and migration plan.

## Writable paths

Only ticket-scoped SpecGen source, schemas, tests, and completion evidence.

## Acceptance criteria

Schema and validator tests prove stable IDs, complete coverage, acyclic known
dependencies, and derived ready-frontier behavior.

## Stop conditions

Stop on a required v1alpha2 semantic change or any ambiguous legacy mapping.
