# Agent-Workflow Compatibility

> Document version: 0.1.1 · Applies to SpecGen 0.1.1

SpecGen is independently installable. This directory records the Agent-Workflow contracts an adapter is allowed to understand. Vendored schemas are **compatibility fixtures**, not imported runtime authority.

## Initial target

Authoritative source snapshot supplied in this project thread:

- Agent-Workflow product version: `0.9.0`
- snapshot label: `agent-workflow-0.9.0-phases8-9-dev-source-20260827`

Recognized contracts:

- `agent-workflow/prompt-pack/v1` — target compilation format for implementation workflow/task structure.
- `agent-workflow/evaluation-plan/v1` — target compilation format for executable evaluation plans.
- `agent-workflow/source-baseline/v1` — repository/source baseline interoperability.
- `agent-workflow/agent-role/v1` — optional target execution hint vocabulary; not part of SpecGen core semantics.
- `agent-workflow/task-result/v1` — baseline result contract pattern for target tasks; SpecGen may also generate task-specific JSON Schemas.

Agent-Workflow documentation additionally defines stable public `--json` integration surfaces and a trusted plugin API. Future integration must use those public seams rather than private modules.

## Policy

A future Agent-Workflow release is not automatically compatible merely because it still reports `0.x` or accepts similar files. Adapter support must be updated against explicit schema/API identifiers and verification fixtures.
