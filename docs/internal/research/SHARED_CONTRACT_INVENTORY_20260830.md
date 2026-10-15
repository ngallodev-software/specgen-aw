# Shared contract seam inventory

Baseline captured 2026-08-30 for the first shared-contract release. The
Agent-Workflow source reference is the immutable 0.9.1 snapshot
`agent-workflow-0.9.1-release-tooling-b5e73c9` (`b5e73c95384b840527999b23727053a5db26adae`).
This is an extraction inventory, not a claim that the bundle already exists.

## File-by-file inventory

### SpecGen (`specgen-aw`)

| File | Disposition | Reason/evidence |
| --- | --- | --- |
| `compat/agent-workflow/0.9.0/schemas/pack.schema.json` | extract as historical fixture | `agent-workflow/prompt-pack/v1`; byte-identical to 0.9.1. |
| `compat/agent-workflow/0.9.0/schemas/evaluation-plan.schema.json` | extract as historical fixture | `agent-workflow/evaluation-plan/v1`; byte-identical to 0.9.1. |
| `compat/agent-workflow/0.9.0/schemas/source-baseline.schema.json` | extract as historical fixture | `agent-workflow/source-baseline/v1`; byte-identical to 0.9.1. |
| `compat/agent-workflow/0.9.0/schemas/agent-role-v1.schema.json` | extract as historical fixture | `agent-workflow/agent-role/v1`; byte-identical to 0.9.1. |
| `compat/agent-workflow/0.9.0/schemas/task-result.schema.json` | extract as historical fixture | `agent-workflow/task-result/v1`; byte-identical to 0.9.1. |
| `compat/agent-workflow/0.9.1/schemas/pack.schema.json` | extract as release fixture | Current compiler input; digest frozen by `SNAPSHOT.json`. |
| `compat/agent-workflow/0.9.1/schemas/evaluation-plan.schema.json` | extract as release fixture | Current compiler input; digest frozen by `SNAPSHOT.json`. |
| `compat/agent-workflow/0.9.1/schemas/source-baseline.schema.json` | extract as release fixture | Current compiler input; digest frozen by `SNAPSHOT.json`. |
| `compat/agent-workflow/0.9.1/schemas/agent-role-v1.schema.json` | extract as release fixture | Current compiler input; digest frozen by `SNAPSHOT.json`. |
| `compat/agent-workflow/0.9.1/schemas/task-result.schema.json` | extract as release fixture | Current compiler input; digest frozen by `SNAPSHOT.json`. |
| `compat/agent-workflow/0.9.0/SNAPSHOT.json` | retain as provenance evidence | Captures source commit, schema digests, and dependency context. |
| `compat/agent-workflow/0.9.1/SNAPSHOT.json` | retain as provenance evidence; replace with bundle metadata after migration | Captures source commit, schema digests, and dependency context. |
| `compat/agent-workflow/0.9.0/SOURCE.json` | retain as provenance evidence | Captures compatibility snapshot/archive identity. |
| `compat/agent-workflow/0.9.1/SOURCE.json` | retain as provenance evidence | Captures compatibility snapshot/archive identity. |
| `compat/agent-workflow/compatibility.json` | retain as application support policy; adapt to bundle provenance | Application-version compatibility is not bundle authority. |
| `src/specgen/agent_workflow.py` | narrow adapter; remove local schema loading in extraction phase | Compiles target artifacts and validates against vendored bytes today; does not run workers. |
| `src/specgen/contracts.py` | narrow adapter | Exposes contract lookup and compatibility projection. |
| `src/specgen/canonical.py` | split shared canonicalization helper from SpecGen snapshot digest | Generic canonical bytes/digest behavior is a shared seam; snapshot semantics remain SpecGen-owned. |
| `src/specgen/validate.py` | retain SpecGen validator; delegate shared artifact validation | Validates canonical SpecGen documents and references. |
| `src/specgen/api.py`, `src/specgen/cli.py` | retain application API/CLI; call bundle through adapter | Authoring and compilation remain SpecGen authority. |
| `docs/AGENT_WORKFLOW_INTEGRATION.md`, `docs/VERSIONING.md` | retain and update boundary/provenance documentation | Defines target adapter and version policy. |

### Agent-Workflow (`agent-workflow`)

