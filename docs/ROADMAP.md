# Roadmap

> Document version: 0.1.1 · Applies to SpecGen 0.1.1

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

- Schema loader/validator for `v1alpha2` and authoring events.
- Stable-ID and referential-integrity checks.
- Trace and preservation coverage checks.
- Canonical JSON serialization/digest.
- Small known-good/known-bad corpus only where it protects critical validator seams.

Exit signal: canonical specs can be validated deterministically without an LLM.

## Phase 2 — Markdown projection + authoring history

- Deterministic `SPEC.md` projection.
- Append-only event persistence boundary from ADR-0005.
- Semantic diff between immutable snapshots.

Exit signal: canonical state, history, and human projection cannot drift silently.

## Phase 3 — Elicitation/compiler loop

- Express, guided, and strict/headless ambiguity policies (names provisional).
- Typed questions linked to affected spec paths/IDs.
- Structured candidate outputs validated before commit.
- Explicit assumptions and unresolved questions.

Exit signal: ambiguous intent can converge into a valid snapshot with traceable decisions.

## Phase 4 — Repository-aware brownfield analysis

- Evidence model for code/docs/config.
- Source revision/baseline binding.
- Existing interface/data-contract extraction.
- Requested-vs-current contradiction detection.
- Read-only evidence drift checks.

## Phase 5 — Evaluation model

- Portable evaluation-intent contract.
- Deterministic behavior evals for the authoring skill where they protect critical behavior.
- Public/hidden/external oracle separation.
- Requirement ↔ acceptance ↔ evaluation traceability.

## Phase 6 — Agent-Workflow adapter

- Lower representable implementation state to `agent-workflow/prompt-pack/v1`.
- Lower evaluation intent to `agent-workflow/evaluation-plan/v1`.
- Emit structured task result contracts where needed.
- Bind repository-aware work to source-baseline semantics.
- Validate against pinned fixtures.
- Add only critical black-box public-CLI integration coverage.

## Phase 7 — Skill + optional Agent-Workflow plugin

- Thin agent-facing authoring skill.
- Optional Agent-Workflow plugin registration.
- Digest-bound resources and capability discovery.

## Phase 8 — Interactive app/API

Only after CLI/contracts prove the interaction model: question ledger, evidence viewer, conflicts, snapshots/diffs/trace, provider abstraction, exports.

## Explicitly deferred

General execution engine, duplicated worker/review/acceptance lifecycle, database as sole authority, broad plugin/hook marketplace, or other orchestration not justified by a concrete requirement.
