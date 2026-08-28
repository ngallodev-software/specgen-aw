# ADR-0008 — Agent-assisted brownfield analysis stays separate and optional

- Status: accepted
- Date: 2026-08-27
- Applies after: SpecGen 0.2.0

## Context

ADR-0007 deliberately limits deterministic repository analysis to revision-bound evidence, durable declarations, and explicit references. Brownfield specification authoring still benefits from semantic code understanding: locating behavior, tracing callers/callees, identifying preservation risks, and discovering tests or data-flow seams.

`codebase-memory-mcp` provides a local code knowledge graph and agent-facing structural tools that can answer many of those questions more efficiently than repository-wide grep/read exploration. Making it a required SpecGen dependency, however, would couple canonical authoring to a third-party indexing runtime and blur deterministic evidence with agent inference.

## Decision

SpecGen adds a separate optional brownfield research layer.

- `specgen/repository-analysis/v1alpha1` remains unchanged and deterministic.
- `specgen/brownfield-plan/v1alpha1` describes user decision questions, research focus, tool preferences, efficiency guardrails, and stop conditions.
- `specgen/brownfield-analysis/v1alpha1` records agent-assisted semantic findings with evidence locators and explicit confidence.
- SpecGen may detect whether a `codebase-memory-mcp` executable is available and shape the plan accordingly, but it does not require the package and does not assume MCP registration.
- The agent/runtime chooses direct MCP tools when exposed and may use the tool's CLI fallback when available and permitted.
- Semantic findings may inform canonical provenance, requirements, preservation claims, risks, acceptance, and implementation structure, but only the canonical snapshot owns specification meaning.
- User decisions remain distinguishable from tool output and inference.

The preferred research sequence is narrow-first: establish graph/project state, inspect graph schema once, obtain one architecture overview, search to a small candidate set, trace shallow call paths, read decisive snippets/tests/contracts, assess blast radius, and stop when remaining uncertainty requires a user decision.

## Consequences

Brownfield agents can use high-leverage semantic code intelligence without turning SpecGen core into a source indexer. The application still works when `codebase-memory-mcp` is absent. Reviewers can distinguish reproducible repository evidence from agent interpretation, and a future code-intelligence provider can be added without redefining canonical specification authority.
