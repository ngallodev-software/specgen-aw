# Development source links

> Document version: 0.1.8 · Applies to SpecGen 0.1.8

Copy `dev/agent-workflow.example.toml` to the ignored
`dev/agent-workflow.toml`, then set the local Agent-Workflow source root. The
machine-specific config declares the Agent-Workflow source identity and the
public surfaces SpecGen watches during development. The root can also be
overridden with `SPECGEN_AGENT_WORKFLOW_ROOT`.

The checked-in release compatibility authority remains under
`compat/agent-workflow/`. Development links never rewrite it automatically.

```bash
cp dev/agent-workflow.example.toml dev/agent-workflow.toml
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