| File | Disposition | Reason/evidence |
| --- | --- | --- |
| `schemas/pack.schema.json` | extract shared schema bytes; semantic owner remains Agent-Workflow | `agent-workflow/prompt-pack/v1`; consumed by compiler and runtime. |
| `schemas/evaluation-plan.schema.json` | extract shared schema bytes | Cross-application evaluation intent handoff. |
| `schemas/source-baseline.schema.json` | extract shared schema bytes | Cross-application Git provenance handoff. |
| `schemas/agent-role-v1.schema.json` | extract shared schema bytes | Logical role compatibility hint; runtime resolution remains Agent-Workflow. |
| `schemas/task-result.schema.json` | extract shared schema bytes | Structured implementation-result handoff. |
| `src/agent_workflow/manifests.py` | retain application owner; consume bundle validation/digests | Native manifest interpretation and archive behavior remain runtime authority. |
| `src/agent_workflow/pack.py` | retain application owner; consume bundle schema/validation seam | Pack loading, interpretation, and execution preparation remain runtime authority. |
| `docs/PUBLIC_JSON_API.md` | retain application public API | Runtime status/evaluation/review projections are not bundle contracts. |
| `docs/PLUGIN_API.md` | retain application host API | Plugin loading is an application lifecycle concern. |
| `docs/PROMPT_PACKS.md` | retain application semantics; link bundle IDs | Pack layout and interpretation remain Agent-Workflow-owned. |
| `docs/ARCHITECTURE.md` | retain authority evidence | Explicitly assigns scheduling, execution, evaluation, review, acceptance, and sealing to Agent-Workflow. |

The braces in the table are literal file groups; the baseline JSON records
each file separately. No private Agent-Workflow module is a proposed bundle
public import.

## Approved bundle surface and ownership

The machine-readable freeze of this API and ownership decision is
[`SHARED_CONTRACT_SURFACE_20260830.json`](SHARED_CONTRACT_SURFACE_20260830.json).
It is intentionally a design/boundary artifact; it does not publish a bundle
or grant either application permission to import private modules.

The separately released bundle has the following public surface, with stable
namespaced IDs and immutable versioned bytes:

| Surface | Bundle owns | SpecGen owns | Agent-Workflow owns |
| --- | --- | --- | --- |
| schemas and IDs | schema bytes, `$id` values, references, supported versions | canonical SpecGen schemas and authoring model | native runtime/lifecycle schemas not crossing the boundary |
| normalization | deterministic JSON normalization/canonical bytes | snapshot meaning and authoring events | runtime state normalization |
| validation | reusable validation and actionable diagnostics for bundle artifacts | authoring/readiness validation | lifecycle, execution, and sealed-evidence validation |
| descriptors/digests | artifact descriptor format and deterministic digest helpers | source/snapshot provenance | runtime receipt/seal digests |
| negotiation | bundle version, schema digest, and feature compatibility checks | compiler declaration of required bundle provenance | pre-execution consumer verification |
| migrations | explicit version-to-version transforms, provenance, fail-closed unsupported cases | migration requests from compiler outputs | migration requests for consumed artifacts; never rewrite sealed history |
| conformance fixtures | immutable valid/invalid fixtures and expected outcomes | compiler adapter conformance | runtime consumer conformance |
| target compilation | — | canonical authoring and target-pack compilation | — |
| scheduling/execution | — | — | task scheduling, role/model resolution, workers, lifecycle, logging |
| evaluation/review/sealing | — | — | evaluation execution, review, acceptance, immutable sealing |

### Narrow adapter rules

SpecGen imports only the documented bundle package/CLI surface for shared
artifacts. It emits bundle version and exact schema digest in generated target
provenance, while retaining canonical authoring and compilation. Agent-Workflow
imports the same documented surface for schema validation, negotiation, and
supported migrations, while retaining runtime interpretation and lifecycle.
Neither application imports the other application's private Python modules.

The bundle must not expose scheduler, worker launch, model selection, task
authoring, repository mutation, evaluation execution, review disposition,
acceptance, sealing, or generic CRUD APIs. A bundle release is immutable; a
changed shared artifact requires a new release and migrations from every
supported prior release.

## Baseline and next gate

The exact per-file baseline is
[`SHARED_CONTRACT_FIXTURE_BASELINE_20260830.json`](SHARED_CONTRACT_FIXTURE_BASELINE_20260830.json).
It is intentionally based on the clean pinned Agent-Workflow snapshot rather
than the current development checkout. Before extraction, the bundle release
gate must reproduce these bytes, validate valid/invalid fixtures in both
applications, and prove exact-match acceptance plus digest/version mismatch
rejection.
