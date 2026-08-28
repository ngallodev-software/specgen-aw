# ADR-0005 — Authoring history uses events, immutable snapshots, and derived deltas

- Status: Accepted
- Date: 2026-08-27
- Decision owners: SpecGen maintainers

## Context

Prior-art review surfaced three strong but different persistence models:

1. specBuilder keeps immutable/versioned answers and append-only compiled snapshots.
2. BMAD `bmad-spec` treats an append-only `.memlog.md` as decision-of-record and re-derives the current spec.
3. OpenSpec separates current truth from explicit proposed change/delta artifacts.

Each solves a different problem. A single representation forced to serve audit history,
reproducible compilation, and human change review creates avoidable coupling.

## Decision

SpecGen will separate these concerns:

### 1. Append-only authoring event journal

User decisions, accepted assumptions, evidence observations, unresolved questions,
corrections, and explicit supersession events are recorded chronologically. Existing
events are not edited in place.

The journal preserves *why and when specification meaning changed*.

### 2. Immutable canonical snapshots

A successful compilation emits an immutable canonical `specgen/spec/<version>`
snapshot with a deterministic digest and links to the authoring event range/evidence
from which it was derived.

The snapshot preserves *exactly what the specification meant at a point in time*.

### 3. Derived semantic deltas

Human-reviewable added/modified/removed changes are derived by comparing canonical
snapshots. A delta may be materialized as an artifact, but it is not an independent
source of truth unless a future ADR explicitly introduces a proposal workflow.

The delta explains *what changed between two known states*.

## Consequences

- Markdown remains a derived projection and is not the history authority.
- Event history can preserve superseded decisions without polluting the current spec.
- Snapshots are reproducible and suitable for digest binding and external compilation.
- Brownfield reviews can use explicit semantic deltas without making patch syntax the
  sole specification representation.
- Elicitation persistence and canonical compilation are related but distinct APIs.
- The implementation must define stable event IDs, snapshot IDs, supersession
  semantics, and deterministic snapshot derivation before `v1beta1`.

## Rejected alternatives

### Mutable canonical document only

Simple, but loses authored decision history and makes provenance difficult.

### Event log only

Excellent audit history but inefficient as the only downstream machine contract;
consumers should not have to replay authoring history to know current truth.

### Snapshot only

Reproducible but weak at explaining why decisions changed.

### Delta/change folders as sole authority

Strong for review and brownfield work but cumbersome for consumers that need a full,
resolved current-state contract.

## Prior-art influence

- `dshills/specBuilder`: immutable answer versions, append-only snapshots, traceability.
- `bmad-code-org/BMAD-METHOD` `bmad-spec`: append-only decision memory and derived spec.
- `Fission-AI/OpenSpec`: current truth separated from proposed deltas.

This ADR adapts these mechanisms; it does not copy their schemas or persistence code.
