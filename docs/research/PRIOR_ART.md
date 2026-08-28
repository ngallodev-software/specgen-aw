# Prior Art — Initial Assessment

> Document version: 0.1.8 · Applies to SpecGen 0.1.8

Status: preliminary. This is a shortlist for code-level analysis, not a final reuse decision.

## Tier 1: deep source assessment

### dshills/specBuilder / ngallodev/specBuilder

Source: https://github.com/dshills/specBuilder and the working fork https://github.com/ngallodev/specBuilder

Why it matters: it is unusually close to our intended product. It describes itself as a requirements compiler rather than a chatbot; uses constrained structured output; maintains versioned answers and append-only spec snapshots; enforces trace coverage; validates against JSON Schema; provides issue-to-question links; and exports `SPEC.json`, `SPEC.md`, `PLAN.md`, `TRACE.json`, `DECISIONS.md`, and `ACCEPTANCE.md`.

Deep-review targets:

- `ProjectImplementationSpec.schema.json` and `TRACE.schema.json`;
- question/answer versioning and provenance semantics;
- compiler determinism claims and actual implementation;
- validator architecture and issue classification;
- snapshot/diff persistence;
- export pipeline;
- provider abstraction and places where LLM behavior leaks into authority.

Expected posture: likely mine heavily for domain-model and UX ideas; do not assume its schema should become ours.

### GitHub Spec Kit

Source: https://github.com/github/spec-kit and https://github.github.com/spec-kit/

Why it matters: widely adopted spec-driven workflow with Spec → Plan → Tasks → Implement, cross-artifact checks, templates, and broad coding-agent integration.

Deep-review targets: artifact boundaries, constitution/principles mechanism, agent adapter strategy, checklists, greenfield assumptions, and where Markdown-only authority limits machine traceability.

Expected posture: learn workflow/adapter ergonomics; likely reject Markdown as the sole canonical data contract.

### OpenSpec

Source: https://github.com/Fission-AI/OpenSpec (verify canonical repository during deep review; multiple forks/mirrors are common)

Why it matters: emphasizes lightweight, mutable spec-driven development, separates current truth from proposed change deltas, and uses ADDED/MODIFIED/REMOVED requirement patches with scenarios.

Deep-review targets: change/delta semantics, brownfield updates, scenario format, archive/sync behavior, multi-agent installation, and conflict handling.

Expected posture: delta/change-set model is particularly relevant to versioned canonical snapshots and brownfield specs.

### Cavekit spec workflow

Source: https://github.com/JuliusBrussee/cavekit (currently frozen; ideas have partly migrated into the broader Caveman project).

Why it matters: aggressively lean single-spec approach, durable root `SPEC.md`, explicit invariant/backprop behavior, small skill surface, and right-sizing rather than forcing full ceremony.

Deep-review targets: `spec`/`build`/`check` skills, SPEC format, backpropagation of failures into invariants, research/review handoffs, and token-cost tradeoffs.

Expected posture: borrow the discipline of right-sizing and backpropagation; do not adopt compressed prose as canonical machine semantics.

## Tier 2: architecture/concept assessment

### BMAD Method

Source: https://github.com/bmad-code-org/BMAD-METHOD

Current versions include a `bmad-spec` skill whose `.memlog.md` is an append-only decision/constraint/capability/question log from which `SPEC.md` is derived. This is directly relevant to our unresolved persistence question: immutable answers/snapshots versus append-only event/memory log versus explicit deltas.

Assess the memlog/single-writer model deeply before choosing SpecGen's authoring-history authority. Avoid inheriting the full multi-agent methodology unless evidence shows it solves a SpecGen problem.

### Kiro

Source: https://github.com/kirodotdev/Kiro plus public product documentation.

Relevant concepts: structured requirements/design/tasks, EARS-style requirements, steering, hooks, and repository-aware spec-driven development. Treat as a product/reference comparison first; confirm license/source boundaries before any reuse.

### SpecShip and similar workflows

Source: https://github.com/aws-samples/sample-specship

Relevant for brownfield recon, pre-generated test cases, adversarial validation, and quality gates. More relevant to evaluation/repository analysis than to the canonical core schema.

## Main research question

The deepest design question is not “which project should we fork?” It is:

> Which mechanisms have demonstrated value, and which authority/persistence model lets us combine them without inheriting another framework's constraints?

The comparative review should score mechanisms rather than projects: elicitation, provenance, canonical state, versioning, delta semantics, traceability, validation, repository analysis, evaluation generation, artifact rendering, agent portability, and execution handoff.
