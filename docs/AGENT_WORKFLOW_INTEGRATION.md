# Agent-Workflow Integration Architecture

> Document version: 0.2.0 · Applies to SpecGen 0.2.0

## Baseline

Branch and promotion handling follows [the accepted delivery workflow](DELIVERY_WORKFLOW.md): synchronize production first, rebase QA and work branches, use isolated worktrees, gate QA through Jenkins, and tag only the promoted production commit.

Release compatibility is pinned under `compat/agent-workflow/`; moving development source is observed separately through `dev/agent-workflow.toml`. Native target schema ownership is provided by the separately released `specgen-agent-workflow-contracts` bundle. SpecGen consumes it through `src/specgen/contract_bundle.py`, and generated packs declare the exact bundle version and schema digests in `workflow.requires`. The adapter targets Agent-Workflow `0.9.1` public contracts and never imports private Agent-Workflow Python implementation modules.

## Contract mapping

| SpecGen concern | Agent-Workflow 0.9.1 contract | Relationship |
|---|---|---|
| implementation phases/tasks/dependencies | `agent-workflow/prompt-pack/v1` | compile target |
| executable evaluation plan | `agent-workflow/evaluation-plan/v1` | compile target where faithfully representable |
| source/repository baseline | `agent-workflow/source-baseline/v1` | compile target from bound Git analysis |
| logical execution role | `agent-workflow/agent-role/v1` | optional target hint only |
| generic task result envelope | `agent-workflow/task-result/v1` | packaged result-contract schema |
| runtime state/provenance/status | documented public CLI/API contracts | black-box consumption only |
| optional hosting | Agent-Workflow trusted plugin API | Phase 7 adapter seam |

## Non-negotiable boundaries

1. No core import dependency on `agent_workflow.*`.
2. No duplicate Agent Run lifecycle, review authority, acceptance authority, worker supervision, or mutable status database.
3. No compatibility claim based only on accidental schema validation; product version and exact contract identities are pinned.
4. Agent-Workflow-specific execution fields remain adapter/extension concerns unless they independently belong to general specification semantics.
5. Lowering fails closed when target contracts cannot preserve material SpecGen meaning.

## 0.1.10 compiler surface

```bash
specgen agent-workflow compile SPEC \
  --output TARGET_DIR \
  [--repository-analysis ANALYSIS] \
  [--repository-root REPO]
```

Compilation requires an `agent-workflow`-ready canonical snapshot and an empty real output directory. This avoids stale resources surviving a later deterministic compile and prevents a symlink from redirecting generated pack files outside the selected root.

The output is an Agent-Workflow-native prompt-pack source tree:

```text
TARGET_DIR/
├── pack.yaml
├── README.md
├── EXECUTION_PROTOCOL.md
├── DELEGATION_RUNBOOK.md
├── evaluation-plan.json          # only when evaluation intent exists
├── source-baseline.json          # only when repository analysis is supplied
├── MANIFEST.sha256
├── result-contracts/
├── templates/
└── phase-*/
    ├── README.md
    ├── MASTER_IMPLEMENTATION_PROMPT.md
    └── tickets/
```

`pack.yaml` is emitted as deterministic JSON text, which is valid YAML and avoids adding a YAML dependency to SpecGen core.

The optional canonical `target_application_id` identifies the portable application being changed. It is a lowercase kebab-case identifier (1–63 characters), with one value per canonical snapshot; it is not derived from a path and does not replace the SpecGen `id` or Agent-Workflow `pack_id`. Agent-Workflow 0.9.1 has no application field in `prompt-pack/v1`, so the adapter preserves the identifier in generated README/task prompts while leaving `pack.yaml` and its legacy `pack_id` meaning unchanged. If it is absent, the target is intentionally unspecified; this supports a new or not-yet-existing application and does not imply that a repository baseline exists.

