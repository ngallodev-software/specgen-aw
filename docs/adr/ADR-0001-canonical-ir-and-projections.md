# ADR-0001: Canonical Spec IR with derived projections

- Status: accepted
- Date: 2026-08-27

## Context

The product must produce human-readable specifications, machine-readable data/evals, and execution-target artifacts. Independently generated copies would drift.

## Decision

SpecGen owns one versioned canonical IR. Human Markdown, evaluation assets, and target-specific artifacts are derived projections/compilations.

## Consequences

- Renderers/adapters cannot become competing authorities.
- Normative prose must map back to canonical IDs/fields.
- Target-specific requirements live in adapter/extension space when they do not belong in general specification semantics.
