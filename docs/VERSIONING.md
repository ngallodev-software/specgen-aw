# Versioning and Compatibility Policy

> Document version: 0.2.0 · Applies to SpecGen 0.2.0

## Project releases

SpecGen uses Semantic Versioning. Pre-1.0 releases may make breaking product/API changes, but every breaking change is recorded in the changelog and machine contracts retain explicit immutable identifiers.

Current release: `0.2.0`.

## Machine-readable contracts

Current canonical contract: `specgen/spec/v1alpha2`.

Retained compatibility contract: `specgen/spec/v1alpha1` (immutable).

Current authoring-event contract: `specgen/authoring-event/v1alpha1`.
Current derived semantic-delta contract: `specgen/semantic-delta/v1alpha1`.
Current elicitation-plan contract: `specgen/elicitation-plan/v1alpha1`.
Current repository-analysis contract: `specgen/repository-analysis/v1alpha1`.
Current repository-drift contract: `specgen/repository-drift/v1alpha1`.
Current brownfield research-plan contract: `specgen/brownfield-plan/v1alpha1`.
Current agent-assisted brownfield-analysis contract: `specgen/brownfield-analysis/v1alpha1`.
Current evaluation-intent contract: `specgen/evaluation-intent/v1alpha1`.

Rules:

1. Every persisted canonical/event/derived contract contains `schema`.
2. Breaking field or semantic changes require a new contract identifier and a new schema file.
3. Existing published schema files are not rewritten to mean something new.
4. Additive changes stay within an identifier only when the contract explicitly permits unknown fields and old consumers remain safe.
5. Alpha/beta transitions require migration notes.
6. Stable `v1` waits for corpus/eval evidence that recurring structural breaks have stopped.

`v1alpha2` is the first deliberate canonical revision. It adds snapshot/state/provenance/preservation semantics and therefore advances the contract rather than mutating `v1alpha1`.

## Document/reference versions

Maintained architecture, help, development, compatibility, research, and reference documents carry the current project release marker. Historical accepted ADR bodies retain their historical version context and are superseded rather than rewritten for routine release alignment.

## External target compatibility

External target support pins product/version range, exact schema/API identifiers, compatibility status, assessment source, and vendored fixture digest where applicable. Unknown breaking versions fail closed.

Agent-Workflow `0.9.1` is the current first-class target. Target adapters may add target-required execution metadata, but a software release does not change the canonical contract unless canonical meaning itself changes.

Compatibility is recorded per application release in `compat/agent-workflow/compatibility.json`. Each retained release points to immutable, versioned fixture schemas and their digests. A new application release may reuse the same schema IDs when the public contract bytes are unchanged; a breaking schema change requires a new schema ID and fixture directory. Historical fixtures remain packaged so old packs and execution results can still be inspected and validated.

## Programmatic and host compatibility

`specgen.api` is the supported Python integration facade for the current pre-1.0 release line. Pre-1.0 API changes remain possible and must be recorded in the changelog. The optional `agent-workflow-spec` host adapter is pinned to Agent-Workflow `0.9.1`; a different host version requires explicit compatibility review rather than optimistic loading.
