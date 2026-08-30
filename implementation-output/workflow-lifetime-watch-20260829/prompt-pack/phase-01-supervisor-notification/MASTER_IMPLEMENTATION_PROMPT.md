# Phase PHASE-001 implementation prompt

Shared watcher notification

Execute only the declared tasks and dependencies in `pack.yaml`.

## Task order / dependencies
- `TASK-001` depends on nothing.
- `TASK-002` depends on `TASK-001`.

Agent-Workflow owns execution, worktrees, review, completion, and acceptance state.
