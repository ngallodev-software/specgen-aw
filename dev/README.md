# Development source links

> Document version: 0.2.0 · Applies to SpecGen 0.2.0

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

The release installer uses the per-user shared Python environment
`${XDG_DATA_HOME:-$HOME/.local/share}/agent-tools/venv` and links executables
into `~/.local/bin`. When a local Agent-Workflow checkout is available, it
installs that checkout into the same environment after verifying the pinned
compatible version. SpecGen and Agent-Workflow skills are linked into the
generic agent directory plus Codex, Claude, Pi, and OpenCode skill directories.
Set `AGENT_TOOLS_VENV` to choose another shared environment.

The sync command creates ignored links beneath `.dev/agent-workflow/current/`
and `.dev/agent-workflow/lock.json`, which records observed product version,
contract digests, reference-document digests, and drift against the declared
release compatibility fixture.

Drift is fail-closed: review the Agent-Workflow change, decide compatibility,
then explicitly update the compatibility fixture/version declaration.
