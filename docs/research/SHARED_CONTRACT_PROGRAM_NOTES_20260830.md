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
| The shared installer found existing non-symlink `/home/nate/.local/bin/specgen` and `agent-workflow` launchers. | host-installation boundary | The committed apps installed successfully into the supported shared venv and its `pip check` passes, but the installer correctly refused to overwrite the host wrappers or continue its link-refresh step. Replace only with explicit operator approval. |
| Agent-Workflow retains an untracked `implementation-output/` tree from the prior prompt-pack execution. | clean-gate blocker | Preserve it as user-owned evidence; do not commit it because repository policy excludes one-off execution output. A clean start requires an explicit archive/delete/ignore decision. |
| The generated pack's normalized phase directory was not predictable from its phase name. | prompt-pack ergonomics gap | Launch tooling must read `pack.yaml` for the exact ticket prompt path; do not reconstruct generated resource paths. |
| Failed `delegate` attempts left a clean worktree, then a clean throwaway branch, before prompt-path and role validation failed. | Agent-Workflow cleanup weakness | Transactional Agent Run preparation works, but delegate-level worktree/branch creation needs equivalent rollback or documented reuse recovery. |
| `analysis` was a valid SpecGen role hint but not a configured Agent-Workflow runtime role. | contract mapping gap | The first execution used the configured `implementation` role without selecting a model; future target lowering needs a validated logical-role mapping or a neutral declared role. |
| Retry run `shared-contract-inventory-r1-20260830` could create and validate its handoff but could not commit because the headless Codex workspace sandbox could not write linked-worktree Git metadata outside its writable root. Host-side `git add` and commit succeeded immediately. | Agent-Workflow/Codex sandbox integration gap | Do not accept the partial retry. Configure the worker's writable Git administrative path or provide a documented coordinator-commit protocol with provenance before launching the bundle foundation task. |
| The retry's child MCP `pack_validate` request was blocked by the host approval policy even though the CLI validation route is available. | Agent runtime integration gap | Task prompts should prefer the installed CLI for local pack validation under non-interactive approval policies. |
| `delegate` treated an inline prompt as a path and attempted a worktree before failing with `ENAMETOOLONG`; retry then found the clean branch/worktree left behind. | Agent-Workflow CLI and rollback gap | Pass a short prompt file path today; make `delegate` reject non-path input before worktree creation or add an explicit inline-prompt option. |
| A local Agent-Workflow configuration with custom preferred Luna names and inherited named profiles was rejected because profiles were required to be preferred names, blocking all later CLI commands and a worker closeout. | configuration validation regression | Allow inactive named profiles; profile selection is already guarded by requested/preferred-name resolution. |

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

## Phase-1 disposition

The inventory task's generated `AC-001` wrongly includes the bundle wheel and
both application adapters, which are explicitly assigned to later tasks. Its
completed evidence is therefore retained as `partial`, rather than rewritten
as a false success. On 2026-08-30 the user explicitly authorized advancing to
the next phase after review of this mismatch; the bundle foundation remains
subject to its own independent completion, evaluation, review, and acceptance
gates.

## Parallel Agent-Workflow reliability gate

The completion-handoff and external-name-lease incident is not a shared-bundle
concern, but it directly affects safe consumption of generated prompt packs.
`COMP-001` and `LEASE-001` therefore run in parallel with bundle work and must
be reviewed before Agent-Workflow consumer integration/acceptance. They do not
change the bundle's schema, migration, or ownership surface.
