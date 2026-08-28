# Brownfield Specification Authoring

> Document version: 0.2.0 · Applies to SpecGen 0.2.0 plus post-release development additions described here

Brownfield authoring has two distinct evidence layers:

1. **deterministic repository evidence** — `specgen/repository-analysis/v1alpha1`;
2. **agent-assisted semantic analysis** — `specgen/brownfield-analysis/v1alpha1`.

Keeping them separate prevents a code-intelligence tool or agent inference from being mistaken for deterministic discovery.

## What the user should answer

Ask the user for information the repository cannot authorize:

- desired behavior and outcome;
- scope and explicit non-goals;
- preservation/compatibility promises;
- priority or policy choices between viable approaches;
- acceptance expectations when existing tests do not define the desired result.

Do not make the user act as a source-code index. Questions such as “which file handles this?”, “what calls this method?”, or “where is the schema?” should normally be answered through repository analysis.

## What the agent should investigate

Investigate only enough of the codebase to establish:

- the current behavior and its entry points;
- relevant callers/callees and component boundaries;
- interfaces, data contracts, persistence/configuration seams, and cross-service dependencies;
- existing tests or observable behavior that should be preserved;
- likely blast radius and implementation constraints;
- contradictions between requested/spec-declared behavior and current evidence.

Connectivity is evidence, not scope authorization. A highly connected symbol may identify risk without making every consumer part of the requested change.

## Efficient `codebase-memory-mcp` use

When the agent exposes `codebase-memory-mcp`, prefer graph queries over broad file enumeration. Current public tooling includes project indexing/status, structured graph search, call-path tracing, Git-diff impact mapping, read-only graph queries, graph schema inspection, source snippets, architecture summaries, and indexed code search. The tool's own guidance recommends discovering exact symbols before tracing them. See the upstream project documentation at <https://github.com/DeusData/codebase-memory-mcp> for the current tool surface.

Use this progression:

1. **Establish the project once.** List projects/index status; index only when necessary.
2. **Inspect graph shape once.** Use `get_graph_schema` before custom graph queries.
3. **Get one architecture overview.** Use it to choose likely packages/routes/components, not to summarize the repository for its own sake.
4. **Search narrowly.** Start from requirement language, interface names, route names, domain nouns, or explicit spec paths. Prefer structured symbol/route searches before grep-style text searches.
5. **Trace shallowly.** Start call-path traversal at depth 1–2. Increase depth only when a missing boundary materially affects the specification.
6. **Read decisive snippets.** Retrieve source only after symbols are identified. Read supporting tests/contracts/configuration where they establish behavior or preservation constraints.
7. **Assess blast radius.** Inspect incoming consumers and shared types/contracts. Use `detect_changes` only for an actual Git diff; it is not a substitute for proposed-change reasoning.
8. **Stop.** Once the material behavior, dependencies, risks, and unresolved user decisions are known, stop exploring adjacent code.

Avoid whole-graph dumps, exhaustive symbol inventories, deep traces by default, repeated architecture calls, or source reads that do not answer a specification question.

## Confidence discipline

The artifact also binds `repository_analysis_digest` to the exact deterministic report summarized by the brownfield plan. A `brownfield-analysis/v1alpha1` finding declares one of:

- `observed` — directly supported by code/declaration/graph evidence;
- `strong_inference` — multiple observations support the conclusion, but it is not a literal declaration;
- `tentative` — plausible and useful enough to record, but further evidence or a user decision is needed.

A user-authorized product decision is not an agent inference and should enter canonical provenance as user input/decision.

## Converting analysis into a specification

Do not copy the repository's architecture wholesale into the spec. Convert only material findings into:

- requirements and invariants;
- preserved behaviors;
- interfaces/data contracts;
- constraints and risks;
- acceptance/evaluation intent;
- implementation phases/tasks when the chosen authoring mode requires them.

Every important semantic conclusion should retain a path/symbol/tool evidence trail. Large code excerpts are unnecessary; record locators and digests where practical.

Before finalization or target compilation, check repository drift. If the baseline moved, revalidate the findings that materially support the proposed change.
