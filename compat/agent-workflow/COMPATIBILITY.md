# Agent-Workflow Compatibility

> Document version: 0.2.0 · Applies to SpecGen 0.2.0

SpecGen is independently installable. This directory records the Agent-Workflow contracts an adapter is allowed to understand. Vendored schemas are compatibility fixtures, not imported runtime authority.

`0.9.1/SNAPSHOT.json` is the deterministic compatibility capture. It records
the source revision, all Agent-Workflow schema digests, and the Python
requirements for both projects as installed in the shared environment. Refresh
it only through the capture command after an explicit compatibility review:

```bash
python scripts/capture-agent-workflow-compat.py \\
  --source /path/to/agent-workflow \\
  --output compat/agent-workflow/0.9.1
```

The live source may be dirty during development, but schema drift and
inconsistent shared-environment requirements fail release verification.

## Initial target

- Agent-Workflow product version: `0.9.1`
- pinned snapshot label: `agent-workflow-0.9.1-release-tooling-b5e73c9`

Recognized contracts:

- `agent-workflow/prompt-pack/v1` — implementation workflow/task structure.
- `agent-workflow/evaluation-plan/v1` — executable evaluation plan where portable intent is representable.
- `agent-workflow/source-baseline/v1` — Git source-baseline target.
- `agent-workflow/agent-role/v1` — optional logical target hint vocabulary.
- `agent-workflow/task-result/v1` — generic result schema that SpecGen can package as a task-local contract resource.

The durable compatibility matrix is `compatibility.json` under `target.compatible_releases`. It retains one entry per assessed Agent-Workflow application release, with immutable fixture paths and SHA-256 digests. The `0.9.0` and `0.9.1` entries intentionally reference the same public schema IDs and bytes; the application version changed without a public contract change. Do not delete an older fixture when a newer application release is added.

Agent-Workflow also publishes a trusted plugin API and stable integration surfaces. SpecGen uses those public seams rather than private modules.

## Adapter policy

- Generated artifacts are validated against the pinned schema fixtures before writing.
- Source-baseline emission requires exact SpecGen repository-analysis/spec binding and live Git-state agreement.
- Result contracts are packaged as real pack-relative JSON Schema resources.
- Hidden/external evaluation oracles are digest-bound and mapped to Agent-Workflow task IDs.
- Unsupported or ambiguously representable evaluation/result/source semantics fail closed.
- A future Agent-Workflow release is not automatically compatible because similar files still validate; compatibility must be reassessed deliberately.

## Plugin adapter

SpecGen `0.1.10` optionally registers `agent-workflow-spec` in the public `agent_workflow.plugins` entry-point group. The adapter imports only `agent_workflow.plugin_api`, requires host version `0.9.1`, and delegates to SpecGen's stable programmatic facade. Canonical schemas are not duplicated as plugin package resources.