`MANIFEST.json` is intentionally absent from source prompt packs. Agent-Workflow reserves that filename for the canonical `agent-workflow/pack-manifest/v1` archive-integrity artifact created by its own `pack archive` operation. SpecGen emits the supported source checksum sidecar `MANIFEST.sha256` instead.

The existing `MANIFEST.sha256` covers the generated application-ID projections. Archive behavior therefore remains Agent-Workflow-owned and unchanged; no second canonical manifest or path-derived identity is introduced.

### Result contracts

Agent-Workflow requires `result_contract.schema` to be a normalized pack-relative path whose bytes are pinned at launch. SpecGen therefore packages the schema bytes under `result-contracts/` and writes the pack-relative path into each task.

The portable task contract currently lowers when `result_contract.schema` is either:

- the pinned `agent-workflow/task-result/v1` schema ID; or
- an inline JSON Schema object.

Unresolvable schema identifiers/paths or unsupported result-contract fields fail closed rather than leaving a dangling target reference.

### Source baseline

When repository provenance exists, compilation requires a valid `specgen/repository-analysis/v1alpha1` artifact bound to the exact canonical spec ID, snapshot ID, and digest. The analysis must use a Git baseline. SpecGen re-reads the live Git HEAD and dirty state, derives the branch, and refuses to emit a baseline if the repository drifted.

A directory-digest baseline cannot be faithfully expressed as Agent-Workflow's Git-oriented `source-baseline/v1`; compilation therefore fails rather than inventing a head or branch.

### Evaluation lowering

Portable evaluation commands lower to Agent-Workflow acceptance commands. Command-based evaluation uses the target `acceptance_commands` scorer. Explicit scorer names must be supported by Agent-Workflow `0.9.1`; multiple distinct per-evaluation scorer assignments are rejected because Agent-Workflow carries scorers globally.

Hidden/external oracles require digest-bound `metadata.oracle_ref = {id, sha256}`. SpecGen maps the evaluation through requirement/acceptance relationships to the implementation task IDs required by Agent-Workflow `oracle_refs`. If multiple incompatible oracles would target the same task, compilation fails.

Unknown evaluation metadata that cannot be represented is also a blocking diagnostic. The adapter does not silently union, drop, or relabel evaluation semantics.

## Development source linkage

Copy `dev/agent-workflow.example.toml` to ignored `dev/agent-workflow.toml`. `scripts/sync-agent-workflow-dev.py` resolves the live checkout, compares observed public surfaces with release fixtures, and materializes ignored links under `.dev/`.

Development drift is evidence requiring an explicit compatibility decision; it never silently rewrites release compatibility.

## Authoring mode vs target adapter

`specgen author assess --mode agent-workflow` is an authoring policy profile over `specgen/spec/v1alpha2`. It establishes implementation-readiness guardrails but is not the target compiler. Phase 6 then lowers the validated portable snapshot into Agent-Workflow resources without moving execution authority into SpecGen. See ADR-0006.

## Optional plugin direction

Agent-Workflow's public trusted plugin API is a suitable Phase 7 host seam. The plugin remains thin: expose SpecGen commands/resources and delegate to SpecGen core; do not duplicate the canonical model or execution lifecycle.

## Optional host plugin

SpecGen registers the optional `agent-workflow-spec` entry point in the public `agent_workflow.plugins` group. Agent-Workflow must explicitly enable it; normal SpecGen CLI/library use never imports Agent-Workflow. The adapter imports only `agent_workflow.plugin_api` inside `plugin()` and exposes one host command, `spec`, with compatibility, assess, analyze, finalize, and compile subcommands.

The host version must exactly match the pinned `0.9.1` compatibility target. A mismatch fails closed. The plugin is a trusted in-process adapter, not a security boundary or a second execution authority. No private `agent_workflow.*` modules are imported.

`PluginPackageResource` is intentionally not used for the initial integration because the plugin does not need Agent-Workflow to activate duplicate copies of SpecGen's canonical schemas/assets. If a future Agent-Workflow capability requires packaged activation, resources must be digest-bound to the SpecGen-owned bytes rather than forked.
