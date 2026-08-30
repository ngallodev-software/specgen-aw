# SpecGen — Selective CaveKit-derived Refinements

This prompt pack is a deliberately narrow plan for harvesting a few useful ideas
from CaveKit without turning SpecGen into CaveKit, an execution engine, or a
second Agent-Workflow.

The authoritative product boundary remains:

> **SpecGen owns specification meaning. Execution targets own execution meaning.**

The current SpecGen 0.2.0 source already implements most of the foundations the
original CaveKit plan proposed: requirement/task/evaluation readiness checks,
task dependency-cycle validation, deterministic repository analysis,
`specgen/brownfield-plan/v1alpha1`, `specgen/brownfield-analysis/v1alpha1`,
authoring history, immutable snapshots, and Agent-Workflow target lowering.
This plan therefore does **not** reimplement those capabilities.

## What remains worth adopting

1. Strengthen implementation-readiness diagnostics around observable acceptance
   using the existing canonical requirements, acceptance criteria, evaluations,
   tasks, and dependency graph.
2. Make brownfield authoring more explicit about **preserve / intentionally
   change / unresolved** decisions while continuing to use the existing
   repository and brownfield contracts.
3. Keep external review feedback as an input to normal SpecGen authoring events,
   rather than creating a review/gate/waiver lifecycle inside SpecGen.

## Explicitly rejected from the earlier plan

- a second `criterion` record alongside `acceptance_criteria`;
- SpecGen-owned ready-frontier, completion, worker, review, gate, receipt, or
  waiver state;
- a second evidence model beside repository-analysis and brownfield evidence;
- a mandatory CaveKit or Codebase Memory runtime dependency;
- broad new CLI/API/report surfaces without a demonstrated authoring need;
- copied Agent-Workflow delegation/runbook/completion machinery;
- default unit-test expansion.

CaveKit remains credited prior art and methodology reference only. Agent-Workflow
0.9.0 remains the execution target and owns durable execution/review/acceptance
state.
