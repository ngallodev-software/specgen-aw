# Shared contract program notes — 2026-08-30

## Scope and approved boundary

The next architecture phase is a separately released, immutable shared
SpecGen-to-Agent-Workflow contract bundle. It owns only cross-application
semantic seams: shared schema bytes and IDs, canonicalization/normalization,
validation, descriptors/digests, feature/version negotiation, deterministic
migrations, and conformance fixtures.

SpecGen remains the canonical specification and target-pack author/compiler.
Agent-Workflow remains the native target interpreter and owns scheduling,
logical role/model selection, execution, durable lifecycle, evaluation, review,
and sealing. The bundle must not become a third application, generic CRUD
layer, or shared orchestration framework.

Generated Agent-Workflow targets must declare the exact immutable bundle
version and schema digest used by the compiler. Consumers reject mismatches
before execution. A bundle change affecting a shared artifact must include
deterministic migrations from every supported prior version. Migrations produce
provenance-linked derivatives and never rewrite sealed historical artifacts.

## Current evidence

- SpecGen currently compiles `agent-workflow/prompt-pack/v1`,
  `agent-workflow/evaluation-plan/v1`, `agent-workflow/source-baseline/v1`,
  `agent-workflow/task-result/v1`, and logical-role compatibility resources
  from `src/specgen/agent_workflow.py`.
- Agent-Workflow owns the native prompt-pack schema, validation, deterministic
  archive manifest, and runtime interpretation through
  `src/agent_workflow/manifests.py`, `src/agent_workflow/pack.py`, and its
  execution/lifecycle modules.
- SpecGen presently packages duplicate versioned Agent-Workflow schema
  fixtures under `compat/agent-workflow/`; these are the initial extraction
  candidates, subject to byte-for-byte conformance characterization.
- SpecGen has no portable non-Agent-Workflow task-pack output. `PORT-001`
  remains a separate target work item; it must not reuse the native
  Agent-Workflow manifest name or imply Agent-Workflow lifecycle authority.

## Observations and corrective actions

| Observation | Classification | Disposition |
|---|---|---|
| Shared user Python environment failed `pip check`: `inspect-ai 0.3.247` requires Click `<8.2.2`, while Click `8.5.0` is installed. | environment weakness | Kept the gate fail-closed; validated SpecGen in a fresh isolated environment instead. Do not alter SpecGen dependencies to mask an unrelated environment conflict. |
| The temporary SpecGen verification environment lacked the `build` module after editable install. | verification setup gap | Used the build-capable project interpreter for wheel/sdist and wheel-source checks; future clean-host verification should install the declared build tool explicitly. |
| `rtk` did not return a reusable long-running session for full pytest; it emitted partial output and ended its call window. | CLI/tool limitation | Used plain `python -m pytest` only for tracked long-running test execution, as permitted when RTK is incompatible; record this behavior in tooling guidance if it recurs. |
| Agent-Workflow's new rollback/watcher tests initially violated the repository test-authority manifest. | implementation process weakness | Added explicit authority records, bounded rationale, and the one additional subprocess budget; full release gate then passed. |
| The installed-product plugin journey assumed its fixture was the first discovered entry point. Installing SpecGen made its valid optional plugin sort first. | combined-install weakness | Fixed the test to select the named fixture candidate. The test now proves disabled candidates are not imported while allowing unrelated installed plugins. |
| Three stale tmux sessions and one merged clean Agent-Workflow worktree remained from old runs. | cleanup gap | Removed exactly those named sessions and the ancestor worktree after provenance/status checks. |

## Strengths to retain

- SpecGen already has narrow target compilation seams and digest-bound
  compatibility fixtures, making extraction bounded rather than a rewrite.
- Agent-Workflow already validates native packs and keeps execution/review/
  acceptance separate from generation.
- Both applications support fail-closed validation patterns that the shared
  bundle can reuse.

## Required phase gates

1. Characterize every shared artifact and choose the bundle namespace,
   repository, registry, signing, publication, and supported-version policy.
2. Publish bundle `0.x` with schemas, IDs, descriptor/digest, validation,
   negotiation, migration, and fixture-only surface; prove wheel content and
   immutability.
3. Move SpecGen compilation to the bundle and emit bundle provenance; retain
   its authoring/compiler ownership.
4. Move Agent-Workflow native validation and target consumption to the bundle;
   retain its runtime ownership.
5. Run cross-repository conformance for exact-version acceptance, mismatch
   rejection, supported migration, unsupported/manual migration failure, and
   sealed-artifact preservation.

Each phase needs independent review plus the existing application build,
install, schema, and relevant end-to-end checks before the next phase starts.
