# Changelog

## 0.1.8 — 2026-08-27

Midpoint integrity correction after fresh source audit.

- Regenerate release manifest and align maintained reference-document versions.
- Align Agent-Workflow compatibility metadata with the current SpecGen release and previously verified pinned 0.9.0 contract digests.
- Fix the advertised Agent-Workflow compatibility contract ID to match its schema `$id`.
- Make hidden/external Agent-Workflow evaluation lowering fail closed unless a digest-bound `metadata.oracle_ref` is supplied, instead of silently dropping oracle semantics.
- No tests added or run by explicit instruction.

## 0.1.7

- Added portable `specgen/evaluation-intent/v1alpha1`.
- Added Agent-Workflow 0.9.0 prompt-pack/evaluation-plan compiler with pinned-schema validation.
- Added deterministic task prompt resources and CLI compile surface.
- No tests added or run for this release slice by explicit release instruction.

## 0.1.6 — 2026-08-27

Phase 4 repository-aware brownfield evidence boundary.

- Add `specgen/repository-analysis/v1alpha1` with revision binding, hashed evidence, durable interface/data-contract discovery, and evidence-backed contradictions.
- Add `specgen/repository-drift/v1alpha1` for read-only baseline/evidence drift.
- Add `repo analyze` and `repo drift` CLI seams.
- Let `agent-workflow` analysis attach declared/live Agent-Workflow target context without importing its runtime.
- Record ADR-0007 limiting deterministic discovery to durable declarations and explicit references rather than heuristic source-code semantics.
- Extend only the phase-end black-box critical seam; no unit-test suite added.
- Record `https://github.com/ngallodev-software/specgen-aw` as the canonical public repository.
- Keep the phase-end critical seam integration-oriented while removing redundant process launches that added runtime without adding coverage.


## 0.1.5 — 2026-08-27

- Added `express`, `guided`, `strict`, and opinionated `agent-workflow` authoring profiles.
- Added `specgen/elicitation-plan/v1alpha1` for deterministic typed questions and guardrails.
- Added candidate finalization with mode readiness checks and canonical snapshot digest binding.
- Recorded ADR-0006 preserving authoring modes as policy rather than canonical schema shape.

All notable changes are recorded here. Software releases use Semantic Versioning; machine contracts carry independent explicit identifiers.

## 0.1.4 — 2026-08-27

Phase 2 deterministic projection/history/diff boundary.

- Add deterministic Markdown rendering from valid `specgen/spec/v1alpha2` snapshots.
- Add validated append-only single-writer NDJSON persistence for `specgen/authoring-event/v1alpha1`.
- Add versioned `specgen/semantic-delta/v1alpha1` and stable-ID semantic snapshot diffing that excludes snapshot bookkeeping.
- Add CLI seams: `render`, `events append`, and `diff`.
- Extend the phase-end black-box critical seam instead of adding unit tests.

## 0.1.3 - 2026-08-27

- Close Phase 1 with a deliberately small public CLI critical-seam corpus through the public CLI.
- Cover valid canonical and authoring-event contracts plus broken references, dependency cycles, and stale snapshot digests.
- Record the successful phase-end verification without expanding into unit-test coverage.


All notable changes are recorded here. Software releases use Semantic Versioning; machine contracts carry independent explicit identifiers.

## 0.1.2 — 2026-08-27

Phase 1 deterministic contract core, implementation checkpoint.

- Add explicit contract discovery for published SpecGen schema identifiers.
- Add compact sorted canonical JSON serialization and SHA-256 snapshot digests; declared snapshot digests omit their own field before hashing.
- Add deterministic JSON Schema + semantic validation for stable IDs, critical references, trace links, preservation mappings, task dependency cycles, snapshot ancestry, and declared digests.
- Add CLI seams: `contracts`, `validate`, and `digest`; validation can emit structured JSON diagnostics.
- Add the `jsonschema` runtime dependency; no broader framework layers introduced.
- Keep Phase 1 open for the intentionally small critical-seam corpus and phase-end verification. No tests run at this checkpoint.

## 0.1.1 — 2026-08-27

First deliberate contract revision and engineering-policy baseline.

- Add immutable `specgen/spec/v1alpha2`; retain `v1alpha1` unchanged.
- Add `specgen/authoring-event/v1alpha1` as the append-only authoring-history boundary.
- Add stable lifecycle-aware object IDs, current/proposed state, snapshot identity/ancestry, typed provenance, preservation claims, and invariant requirements.
- Record lean source, high-value testing, focused/versioned documentation, single-source diagram, and self-applying overlay policies.
- Refactor README into a concise public entry point with linked drill-down documentation.
- Rough out Phase 1 implementation modules before coding.

## 0.1.0 — 2026-08-27

Initial architecture scaffold.

- Establish `specgen/spec/v1alpha1` as the first canonical specification contract.
- Pin initial Agent-Workflow compatibility assessment to Agent-Workflow `0.9.0`.
- Add explicit compatibility manifest and vendored compatibility fixtures for selected Agent-Workflow public schemas.
- Establish ADR discipline and canonical-IR → projections/adapters architecture.
- Add development Agent-Workflow source-link/drift workflow.
- Add source-level prior-art review and ADR-0005 selecting append-only authoring events + immutable snapshots + derived semantic deltas.
