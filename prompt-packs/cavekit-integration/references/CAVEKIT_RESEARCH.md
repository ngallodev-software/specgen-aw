# Cavekit research evidence

The comparison was read from `/home/nate/.cavekit/SPECGEN_AW_COMPARISON.md`.
Codebase Memory project `home-nate-.cavekit` was ready with 2,801 nodes and
4,624 edges.

High-value evidence:

- Coverage/DAG: `internal/site/frontier.go:ReadyTasks,FrontierSummary`,
  `internal/site/parser.go:Task,parseTableRow,parseBlockedBy`,
  `internal/site/tracking.go`, `internal/site/frontier_test.go`,
  `agents/architect.md`, `commands/map.md`.
- Brownfield: `skills/brownfield-adoption/SKILL.md`, `commands/sketch.md`,
  `agents/drafter.md`, `agents/surveyor.md`, `commands/scan.md`,
  `REPO_DISSECTION.md`.
- Review/validation/revision: `scripts/codex-design-challenge.sh`,
  `scripts/codex-review.sh`, `scripts/codex-gate.sh`,
  `scripts/codex-findings.sh`, `scripts/codex-speculative.sh`,
  `references/validation-gates.md`, `commands/revise.md`.

Important negative evidence: Cavekit has no typed waiver contract, no standalone
brownfield extractor, and no durable structured receipt authority. Its parser,
shell ledgers, mutable findings, and speculative PID state are reference
material only.
