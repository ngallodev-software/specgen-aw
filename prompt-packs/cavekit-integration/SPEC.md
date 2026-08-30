# Selective CaveKit-derived Refinements — Specification

> Status: proposed post-0.2 refinement plan. No canonical schema revision is authorized by this document.

## Goal

Improve SpecGen's ability to produce implementation-ready and brownfield-safe
specifications by selectively adopting high-value CaveKit ideas **only where they
reinforce SpecGen's existing product purpose**.

The work is intentionally limited to authoring quality, traceability, evidence,
and handoff readiness. It must not add execution orchestration or duplicate
Agent-Workflow lifecycle authority.

## Existing authorities to reuse

The following current SpecGen 0.2.0 concepts remain authoritative and should be
extended only when a concrete gap is demonstrated:

- `specgen/spec/v1alpha2` for canonical specification meaning;
- `acceptance_criteria` as the canonical criterion concept;
- implementation tasks plus `dependencies` as the static implementation graph;
- `specgen/elicitation-plan/v1alpha1` for readiness questions and blockers;
- `specgen/repository-analysis/v1alpha1` for deterministic repository evidence;
- `specgen/brownfield-plan/v1alpha1` for research planning;
- `specgen/brownfield-analysis/v1alpha1` for agent-assisted semantic findings;
- preservation claims, provenance, risks, decisions, unresolved questions, and
  authoring events for promotion into canonical meaning;
- Agent-Workflow target compilation for execution handoff.

## Invariants

1. `specgen/spec/v1alpha2` remains the sole current specification authority.
2. Acceptance criteria remain the criterion model; no parallel `criterion`
   entity is introduced.
3. Coverage is derived from canonical relationships. A coverage view or
   diagnostic never becomes a competing source of truth.
4. Task dependencies describe static implementation intent only. Runtime
   readiness/frontier/completion state belongs to the execution target.
5. Deterministic repository evidence remains separate from agent inference.
6. Brownfield observations do not become requirements merely because they exist
   in the current codebase.
7. Preserve/change decisions require user-authorized specification changes and
   flow through normal authoring history.
8. Review findings, gate results, waivers, and execution receipts are not new
   SpecGen lifecycle authorities.
9. Agent-Workflow remains a versioned target, not a SpecGen runtime dependency.
10. CaveKit and Codebase Memory remain optional prior-art/tooling inputs, never
    canonical authorities or required dependencies.
11. Existing public contracts are not mutated silently. Any genuinely necessary
    contract change follows SpecGen's versioning and ADR rules.
12. Complexity must earn its cost; a diagnostic or skill refinement is preferred
    over a new contract, command, or service when it solves the same problem.

## Refinement A — Acceptance and implementation readiness

Use the existing authoring model rather than adding a criterion/task-coverage
subsystem.

Required behavior:

- In `agent-workflow` authoring mode, every active requirement should have an
  observable acceptance criterion before compilation readiness is granted.
- Evaluation coverage for a requirement should recognize both direct
  `evaluation.requirement_ids` links and evaluations linked through that
  requirement's acceptance criteria.
- Existing task coverage (`task.requirement_ids`) and dependency validation are
  retained.
- Existing unknown-dependency and cycle checks remain authoritative.
- If an implementation phase/task assignment creates a target-specific
  impossibility, reject it at the Agent-Workflow readiness/compile boundary;
  do not add runtime scheduling state to the canonical spec.
- Human-facing coverage summaries may be derived for diagnostics, but no stored
  coverage ledger, completion status, receipt list, or ready frontier is added.

This is the useful part of CaveKit's coverage/frontier idea: make missing
implementation proof obvious **before** handoff, without importing its runtime
tracking model.

## Refinement B — Brownfield preserve/change discipline

Do not implement a second brownfield extractor or a new parity database. The
current repository and brownfield contracts already establish the correct
boundary.

Refine the brownfield skill/planner so material current-system findings are
handled with an explicit authoring question:

- **preserve** — current behavior is an intentional compatibility obligation;
- **change** — the user explicitly authorizes a different desired behavior;
- **unresolved** — more code evidence or a user decision is still required.

The classification is an authoring aid, not a new canonical entity. Accepted
outcomes are represented using the existing canonical requirements,
preservation claims, decisions, risks, unresolved questions, provenance, and
authoring events.

The agent should continue to:

- investigate code-answerable questions rather than asking the user;
- ask the user for intent, scope, priority, policy, and acceptance decisions;
- distinguish observed facts, strong inference, tentative inference, and user
  decisions;
- use Codebase Memory only when available and helpful;
- stop research when remaining uncertainty is a product decision.

A new brownfield contract version is justified only if a concrete workflow
cannot be represented cleanly by the existing v1alpha1 plan/analysis contracts.
Such a change must not force a canonical `specgen/spec` revision unless canonical
meaning itself changes.

## Refinement C — External review feedback

Retain the useful CaveKit principle that findings should not disappear silently,
but implement it through SpecGen's existing authoring lifecycle:

- external reviewer feedback is evidence/input;
- accepted feedback becomes an explicit authoring event and canonical change;
- rejected feedback may be captured as a decision/rationale when useful;
- unresolved feedback remains an unresolved question or risk.

Do **not** add SpecGen-owned `review_finding`, `gate_receipt`, or `waiver`
contracts merely to mirror execution governance. Agent-Workflow or another
execution target may own those records in its own lifecycle.

## Explicit non-goals

- runtime task frontier calculation;
- worker/process/run state;
- review orchestration;
- acceptance/release gate state;
- execution waivers or receipt ledgers;
- mutable findings databases;
- CaveKit Markdown parsing or shell-ledger compatibility;
- a generic source-code semantic indexer;
- a generic plugin/hook framework;
- new HTTP/database/background-service architecture;
- reimplementation of capabilities already present in SpecGen 0.2.0.

## Success criteria

The refinement is successful if SpecGen becomes better at detecting a spec that
is not yet safe to hand to an implementation agent, and better at distinguishing
brownfield behavior that must be preserved from behavior intentionally being
changed, while the canonical model, execution boundary, and application size
remain essentially as simple as before.
