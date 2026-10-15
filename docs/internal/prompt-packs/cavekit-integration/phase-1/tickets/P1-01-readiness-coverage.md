# P1-01 — Strengthen readiness using existing coverage relationships

## Objective

Adopt the useful part of CaveKit's coverage discipline without introducing a
parallel criterion or runtime tracking model.

## Required behavior

- Treat `acceptance_criteria` as the sole criterion authority.
- In `agent-workflow` mode, an active requirement without an observable
  acceptance criterion is a readiness blocker.
- Requirement evaluation coverage recognizes either a direct evaluation link or
  an evaluation linked through one of the requirement's acceptance criteria.
- Preserve existing task requirement coverage and task dependency validation.
- Preserve existing cycle/unknown-dependency failures.
- Do not calculate or persist runtime ready-frontier/completion state.
- Do not add task owners, receipts, waivers, or execution statuses to canonical
  SpecGen merely for coverage reporting.

## Likely files

`src/specgen/elicitation.py` and the smallest existing critical-seam/integration
coverage needed to protect the changed readiness behavior. Touch schemas only if
a genuine public-contract change is unavoidable; stop before doing so without an
explicit versioning decision.

## Writable paths

Write only the smallest implementation, test, and maintained-documentation
paths needed for this behavior. Do not edit generated archives or unrelated
repositories.

## Tests

Run the focused readiness/critical-seam tests and the repository release checks
with bounded timeouts. Record the exact commands and results.

## Stop conditions

Stop for a schema/version change, a new lifecycle authority, or any request to
persist runtime frontier state; report the decision required instead.

## Acceptance

A canonical specification that has requirement/task/evaluation structure but no
observable acceptance is not Agent-Workflow-ready. An evaluation linked through
an acceptance criterion correctly satisfies evaluation coverage for the linked
requirement. Existing valid Agent-Workflow-ready specs remain valid unless they
were relying on missing acceptance.

## Non-goals

No coverage ledger, criterion schema, ready frontier, runtime task status,
receipt model, or new execution lifecycle.
