# ADR-0007 — Brownfield analysis is evidence-first and read-only

- Status: accepted
- Date: 2026-08-27
- Applies from: SpecGen 0.1.6

## Context

Repository-aware specification authoring needs current-system evidence without turning SpecGen into a language-indexer, build system, or execution engine. Arbitrary source-code pattern matching can look precise while producing false interface and contract claims.

## Decision

The deterministic brownfield layer is read-only and evidence-first.

It may:

- bind analysis to a Git commit or deterministic directory revision;
- hash evidence files it actually observed;
- recognize durable declared interfaces/contracts such as OpenAPI, protobuf, GraphQL, JSON Schema, Python console-script declarations, and Node `bin` declarations;
- include source/config/doc files explicitly referenced by a canonical spec;
- report missing referenced paths and other evidence-backed contradictions;
- compare a prior analysis to the current repository and report drift.

It must not claim semantic understanding of arbitrary application code from heuristic regex scans. Deeper semantic inference belongs to a later agent-assisted analysis layer and must remain distinguishable from deterministic evidence.

Agent-Workflow authoring may attach the currently declared Agent-Workflow target/version context, but the repository analyzer does not import Agent-Workflow runtime code.

## Consequences

The first analyzer is intentionally narrower than a code-intelligence product. Its findings are reproducible, revision-bound, and suitable as provenance inputs. New language-specific discovery should be added only when it recognizes a durable public declaration or protects a demonstrated seam.
