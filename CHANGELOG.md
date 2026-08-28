# Changelog

## Unreleased

- Add an end-to-end application usage guide and focused brownfield authoring guide.
- Add `specgen brownfield capabilities` and `specgen brownfield plan` over the existing deterministic repository-analysis boundary.
- Add optional `codebase-memory-mcp` detection; ordinary SpecGen use remains dependency-free and MCP registration remains owned by the invoking agent/runtime.
- Add `specgen/brownfield-plan/v1alpha1` and `specgen/brownfield-analysis/v1alpha1` so targeted research instructions and semantic agent findings remain distinct from deterministic repository evidence.
- Add a dedicated `specgen-brownfield` skill that asks users only for decisions the code cannot answer and uses graph search/call tracing/snippet reads with explicit narrowing and stop conditions.
- Record ADR-0008 preserving the deterministic/agent-assisted evidence boundary.
- No tests added or run during this implementation checkpoint.


## 0.2.0 — 2026-08-27

Initial public release closeout over the completed 0.1.x implementation phases.

- Promote the coherent canonical authoring, repository evidence, evaluation, Agent-Workflow compilation, skill/plugin, and programmatic API surface to the initial public release.
- Keep `specgen/spec/v1alpha2` and all previously published contract IDs unchanged; the software release does not redefine existing schema meaning.
- Reconcile package, compatibility, README, roadmap, and maintained reference-document release markers.
- Remove obsolete generated README variants and old checkpoint archives from the repository root.
- Preserve Agent-Workflow 0.9.0 as an optional, explicitly versioned target and public-plugin host rather than a core runtime dependency.
- Keep standalone HTTP/service infrastructure deferred until a concrete requirement justifies a new authority boundary.
- Release overlay remains cumulative from authoritative SpecGen 0.1.8 and is self-applying/deletion-aware.
- Tests are intentionally deferred until after overlay delivery, per release instruction.

## 0.1.11 — 2026-08-27

Complete the minimal application/programmatic API and installed-runtime asset boundary.

- Add deterministic canonical candidate creation plus load/write conveniences.
- Add authoring-event record convenience over the existing validated single-writer event log.
- Expand `specgen.api` without introducing persistence, services, provider frameworks, or another specification model.
- Install the existing source-owned schemas, Agent-Workflow compatibility fixtures/metadata, and skill as distribution data.
- Locate runtime contracts in either a source checkout or installed distribution so normal package/plugin use does not depend on repository-relative paths.
- No tests added or run; verification remains deferred until overlays are delivered.

## 0.1.10 — 2026-08-27

Complete the agent-facing and programmatic integration surfaces without creating another specification authority.

- Add the thin `skills/specgen/SKILL.md` workflow over existing canonical authorities.
- Add stable `specgen.api` facade for programmatic integrations without service/persistence architecture.
- Add optional `agent-workflow-spec` public plugin entry point with compatibility, assess, analyze, finalize, and compile commands.
- Add public Agent-Workflow compatibility inspection and shared target writing for CLI/plugin callers.
- Keep Agent-Workflow optional: no private imports, no runtime dependency, no duplicate model, and no speculative plugin package resources.
- No tests added or run; verification remains deferred until overlays are delivered.

## 0.1.9 — 2026-08-27

Complete the Agent-Workflow 0.9.0 compilation seam without changing the canonical SpecGen schema.

- Require `agent-workflow` authoring readiness before target compilation.
- Generate Agent-Workflow-native phase/ticket prompt-pack resources and prevent stale output by requiring an empty target directory.
- Package task result contracts as real pack-relative JSON Schema resources; fail closed on unresolvable or unsupported result-contract semantics.
- Emit `agent-workflow/source-baseline/v1` from an exact snapshot-bound Git repository analysis and re-check live HEAD/dirty state before lowering.
- Correct hidden/external oracle lowering so Agent-Workflow `oracle_refs` are keyed by implementation task IDs rather than SpecGen evaluation IDs.
- Remove the invalid fallback scorer `acceptance`; command-based evaluation uses Agent-Workflow's `acceptance_commands` scorer and unsupported/global-scorer conflicts fail closed.
- Reject evaluation metadata that cannot be represented rather than silently discarding it.
- Emit source prompt-pack `MANIFEST.sha256`; deliberately do not emit `MANIFEST.json`, which Agent-Workflow reserves for its own archive-integrity contract.
- Align current release/reference surfaces to 0.1.9 and correct the stale `Current release: 0.1.5` versioning reference.
- No tests added or run by explicit instruction.

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
