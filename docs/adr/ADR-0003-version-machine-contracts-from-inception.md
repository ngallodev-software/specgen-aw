# ADR-0003: Version machine contracts from inception

- Status: accepted
- Date: 2026-08-27

## Decision

The project begins at SemVer `0.1.0`; the first canonical spec contract is `specgen/spec/v1alpha1`. Every persisted/exchanged machine document carries a schema identifier, and compatibility changes are explicit.

## Rationale

Retrofitting version identity after consumers exist creates ambiguity precisely where generated artifacts need deterministic behavior. Pre-stable contract naming lets the model evolve without pretending the first structure is final.
