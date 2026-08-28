---
name: specgen-brownfield
description: Create evidence-grounded brownfield specifications efficiently, using codebase-memory-mcp when available to answer codebase questions before asking the user.
---

# SpecGen Brownfield Skill

Use this skill when authoring or revising a SpecGen specification for an existing repository. Prefer it when the request is a change to current behavior, a refactor with preservation requirements, an integration into an existing architecture, or any task where the implementation surface should be discovered before the spec is finalized.

Use the general `specgen` skill for canonical authority, validation, traceability, finalization, evaluation, and Agent-Workflow compilation. This skill adds the brownfield research policy.

## Primary rule

Ask the user **decision questions**. Investigate **code questions**.

User questions normally cover desired outcome, product/policy choices, scope, non-goals, compatibility promises, preservation boundaries, priority, and acceptance expectations.

Do not ask the user to identify files, symbols, call chains, schemas, internal dependencies, or existing tests when repository tools can answer those questions.

## Establish the authoritative baseline

Before semantic code investigation, run or obtain deterministic SpecGen repository analysis:

```bash
specgen repo analyze /path/to/repo --spec candidate.json --mode MODE > repository-analysis.json
specgen brownfield plan /path/to/repo --spec candidate.json --mode MODE > brownfield-plan.json
```

The deterministic report and the semantic analysis are different artifacts. Never merge arbitrary source-code inference into `repository-analysis/v1alpha1`.

If reusing an older repository report:

```bash
specgen repo drift repository-analysis.json /path/to/repo
```

Material drift requires re-checking affected semantic findings.

## Detect the enhanced path

First inspect the tools actually available to the agent. If `codebase-memory-mcp` MCP tools are exposed, use them directly.

If MCP tools are not exposed but the executable is available, `specgen brownfield capabilities` may report a CLI fallback. When shell execution is permitted, every upstream MCP operation can also be invoked through `codebase-memory-mcp cli ...`.

If neither is available, follow the same narrowing policy with ordinary repository search/read tools. Do not block brownfield authoring merely because codebase-memory-mcp is absent.

## Efficient codebase-memory-mcp sequence

### 1. Confirm index/project state

Use `list_projects` and `index_status`; call `index_repository` only if the target is not adequately indexed. Work against the exact repository the SpecGen baseline describes.

Do not repeatedly re-index during one research pass unless the repository actually changed.

### 2. Learn graph shape once

Call `get_graph_schema` before custom `query_graph` work. This tells you which labels/relationships actually exist in the indexed project and avoids speculative graph queries.

### 3. Get one architecture overview

Call `get_architecture` once near the start. Extract only the packages, routes, entry points, clusters, boundaries, or hotspots relevant to the requested behavior.

Do not turn the architecture response into a generic repository summary.

### 4. Narrow from spec language to candidate symbols

Use the brownfield plan's focus areas and requirement language. Search in this order when applicable:

1. structured `search_graph` for named classes/functions/methods/interfaces/routes;
2. semantic search if the installed tool exposes it and exact vocabulary is uncertain;
3. `search_code` for literals/config keys/error text or other evidence not represented structurally.

Keep a short candidate set. Prefer a handful of high-signal symbols over hundreds of matches.

### 5. Trace behavior shallowly

Use `trace_path` / `trace_call_path` around candidate symbols. Start at depth 1 or 2. Expand to depth 3+ only when a still-unanswered specification question crosses that boundary.

Inspect both incoming and outgoing relationships when preservation or blast radius matters.

Do not assume every reachable node is in scope.

### 6. Read decisive source, not files indiscriminately

Use `get_code_snippet` after `search_graph` has identified qualified symbols. Read ordinary files only for declarations/configuration/tests that the graph cannot provide or when surrounding context is necessary.

For each material claim, capture concise evidence such as:

- repository-relative path;
- qualified symbol or route;
- query/tool that established the relationship;
- digest when one is already available from deterministic evidence.

Do not paste large code excerpts into the spec or analysis artifact.

### 7. Establish tests, contracts, and consumers

Use graph relationships and targeted queries to identify existing tests, shared types/contracts, callers, routes, persistence/configuration boundaries, and cross-service links relevant to the change.

Treat existing tests as evidence of current behavior, not automatic authority for desired future behavior.

### 8. Assess blast radius deliberately

For an existing Git diff, `detect_changes` can map changed symbols and risk. Do not use it to invent a diff for a proposed change.

For proposed work, inspect incoming callers/consumers and shared interfaces using `trace_path`, `search_graph`, or read-only `query_graph` based on the graph schema.

Stop once the direct preservation risks and implementation boundaries needed by the spec are understood.

## Question policy during research

Before asking the user a question, classify it:

- **Code-answerable:** investigate first.
- **User decision:** ask now if it materially changes the spec.
- **Low impact / deferrable:** record as unresolved or defer until a later phase.

Good user questions are narrow and decision-shaped, for example: whether backward compatibility is required, which of two observable behaviors is intended, whether a migration is allowed, or which external behavior is the acceptance boundary.

Bad user questions offload repository exploration, for example: asking which controller owns a route or which service writes a table.

## Produce a structured semantic artifact

Record semantic findings as `specgen/brownfield-analysis/v1alpha1`. Bind `repository_analysis_digest` to the digest emitted in `brownfield-plan.json` so reviewers can identify the exact deterministic evidence report that preceded semantic analysis.

For every finding:

- classify it as architecture, behavior, entry point, dependency, data flow, interface, persistence, test coverage, risk, preservation, or unknown;
- mark confidence as `observed`, `strong_inference`, or `tentative`;
- include at least one tool/path/symbol/query evidence locator;
- attach affected SpecGen refs when known.

Put genuine unresolved decisions under `open_questions`. Set `needs_user_decision` true only when more repository analysis cannot legitimately settle the matter.

Validate the artifact:

```bash
specgen validate brownfield-analysis.json
```

## Feed findings into the canonical spec carefully

Use semantic analysis to update only material specification meaning. Typical translations are:

```text
observed current behavior -> context / provenance / preservation claim
shared public contract     -> interface or data_contract + preservation/requirement
required future behavior   -> requirement + acceptance/evaluation intent
high-risk dependency       -> constraint/risk and possibly implementation sequencing
user choice                -> decision/provenance, never agent inference
```

Do not reproduce the entire code architecture in the canonical spec.

When using the brownfield analysis as provenance, represent it as tool output/inference and keep the deterministic repository-analysis artifact separately identifiable.

## Efficiency guardrails

- one graph-schema inspection per research pass unless indexing materially changes;
- one architecture overview by default;
- search before trace, trace before broad source reads;
- start call traces at depth 1–2;
- expand only to answer a named spec question;
- prefer symbol/route/path locators over source excerpts;
- stop when remaining uncertainty is a user decision;
- never explore adjacent modules merely because the graph makes them easy to reach.

## Stop conditions

Stop and surface the issue when:

- the repository/index cannot be matched confidently to the intended source tree;
- deterministic repository drift makes prior evidence stale;
- the requested outcome is too ambiguous to choose a meaningful research focus;
- code evidence supports multiple materially different behaviors and only the user can choose;
- a preservation/compatibility decision is required before implementation scope can be determined;
- more graph exploration would add detail without changing requirements, acceptance, risk, or implementation boundaries.
