# Roadmap

> Document version: 0.2.0 · Applies to SpecGen 0.2.0

Mutable plan; completed architecture decisions remain in ADRs. Testing follows [ENGINEERING_POLICY.md](ENGINEERING_POLICY.md) and is currently disabled by explicit release instruction.

## Phase 0 — Foundation and prior-art assessment

Versioning, contract namespace, ADR discipline, compatibility fixtures, development Agent-Workflow linkage, prior-art assessment, engineering policy, and the first deliberate canonical revision (`specgen/spec/v1alpha2`) are complete.

## Phase 1 — Canonical IR + deterministic validator

Complete in `0.1.3`: contract discovery, JSON Schema validation, stable-ID/reference/trace/preservation checks, dependency cycles, snapshot ancestry/digest checks, canonical serialization/digest, and the deliberately small public critical seam.

## Phase 2 — Markdown projection + authoring history

Complete in `0.1.4`: deterministic Markdown rendering, append-only single-writer authoring events, immutable snapshot semantics, `specgen/semantic-delta/v1alpha1`, and stable-ID semantic diffing.

## Phase 3 — Elicitation/compiler loop

Complete in `0.1.5`: express/guided/strict/agent-workflow authoring profiles, `specgen/elicitation-plan/v1alpha1`, deterministic readiness assessment, and canonical finalization. Provider-driven conversation remains an interaction-surface concern rather than canonical authority.

## Phase 4 — Repository-aware brownfield analysis

Complete in `0.1.6`: `repository-analysis/v1alpha1`, Git/directory baselines, durable contract/interface discovery, explicit referenced evidence, contradictions, `repository-drift/v1alpha1`, Agent-Workflow development target context, and ADR-0007's evidence-first boundary.

## Phase 5 — Evaluation model

Implementation complete in `0.1.7`; integrity corrected in `0.1.8`.

- portable `specgen/evaluation-intent/v1alpha1`;
- requirement ↔ acceptance ↔ evaluation relationships;
- public/hidden/external oracle classification;
- digest-bound hidden/external target references when lowered.

## Phase 6 — Agent-Workflow adapter

**Complete in `0.1.9` at the implementation level; tests intentionally not run.**

Implemented:

- Agent-Workflow-ready authoring state is required before target compilation;
- native phase/ticket prompt-pack resource layout;
- deterministic prompt resources carrying requirements, acceptance, evaluation/test intent, dependencies, expected outputs, source context, result handoff, and stop/writable guardrails;
- task result-contract schemas are packaged as pack-relative JSON Schema resources;
- evaluation lowering fails closed on unsupported metadata, invalid scorers, per-evaluation/global-scorer mismatch, unresolved oracle/task mapping, or incompatible task oracles;
- hidden/external oracle references are mapped to Agent-Workflow task IDs rather than SpecGen evaluation IDs;
- Git-bound `agent-workflow/source-baseline/v1` emission from an exact snapshot-bound repository analysis;
- live repository drift checking before baseline emission;
- source prompt-pack `MANIFEST.sha256` emission;
- no hand-authored `MANIFEST.json`, because Agent-Workflow reserves it for its archive-integrity contract;
- target output directories must be empty, preventing stale resources from surviving recompilation.

Remaining Phase 6 work is release verification only, and must not be run until testing is explicitly re-enabled.

## Phase 7 — Agent skill + optional Agent-Workflow plugin

**Complete in `0.1.10` at the implementation level; tests intentionally deferred.**

- thin agent-facing skill over the canonical CLI/library behavior;
- practical express/guided/strict/agent-workflow workflow guidance;
- repository analysis, uncertainty, preservation, traceability, evaluation, finalization, target compilation, and stop-condition guidance;
- optional `agent-workflow-spec` entry point exposing `agent-workflow spec ...` through Agent-Workflow's public trusted plugin API only;
- plugin commands delegate to SpecGen authorities and return structured host data;
- no SpecGen-internal plugin framework, no private Agent-Workflow imports, and no duplicate specification model;
- no package resources are registered merely to satisfy a plugin surface: the adapter advertises logical SpecGen resources and leaves canonical schemas owned by SpecGen.

## Phase 8 — Minimal application/programmatic API

**Complete in `0.1.11` at the implementation level; tests intentionally deferred.**

`specgen.api` is the stable Python facade over existing authorities for canonical candidate creation/load/write, authoring-event recording, repository analysis, readiness assessment/finalization, validation, rendering, semantic diff, evaluation intent, target compilation/writing, contract/mode discovery, snapshot digests, drift, and compatibility inspection. The conveniences remain contract-backed and do not create mutable service authority.

Normal installed distributions now carry the same source-owned canonical schemas, pinned Agent-Workflow compatibility schemas, compatibility metadata, and skill as installation data. Runtime lookup supports both source checkouts and installed distributions without maintaining duplicate schema copies.

No standalone HTTP service is justified for the initial release. Do not add authentication, databases, background workers, task queues, websockets, provider frameworks, or duplicate persistence unless a concrete later requirement demands them. An HTTP service requires an ADR before implementation.

## Initial public release closeout

**Complete in `0.2.0`; testing follows overlay delivery.**

- release/package/reference surfaces reconciled to `0.2.0`;
- release manifest regeneration remains part of the self-applying overlay;
- README/changelog/roadmap claims reconciled to implemented behavior;
- immutable old schema versions retained with unchanged meanings;
- fresh source-tree consistency audit completed before test execution;
- obsolete generated README variants and old root checkpoint archives removed explicitly;
- cumulative self-applying release overlay produced from authoritative `0.1.8`;
- clean source archives are defined by the regenerated `MANIFEST.sha256` inventory and contain only managed release files;
- deferred work and remaining architecture choices are reported as release notes rather than expanded into speculative code.

## Explicitly deferred

General execution engine, duplicated worker/review/acceptance lifecycle, database as specification authority, generalized plugin/hook marketplace, speculative provider abstraction, arbitrary source-code semantic parsing, or other orchestration not justified by a concrete requirement.
