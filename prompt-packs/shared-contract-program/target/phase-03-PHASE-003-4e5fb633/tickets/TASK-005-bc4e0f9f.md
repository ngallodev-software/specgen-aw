# Prove migration and cross-product conformance

- Task ID: `TASK-005`
- Tier: `implementation`
- Target application: `agent-workflow-spec-contracts`
- Logical role hint: `review`
- Dependencies: `TASK-003`, `TASK-004`

## Authorized requirements
- `REQ-002` — SpecGen-generated native targets declare exact bundle version and digest; Agent-Workflow rejects a mismatch before execution.
- `REQ-003` — Every supported shared-artifact version transition has deterministic validated migration that emits provenance-linked derived artifacts and fails closed when meaning cannot be preserved.
- `REQ-004` — SpecGen retains canonical authoring and compilation; Agent-Workflow retains runtime interpretation, scheduling, execution, evaluation, review, and sealing.

## Acceptance
- `AC-002` — An exact producer/consumer bundle match is accepted and version or digest mismatches fail before Agent Run preparation/execution.
- `AC-003` — Supported old fixtures migrate to validated derived current artifacts with source/target digest provenance; unsupported changes return an actionable manual migration error and sealed sources remain byte-identical.
- `AC-004` — The bundle contains no application lifecycle/scheduler/authoring implementation and docs/test boundaries prove each application retains its named authority.

## Evaluation / test intent
- `EVAL-002` — kind `acceptance`, oracle `public`
- `EVAL-003` — kind `acceptance`, oracle `public`
- `EVAL-004` — kind `acceptance`, oracle `public`

## Expected outputs
```json
[
  "exact-match/mismatch conformance matrix",
  "migration fixture matrix",
  "independent phase review and release evidence"
]
```

## Structured result
Write the task result using `result-contracts/agent-workflow-task-result-v1.schema.json`; Agent-Workflow owns collection and validation of `result.json`.

## Execution guardrails
- Writable scope: modify only repository paths necessary to satisfy the authorized requirements; Agent-Workflow owns worktree and writable-scope enforcement.
- Acceptance: report against the linked criteria and do not broaden scope to make acceptance easier.
- Test behavior: follow the repository/specification testing policy and the evaluation intent above; do not add tests merely to increase test count.
- Stop conditions: stop and report blocked if required source evidence, permissions, dependencies, or specification decisions are missing or contradictory.
