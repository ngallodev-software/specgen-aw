# Versioning and Compatibility Policy

> Document version: 0.1.2 · Applies to SpecGen 0.1.2

## Project releases

SpecGen uses Semantic Versioning. Pre-1.0 releases may make breaking product/API changes, but every breaking change is recorded in the changelog and machine contracts retain explicit immutable identifiers.

Current release: `0.1.2`.

## Machine-readable contracts

Current canonical contract: `specgen/spec/v1alpha2`.

Retained compatibility contract: `specgen/spec/v1alpha1` (immutable).

Current authoring-event contract: `specgen/authoring-event/v1alpha1`.

Rules:

1. Every persisted canonical or event document contains `schema`.
2. Breaking field or semantic changes require a new contract identifier and a new schema file.
3. Existing published schema files are not rewritten to mean something new.
4. Additive changes stay within an identifier only when the contract explicitly permits unknown fields and old consumers remain safe.
5. Alpha/beta transitions require migration notes.
6. Stable `v1` waits for corpus/eval evidence that recurring structural breaks have stopped.

`v1alpha2` is the first deliberate revision of the canonical schema. It adds snapshot/state/provenance/preservation semantics and therefore advances the contract rather than mutating `v1alpha1`.

## Document/reference versions

Maintained architecture, help, man, and reference documents declare a document version and applicable project version. Increment the document version whenever its maintained content changes. Historical accepted ADRs are not rewritten for routine version alignment.

## External target compatibility

External target support pins product/version range, exact schema/API identifiers, compatibility status, assessment source, and vendored fixture digest where applicable. Unknown breaking versions fail closed.
