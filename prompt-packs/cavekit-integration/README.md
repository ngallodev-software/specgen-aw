# SpecGen-AW Cavekit Integration

This pack defines a bounded integration of high-value Cavekit methodology into
SpecGen-AW. It is a plan, not evidence that the work has been implemented.

The canonical authority remains `specgen/spec/v1alpha2`: Cavekit findings are
read-only evidence and proposed inputs until an explicit user-approved action
promotes them. Markdown is rendered output, not a parser ABI. Agent-Workflow
durable runs, receipts, review, acceptance, and release boundaries remain in
force.

## Research basis

- Comparison: `/home/nate/.cavekit/SPECGEN_AW_COMPARISON.md`
- Coverage: `/home/nate/.cavekit/agents/architect.md`, `commands/map.md`,
  `internal/site/frontier.go`, `internal/site/parser.go`,
  `internal/site/tracking.go`
- Brownfield: `/home/nate/.cavekit/skills/brownfield-adoption/SKILL.md`,
  `commands/sketch.md`, `agents/drafter.md`, `agents/surveyor.md`,
  `commands/scan.md`
- Review: `/home/nate/.cavekit/scripts/codex-design-challenge.sh`,
  `scripts/codex-review.sh`, `scripts/codex-gate.sh`,
  `scripts/codex-findings.sh`, `references/validation-gates.md`,
  `commands/revise.md`
- SpecGen targets: `skills/specgen/SKILL.md`,
  `skills/specgen-brownfield/SKILL.md`, `src/specgen/elicitation.py`,
  `src/specgen/repository.py`, `src/specgen/agent_workflow.py`,
  `schemas/spec/v1alpha2.schema.json`, and `tests/critical-seams/run.py`

## Execution

Validate this pack with the installed Agent-Workflow `0.9.0` tool. Execute
tasks through durable Agent Runs in isolated worktrees. Each phase requires an
independent gate before the next phase is accepted.
