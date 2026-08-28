# Using SpecGen

> Document version: 0.2.0 · Applies to SpecGen 0.2.0 plus post-release development additions described here

SpecGen turns engineering intent into a canonical JSON specification that can be validated, reviewed as Markdown, compared across snapshots, grounded in repository evidence, and compiled for supported execution targets.

The canonical JSON snapshot is the authority. Markdown, elicitation plans, repository reports, brownfield research artifacts, evaluation intent, and Agent-Workflow prompt packs are projections or evidence; they do not replace the canonical specification.

## 1. Install and inspect the application

From a source checkout:

```bash
python -m pip install -e .
specgen version
specgen contracts
specgen modes
```

The normal authoring modes are:

- `express` — minimum ceremony for a narrow, already-understood request;
- `guided` — default; surfaces important gaps without making every gap a blocker;
- `strict` — unresolved questions and missing verification intent block finalization;
- `agent-workflow` — strict phased implementation authoring for later Agent-Workflow compilation.

## 2. Create or obtain a candidate specification

A candidate is a `specgen/spec/v1alpha2` JSON document. Start from `examples/minimal.spec.json`, an existing snapshot, or the Python API:

```python
from specgen.api import create_candidate, write_document

candidate = create_candidate(
    "billing-refund-change",
    "Billing refund behavior",
    created_at="2026-08-27T20:00:00Z",
    problem="Refund handling is inconsistent across the current flows.",
)
write_document("candidate.json", candidate)
```

Do not invent missing product decisions simply to fill fields. Keep unknowns explicit and let readiness assessment identify what still matters.

## 3. Assess what the specification still needs

```bash
specgen author assess candidate.json --mode guided
```

The command emits a machine-readable `specgen/elicitation-plan/v1alpha1`. Resolve useful questions by one of three routes:

1. ask the user when the answer is a product, policy, priority, or acceptance decision;
2. collect repository/document evidence when the answer already exists in the system;
3. leave the item unresolved when neither route can establish it safely.

For an implementation handoff to Agent-Workflow, assess with:

```bash
specgen author assess candidate.json --mode agent-workflow
```

That profile requires phased tasks, requirement/task coverage, result contracts, and evaluation intent.

## 4. Brownfield work: establish the current system before specifying the change

For an existing codebase, first create deterministic repository evidence:

```bash
specgen repo analyze /path/to/repo --spec candidate.json --mode guided \
  > repository-analysis.json
```

This report is deliberately conservative. It binds evidence to a repository baseline, hashes observed files, recognizes durable declarations/contracts, includes explicitly referenced files, and reports evidence-backed contradictions. It does not claim semantic understanding of arbitrary source code.

Then generate a targeted research plan:

```bash
specgen brownfield capabilities
specgen brownfield plan /path/to/repo --spec candidate.json --mode guided \
  > brownfield-plan.json
```

`brownfield plan` separates:

- questions that should be asked of the user;
- codebase research the agent should perform itself;
- focus areas derived from the specification and deterministic repository evidence;
- stop conditions that prevent unnecessary codebase exploration.

### Optional `codebase-memory-mcp` enhancement

If the `codebase-memory-mcp` executable is on `PATH`, `brownfield plan` selects the `codebase-memory-assisted` strategy and emits research tasks optimized for graph-based code intelligence. SpecGen does not require the dependency and does not assume that the MCP server is registered with the current agent; `specgen brownfield capabilities` reports binary availability while MCP registration remains an agent/runtime concern.

The dedicated skill at `skills/specgen-brownfield/SKILL.md` tells an agent how to use the available MCP tools efficiently. Its preferred sequence is:

```text
index/status -> graph schema -> one architecture overview -> narrow structural search
-> shallow call-path tracing -> decisive snippets/tests/contracts -> blast-radius check
-> concise brownfield analysis
```

The agent records semantic findings separately as `specgen/brownfield-analysis/v1alpha1`, binding the exact deterministic repository-analysis digest and distinguishing observed facts from strong or tentative inference. That artifact can then be cited from canonical provenance as `tool_output`/`inference`; it never replaces the deterministic `repository-analysis/v1alpha1` report.

If `codebase-memory-mcp` is unavailable, the plan falls back to the evidence-first repository workflow and targeted file/search tools.

## 5. Update the canonical specification

Use the collected user decisions and evidence to update the candidate. Preserve stable IDs for requirements, interfaces, acceptance criteria, tasks, and other semantic objects that survive a revision.

Important provenance should be represented in `provenance.sources`. For brownfield work, useful sources commonly include:

- the repository baseline or an explicitly referenced repository file;
- deterministic `repository-analysis.json`;
- agent-assisted `brownfield-analysis.json` as tool output/inference;
- user decisions authorizing desired behavior or preservation boundaries.

Authoring-history events can preserve why an important change was made:

```bash
specgen events append events.ndjson event.json
```

## 6. Validate and finalize

Validate at any point:

```bash
specgen validate candidate.json
specgen validate candidate.json --json
```

When readiness passes for the chosen mode:

```bash
specgen author finalize candidate.json --mode guided --output spec.json
```

Finalization binds the canonical content digest. Do not manually patch a finalized digest after editing; revise the candidate and finalize again.

## 7. Produce human review and change artifacts

```bash
specgen render spec.json --output SPEC.md
specgen diff prior-spec.json spec.json > semantic-delta.json
specgen evals intent spec.json > evaluation-intent.json
```

`SPEC.md` is for human review. `spec.json` remains the specification authority.

## 8. Check repository drift before reusing brownfield evidence

If time has passed or the repository changed:

```bash
specgen repo drift repository-analysis.json /path/to/repo
```

Regenerate repository analysis—and any semantic brownfield conclusions affected by the drift—when the report shows material change.

## 9. Compile an Agent-Workflow implementation pack

Use `agent-workflow` authoring mode before compilation. When the spec contains repository provenance, bind the finalized snapshot to a fresh repository analysis and provide the live repository root:

```bash
specgen repo analyze /path/to/repo --spec spec.json --mode agent-workflow \
  > repository-analysis.json

specgen agent-workflow compile spec.json \
  --repository-analysis repository-analysis.json \
  --repository-root /path/to/repo \
  --output targets/agent-workflow
```

The output directory must be empty. Compilation fails closed when required result/evaluation/source semantics cannot be represented faithfully.

Without repository provenance:

```bash
specgen agent-workflow compile spec.json --output targets/agent-workflow
```

## 10. Programmatic use

The supported Python facade is `specgen.api`:

```python
from specgen.api import (
    assess,
    analyze_repository,
    brownfield_plan,
    codebase_memory_capability,
    evaluation_intent,
    finalize_candidate,
    render_markdown,
    validate,
)
```

Use the API for integrations that need SpecGen behavior in-process. Do not create a second schema, persistence authority, or orchestration lifecycle around it unless a concrete requirement justifies a new architecture boundary.

## Practical authoring rule

For greenfield work, ask questions until intended behavior is explicit. For brownfield work, ask fewer implementation questions: investigate the existing code first, then ask the user only for decisions the code cannot legitimately make.
