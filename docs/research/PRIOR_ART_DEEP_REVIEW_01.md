# Prior-art deep review 01 — specification authority, history, and agent handoff

> Document version: 0.1.8 · Applies to SpecGen 0.1.8

Date: 2026-08-27
Status: Initial source-level assessment

This review focuses on mechanisms rather than product popularity. The question is:
which ideas materially improve correctness, provenance, reviewability, or agent
handoff enough to earn permanent surface area in SpecGen?

## Sources reviewed

### specBuilder

Repository: https://github.com/dshills/specBuilder

Relevant mechanisms:

- planner → asker → compiler → validator pipeline;
- typed questions mapped to affected spec paths;
- immutable/versioned answers (`supersedes` relationship);
- append-only compiled snapshots;
- canonical structured spec plus Markdown and trace artifacts;
- schema validation plus semantic issues;
- trace coverage requirement for populated spec fields;
- explicit export bundles for downstream coding agents.

Assessment:

- **RETAIN/ADAPT:** constrained compiler framing rather than chatbot framing.
- **RETAIN/ADAPT:** question ledger + affected paths/IDs.
- **RETAIN/ADAPT:** immutable answer/decision history.
- **RETAIN/ADAPT:** snapshot immutability and deterministic compilation goals.
- **RETAIN/ADAPT:** explicit trace artifact/coverage checking.
- **REJECT AS CORE SHAPE:** adopting `ProjectImplementationSpec` wholesale. It is
  useful prior art but mixes product, implementation, UI/API, planning, and acceptance
  into one project-shaped contract that is narrower than SpecGen's target domain.
- **DEFER:** database/application architecture. SpecGen should establish portable
  contracts and CLI/compiler semantics before selecting a persistent service model.

## GitHub Spec Kit

Repository: https://github.com/github/spec-kit
Documentation: https://github.github.com/spec-kit/

Current workflow is substantially broader than early Spec Kit: core SDD remains
Spec → Plan → Tasks → Implement, but the project now includes clarification,
checklists, cross-artifact analysis, convergence, extensions, presets, workflows,
and many coding-agent integrations.

Relevant mechanisms:

- project constitution/organizational rules preceding feature work;
- clarification as a quality gate when ambiguity matters;
- read-only cross-artifact consistency analysis;
- dependency-ordered task generation;
- convergence check after implementation;
- agent integration as replaceable delivery adapters;
- capability/version inspection for automation.

Assessment:

- **RETAIN/ADAPT:** explicit quality gates: clarify, analyze, converge.
- **RETAIN/ADAPT:** project-wide policy/constitution concept, but represent it as
  versioned context/constraints rather than special Markdown authority.
- **RETAIN/ADAPT:** broad agent portability through thin adapters.
- **RETAIN/ADAPT:** machine-readable capability/version discovery.
- **REJECT AS AUTHORITY MODEL:** Markdown artifact chain as the primary canonical
  state. SpecGen needs one structured authority with projections.
- **DEFER:** broad extension/preset ecosystem until at least two concrete third-party
  integrations demonstrate the required abstraction.

## OpenSpec

Repository: https://github.com/Fission-AI/OpenSpec

OpenSpec is especially strong on brownfield change semantics. Its current model keeps
resolved system truth under `openspec/specs/` and proposed work under
`openspec/changes/`, with proposal/design/tasks and delta specs grouped by change.
It also defines workflow schemas as artifact dependency graphs.

Relevant mechanisms:

- current truth separated from proposed change;
- explicit added/modified/removed requirement deltas;
- scenario-linked requirements;
- change folders that co-locate proposal/design/tasks/deltas;
- configurable artifact dependency graphs;
- project context + per-artifact rules;
- explore-before-commit workflow for uncertain ideas.

Assessment:

- **RETAIN/ADAPT:** semantic added/modified/removed delta views.
- **RETAIN/ADAPT:** distinction between current truth and a proposed future state.
- **RETAIN/ADAPT:** artifact dependency graph as a possible compiler/workflow model.
- **RETAIN/ADAPT:** explicit project context/rules injection, but typed where possible.
- **REJECT AS SOLE AUTHORITY:** patch/delta files cannot replace a resolved canonical
  full-state machine contract.
- **DEFER:** arbitrary user-defined workflow schemas until the core compiler has a
  stable artifact graph.

## BMAD / bmad-spec

Repository: https://github.com/bmad-code-org/BMAD-METHOD
Relevant skill: `src/bmm-skills/plan/bmad-spec/SKILL.md`

The current `bmad-spec` implementation is notable because `.memlog.md`, not `SPEC.md`,
is canonical. The memlog is append-only and records decisions, constraints,
capabilities, assumptions, questions, direction, notes, and events. `SPEC.md` and
spec-authored companions are re-derived from it. Capability IDs remain stable and are
not reused. The skill also defines a preservation pass that checks load-bearing source
claims were not silently dropped.

Relevant mechanisms:

- append-only decision memory;
- derived current contract;
- stable capability IDs across updates;
- explicit assumptions/open questions rather than fabrication;
- load-bearing-content preservation audit;
- single-writer ownership for generated artifacts;
- lean kernel plus discoverable companions.

Assessment:

- **RETAIN/ADAPT:** append-only authoring event journal.
- **RETAIN/ADAPT:** stable IDs that survive updates and retirement.
- **RETAIN/ADAPT:** preservation validation from source evidence to spec.
- **RETAIN/ADAPT:** assumptions/questions as explicit unresolved state.
- **ADAPT, NOT COPY:** single-writer principle becomes canonical compiler authority;
  SpecGen's canonical snapshot remains structured JSON rather than rendered Markdown.
