# Phase PHASE-002 implementation prompt

Run in parallel after the bundle is independently reviewed; DAG permits but does not force concurrency.

Execute only the declared tasks and dependencies in `pack.yaml`.

## Task order / dependencies
- `TASK-003` depends on `TASK-002`.
- `TASK-004` depends on `TASK-002`.

Agent-Workflow owns execution, worktrees, review, completion, and acceptance state.
