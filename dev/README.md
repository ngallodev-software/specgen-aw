# Development source links

> Document version: 0.1.1 · Applies to SpecGen 0.1.1

`dev/agent-workflow.toml` declares the Agent-Workflow source identity and the
public surfaces SpecGen watches during development. The machine-specific root
can be overridden with `SPECGEN_AGENT_WORKFLOW_ROOT`.

The checked-in release compatibility authority remains under
`compat/agent-workflow/`. Development links never rewrite it automatically.

```bash
python scripts/sync-agent-workflow-dev.py
SPECGEN_AGENT_WORKFLOW_ROOT=/path/to/agent-workflow python scripts/sync-agent-workflow-dev.py
python scripts/sync-agent-workflow-dev.py --check
```

The sync command creates ignored links beneath `.dev/agent-workflow/current/`
and `.dev/agent-workflow/lock.json`, which records observed product version,
contract digests, reference-document digests, and drift against the declared
release compatibility fixture.

Drift is fail-closed: review the Agent-Workflow change, decide compatibility,
then explicitly update the compatibility fixture/version declaration.
