# Roadmap

> Document version: 0.1.8 · Applies to SpecGen 0.1.8

Mutable plan; completed architecture decisions remain in ADRs. Tests are run only on explicit request or at the end of a phase that could have broken behavior; see [ENGINEERING_POLICY.md](ENGINEERING_POLICY.md).

## Phase 0 — Foundation and prior-art assessment

- Versioning, contract namespace, ADR discipline, compatibility fixtures, repository layout. **Done.**
- Initial source-level prior-art review and retain/adapt/reject/defer matrix. **Done.**
- Development Agent-Workflow drift/link config. **Done.**
- ADR-0005 event + immutable snapshot + derived-delta architecture. **Done.**
- First deliberate canonical revision: `specgen/spec/v1alpha2`. **Done in 0.1.1.**
- Resolve public project naming and licensing before stable release.

Exit signal: architecture and contracts are concrete enough to implement a small deterministic core without inheriting a prior-art framework.

## Phase 1 — Canonical IR + deterministic validator

Planned source before implementation:

```text
src/specgen/contracts.py    schema discovery + contract identity
src/specgen/canonical.py    canonical serialization/digest boundary
src/specgen/validate.py     schema + ID/ref + trace/preservation checks
```

Do not split these further without demonstrated need.

- Schema discovery/validation for `v1alpha2` and authoring events. **Implemented in 0.1.2.**
- Stable-ID and critical referential-integrity checks. **Implemented in 0.1.2.**
- Trace-reference, preservation, snapshot ancestry, and digest checks. **Implemented in 0.1.2.**
- Canonical JSON serialization/digest. **Implemented in 0.1.2.**
- Small public CLI known-good/known-bad critical-seam corpus protecting the public validator/digest seam. **Done in 0.1.3.**

Exit signal: canonical specs can be validated deterministically without an LLM. **Phase 1 complete in 0.1.3; critical seam verification passed at phase close.**

## Phase 2 — Markdown projection + authoring history

Planned source before implementation:

```text
src/specgen/render.py     canonical snapshot → deterministic Markdown
src/specgen/history.py    validated append-only authoring-event persistence
src/specgen/diff.py       immutable snapshots → semantic delta
```

- Deterministic `SPEC.md` projection. **Implemented in 0.1.4.**
- Append-only event persistence boundary from ADR-0005. **Implemented in 0.1.4 as a single-writer NDJSON seam.**
- Versioned `specgen/semantic-delta/v1alpha1` contract. **Implemented in 0.1.4.**
- Stable-ID semantic diff between immutable snapshots; snapshot bookkeeping excluded. **Implemented in 0.1.4.**
- Extend the black-box critical seam at phase close. **Done in 0.1.4.**

Exit signal: canonical state, history, and human projection cannot drift silently. **Phase 2 complete in 0.1.4 after phase-end seam verification.**

## Phase 3 — Elicitation/compiler loop

Planned/implemented source:

```text
src/specgen/modes.py        named authoring policy profiles
src/specgen/elicitation.py  deterministic questions + guardrails
src/specgen/compiler.py     validated candidate finalization
```

- Express, guided, strict, and Agent-Workflow authoring profiles. **Implemented in 0.1.5.**
- Versioned `specgen/elicitation-plan/v1alpha1` with typed questions linked to affected paths/IDs. **Implemented in 0.1.5.**
- Structured candidate finalization only after canonical and mode guardrails pass. **Implemented in 0.1.5.**
- Agent-Workflow mode requires phased implementation, requirement/task coverage, task result contracts, evaluation intent, and resolved ambiguity. **Implemented in 0.1.5.**
- Full conversational/provider-driven question asking remains a later interaction-surface concern.

Exit signal: ambiguous intent can be deterministically assessed for readiness and finalized into a valid digest-bound snapshot without hiding unresolved decisions. **Phase 3 complete in 0.1.5 after phase-end seam verification.**

## Phase 4 — Repository-aware brownfield analysis

Planned/implemented source:

```text
src/specgen/repository.py  baseline + durable evidence/interface/contract discovery
src/specgen/drift.py       read-only comparison against a prior repository analysis
```

- Versioned `specgen/repository-analysis/v1alpha1` evidence report. **Implemented in 0.1.6.**
- Git commit or deterministic directory baseline binding. **Implemented in 0.1.6.**
- Durable interface/data-contract discovery: OpenAPI, protobuf, GraphQL, JSON Schema, Python console scripts, Node bins. **Implemented in 0.1.6.**
- Explicit spec-referenced repository evidence and missing-path contradictions. **Implemented in 0.1.6.**
- Versioned `specgen/repository-drift/v1alpha1` read-only drift report. **Implemented in 0.1.6.**
- Agent-Workflow mode target context from the declared/live dev source without runtime imports. **Implemented in 0.1.6.**
- Arbitrary source-code semantic inference is explicitly deferred; see ADR-0007.
- Extend the public CLI critical-seam integration at phase close. **Done in 0.1.6.**

Exit signal: repository evidence can be reproduced against a revision, durable public contracts can be surfaced without heuristic code parsing, and stale evidence is mechanically detectable. **Phase 4 complete in 0.1.6 after phase-end seam verification.**

## Phase 5 — Evaluation model

- Portable `specgen/evaluation-intent/v1alpha1` contract. **Implemented in 0.1.7; integrity-corrected in 0.1.8.**
- Public/hidden/external oracle separation. **Implemented in 0.1.7; integrity-corrected in 0.1.8.**
- Requirement ↔ acceptance ↔ evaluation traceability projection. **Implemented in 0.1.7; integrity-corrected in 0.1.8.**
- Additional behavior evals remain limited to critical skill seams; no new test surface was added in this release slice.

**Phase 5 implementation complete in 0.1.7; midpoint integrity corrected in 0.1.8. Testing intentionally not run by release instruction.**

## Phase 6 — Agent-Workflow adapter

- Lower representable implementation state to `agent-workflow/prompt-pack/v1`. **Implemented in 0.1.7; integrity-corrected in 0.1.8.**
- Lower evaluation intent to `agent-workflow/evaluation-plan/v1`. **Implemented in 0.1.7; integrity-corrected in 0.1.8.**
- Preserve structured task result contracts and deterministic prompt resources. **Implemented in 0.1.7; integrity-corrected in 0.1.8.**
- Validate generated target artifacts against pinned Agent-Workflow 0.9.0 schemas during compilation. **Implemented in 0.1.7; integrity-corrected in 0.1.8.**
- Repository source-baseline artifact emission remains a final-release follow-up where a concrete repository analysis is supplied.
- No new tests added or run in this slice by release instruction.

## Phase 7 — Skill + optional Agent-Workflow plugin

- Thin agent-facing authoring skill.
- Optional Agent-Workflow plugin registration.
- Digest-bound resources and capability discovery.

## Phase 8 — Interactive app/API

Only after CLI/contracts prove the interaction model: question ledger, evidence viewer, conflicts, snapshots/diffs/trace, provider abstraction, exports.

## Explicitly deferred

General execution engine, duplicated worker/review/acceptance lifecycle, database as sole authority, broad plugin/hook marketplace, or other orchestration not justified by a concrete requirement.