- **REJECT:** five-field kernel as SpecGen's universal canonical schema. It is an
  intentionally compressed downstream contract, whereas SpecGen needs richer typed
  data/contracts/eval/trace structure.

## Cavekit

Repository: https://github.com/JuliusBrussee/cavekit

Cavekit v4 is particularly useful as negative architectural evidence: its author
rewrote a much larger v3 system after concluding that agent swarms, orchestration,
hooks, dashboards, and many skills cost more complexity/context than they returned.
The surviving core centers on one durable spec, a small command loop, drift checking,
and backpropagating test failures into bugs/invariants.

Relevant mechanisms:

- durable context that survives agent resets;
- tiny default workflow surface;
- explicit interfaces/invariants/tasks/bugs sections;
- read-only drift detection;
- test failure → durable bug → generalized invariant feedback;
- optional research/review/grilling only when the task earns the ceremony;
- strict complexity/context-budget discipline.

Assessment:

- **RETAIN/ADAPT:** right-sized ceremony and small common path.
- **RETAIN/ADAPT:** failure backpropagation into durable knowledge.
- **RETAIN/ADAPT:** read-only drift checker separate from mutator/compiler.
- **RETAIN/ADAPT:** explicit invariant concept; likely represent as requirement or
  constraint subtype rather than special Markdown section.
- **REJECT:** Markdown-only canonical body. It conflicts with SpecGen's machine-first
  interoperability goal.
- **REJECT:** execution/orchestration features from older Cavekit; Agent-Workflow owns
  that domain for our first execution target.

# Cross-project conclusions

## 1. Separate authoring history from current canonical truth

Strongest synthesis:

```text
append-only events
      │
      ▼
deterministic compiler
      │
      ▼
immutable canonical snapshot
      │
      ├── human projection
      ├── semantic delta vs prior snapshot
      ├── eval artifacts
      └── execution-target compilation
```

Accepted as ADR-0005.

## 2. Preserve source claims, not just final prose

SpecBuilder trace coverage and BMAD's preservation sweep converge on the same lesson:
a spec compiler must detect silent loss of load-bearing input. SpecGen should eventually
have a deterministic preservation/coverage report that maps evidence/decisions to
canonical fields and flags materially unrepresented claims.

## 3. Treat ambiguity handling as a quality policy, not mandatory ceremony

Spec Kit clarification, OpenSpec explore, BMAD express/guided modes, and Cavekit grill
all imply the same useful behavior: sparse/ambiguous input sometimes needs interactive
questions, but rich structured input should not be forced through a ritual questionnaire.

SpecGen should support at least:

- `express`: best-effort compile + assumptions/open questions;
- `guided`: targeted elicitation until selected quality thresholds are met;
- `strict/headless`: fail closed when required intent cannot be derived safely.

The exact names remain provisional.

## 4. Add current-vs-proposed semantics without turning patches into truth

OpenSpec's brownfield model is strong. SpecGen should support a proposal/change object
that can produce a candidate next canonical snapshot and a semantic delta, while keeping
the full validated snapshot as the downstream contract.

## 5. Make drift/convergence first-class read-only operations

Spec Kit's analyze/converge and Cavekit's check suggest distinct validators:

- specification integrity: schema, IDs, references, trace coverage;
- evidence drift: repository/source facts no longer match baseline;
- implementation convergence: current implementation satisfies canonical spec;
- target compatibility: compiled artifacts still validate against target contracts.

Mutators should not hide inside these checks.

## 6. Complexity must be evidence-backed

Cavekit's v3→v4 rewrite is a useful warning for SpecGen. Avoid adding orchestration,
agent swarms, a plugin marketplace, a large persistence service, or bespoke execution
lifecycle until a concrete requirement cannot be handled by the compiler/adapter model.

# Immediate schema implications for v1alpha1

Candidate refinements before Phase 1 implementation:

1. Add stable identity semantics for every durable object and a retirement rule.
2. Define provenance categories: user decision, source evidence, inference, assumption.
3. Define a separate authoring-event contract instead of embedding full history in the
   canonical spec snapshot.
4. Define snapshot identity/digest metadata.
5. Make semantic deltas derived from snapshot comparison.
6. Add explicit invariant/constraint representation if current requirement typing is
   insufficient.
7. Add preservation/trace coverage expectations.
8. Add proposal/candidate-snapshot semantics to the roadmap, not necessarily the first
   canonical schema revision.

# Licensing note

All reviewed projects are being treated as prior art/inspiration unless source is
explicitly copied later. Any copied/adapted code must be reviewed against its license
and retain required notices. Mechanism-level architectural inspiration should remain
credited in README/research/ADRs.

## 0.1.1 disposition

The immediate schema implications above were applied as follows:

- stable durable-object identity/retirement: `specgen/spec/v1alpha2`;
- typed provenance: `v1alpha2.provenance.sources`;
- authoring history: separate `specgen/authoring-event/v1alpha1` contract;
- snapshot identity/ancestry/event references: `v1alpha2.snapshot`;
- preservation coverage: `v1alpha2.preservation.claims`;
- invariant representation: `requirements[].type = invariant`;
- current/proposed semantics: `v1alpha2.state`, with proposed state bound to a base snapshot/change ID;
- semantic deltas remain derived and are not canonical truth.
