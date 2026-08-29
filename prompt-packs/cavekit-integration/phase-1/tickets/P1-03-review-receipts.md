# P1-03 — Review, validation, waiver, and receipt authority

## Objective

Adapt Cavekit’s `scripts/codex-design-challenge.sh`, `scripts/codex-review.sh`,
`scripts/codex-gate.sh`, `scripts/codex-findings.sh`,
`references/validation-gates.md`, and `commands/revise.md` into typed,
append-only SpecGen/Agent-Workflow-compatible contracts.

## Required behavior

- Keep technical, review, acceptance, and release gates distinct.
- Emit receipts for pass, fail, skipped, unavailable, degraded, and override.
- Blocking findings stop progression; cycle exhaustion cannot silently advance.
- Waivers require approver, scope, reason, risk, expiry, affected IDs, and a
  receipt.
- Revision maps finding/evidence to canonical authoring events.

## Do not do

Do not copy Markdown ledgers, shell exit codes, PID state, or Cavekit’s implicit
continue behavior as authority.

## Writable paths

Only ticket-scoped SpecGen source, schemas, tests, and completion evidence.

## Acceptance criteria

Fixtures prove separate gate statuses, append-only receipts, blocking findings,
and fully specified waivers.

## Tests

Run schema, receipt, waiver, and blocking-gate regression tests.
