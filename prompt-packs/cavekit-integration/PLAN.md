# Implementation Plan

## Phase 0 — Baseline and contract

Record the exact SpecGen and Agent-Workflow revisions, current schemas, test
authority, installed compatibility snapshot, and Cavekit evidence paths. Do not
modify production files.

## Phase 1 — Typed authority

Implement and validate first-class criterion/task coverage and dependency DAG
records; add read-only brownfield evidence and parity proposals; add review,
gate-receipt, and waiver contracts. Keep all proposal-to-canonical promotion
explicit.

## Phase 2 — Integration and projections

Expose the smallest API/CLI surface through existing `src/specgen/api.py`,
`src/specgen/cli.py`, `src/specgen/repository.py`, and
`src/specgen/agent_workflow.py`. Render coverage, parity, review, and gate
reports from structured authority. Update `skills/specgen/SKILL.md` and
`skills/specgen-brownfield/SKILL.md` only to describe implemented behavior.

## Phase 3 — Verification and acceptance

Run schema, unit, CLI, critical-seam, packaging, and Agent-Workflow compilation
checks. Perform an independent review against every invariant. Verify that
unresolved blockers require valid waivers and that no Cavekit runtime or
Markdown-parser dependency entered the project.

## Stop conditions

Stop and request a decision when a field would change `specgen/spec/v1alpha2`,
when observed behavior conflicts with desired behavior without a decision, when
the Agent-Workflow target contract would change, or when a proposed waiver lacks
an accountable approver or expiry.
