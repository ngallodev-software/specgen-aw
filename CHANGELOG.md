# Changelog

All notable changes are recorded here. Software releases use Semantic Versioning; machine contracts carry independent explicit identifiers.

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
