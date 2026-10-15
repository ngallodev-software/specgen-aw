# Implementation Plan

## Phase 1 — Close real readiness gaps only

Implement the smallest changes needed to improve Agent-Workflow authoring
readiness using the existing canonical model.

Primary candidates:

- make missing acceptance criteria blocker-level in `agent-workflow` mode;
- count acceptance-linked evaluations when assessing requirement evaluation
  coverage;
- improve diagnostics around existing task/dependency relationships where an
  actual gap is demonstrated.

Do not add a new criterion schema, coverage ledger, task status, ready frontier,
receipt model, or canonical schema revision merely to implement this phase.

## Phase 2 — Refine brownfield authoring behavior

Update the existing brownfield planner/skill only where needed to make
preserve/change/unresolved decisions explicit and to route approved outcomes
through the existing canonical authoring lifecycle.

Do not reimplement repository analysis, brownfield plan/analysis contracts,
provenance, or authoring history. Do not add a generic parity subsystem unless a
real workflow proves the current contracts insufficient.

Update documentation only where implemented behavior changes.

## Phase 3 — Focused verification

After implementation is complete, run the smallest high-value verification set:

- contract/schema validation for changed public contracts (if any);
- the existing critical-seam/integration journey covering authoring readiness;
- a focused brownfield authoring journey if brownfield behavior changed;
- Agent-Workflow prompt-pack compilation/validation if the target boundary was
  touched;
- packaging smoke only if packaged files or entry points changed.

Do not add or run broad unit-test suites by default. Add a low-level test only
when the behavior cannot be protected economically at a higher-value seam.

## Decision stops

Stop and require an architectural decision if implementation appears to require:

- a change to `specgen/spec/v1alpha2` meaning;
- SpecGen-owned execution/review/acceptance state;
- a new persistent coverage/parity/receipt authority;
- a mandatory CaveKit or Codebase Memory dependency;
- a second model for concepts already represented in canonical SpecGen data;
- a new service, database, worker framework, or generalized extension system.
