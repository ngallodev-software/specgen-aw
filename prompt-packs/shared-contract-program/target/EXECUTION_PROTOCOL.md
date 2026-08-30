# Execution protocol

Agent-Workflow owns execution state, worktrees, completion collection, review, and acceptance.

1. Validate the prompt pack with the Agent-Workflow 0.9.1 public pack interface.
2. Honor task dependencies and task-local writable/acceptance/test/stop guardrails.
3. Treat result-contract schemas as required structured handoff contracts.
4. Treat hidden/external oracle material as opaque and use only the digest-bound target reference.
5. Never edit generated target artifacts to redefine canonical SpecGen requirements.
