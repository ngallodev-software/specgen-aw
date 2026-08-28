# Agent-Workflow Integration Architecture

> Document version: 0.1.8 · Applies to SpecGen 0.1.8

## Baseline

This repository's initial compatibility knowledge comes from the attached authoritative Agent-Workflow `0.9.0` Phase 8–9 development source snapshot dated 2026-08-27. Compatibility fixtures are copied byte-for-byte from that source and SHA-256 pinned in `compat/agent-workflow/compatibility.json`.

## Contract mapping

| SpecGen concern | Agent-Workflow 0.9.0 contract | Relationship |
|---|---|---|
| implementation phases/tasks/dependencies | `agent-workflow/prompt-pack/v1` | compile target |
| executable evaluation plan | `agent-workflow/evaluation-plan/v1` | compile target where representable |
| source/repository baseline | `agent-workflow/source-baseline/v1` | interoperate/reference |
| logical execution role | `agent-workflow/agent-role/v1` | optional target hint only |
| generic task result envelope | `agent-workflow/task-result/v1` | pattern/target contract |
| runtime state/provenance/status | documented public CLI `--json` contracts | black-box consumption only |
| optional hosting | Agent-Workflow trusted plugin API | future adapter/plugin |

## Non-negotiable boundaries

1. No core import dependency on `agent_workflow.*`.
2. No duplicate Agent Run lifecycle, review authority, acceptance authority, worker supervision, or mutable status database.
3. No claim of support for an Agent-Workflow version merely because an old schema still appears to validate. Product version and contract identity are both recorded.
4. Agent-Workflow-specific execution fields remain in adapter/extension space unless they independently belong to general specification semantics.

## Compatibility update workflow

When a new Agent-Workflow source/version is assessed:

1. Record exact product version and source revision/snapshot.
2. Compare every consumed/emitted public schema and public JSON contract.
3. Add new immutable fixtures under `compat/agent-workflow/<version>/`.
4. Record SHA-256 digests.
5. Classify each contract as unchanged/additive/breaking.
6. Update adapter behavior and migrations if required.
7. Run target-specific validation/integration corpus.
8. Only then mark the new version `verified`.

## Future plugin shape

Agent-Workflow 0.9.0's own plugin documentation uses `agent-workflow-spec` as an example command for “author and compile implementation specifications.” This is a strong fit for an optional thin host package. The plugin should expose SpecGen-owned schemas/templates as digest-bound package resources and delegate authoring/compilation to the independent SpecGen package.


## Development source linkage

During development, copy `dev/agent-workflow.example.toml` to the ignored
`dev/agent-workflow.toml`; it declares the expected Agent-Workflow product
version, tracked contract paths, and reference surfaces.

`scripts/sync-agent-workflow-dev.py` resolves the source root (optionally through
`SPECGEN_AGENT_WORKFLOW_ROOT`), validates observed versions/digests against the
checked-in compatibility fixture, and materializes ignored symlinks below `.dev/`.

This does not change release compatibility automatically. Drift is evidence requiring
an explicit compatibility decision.


## Agent-Workflow authoring mode

`specgen author assess --mode agent-workflow` is an authoring guardrail profile, not the Phase 6 adapter. It requires enough phased/task/result/evaluation structure for later prompt-pack-oriented compilation while preserving `specgen/spec/v1alpha2` as the portable authority. See [ADR-0006](adr/ADR-0006-authoring-modes-and-agent-workflow-profile.md).

## 0.1.8 compiler surface

`specgen agent-workflow compile SPEC --output DIR` emits a JSON-as-YAML `pack.yaml`, deterministic task prompt resources, and an `evaluation-plan.json` when portable evaluation intent is representable. Hidden/external oracle intent must provide `metadata.oracle_ref` with a digest-bound `{id, sha256}` reference; otherwise lowering fails closed with a compile diagnostic rather than silently discarding oracle semantics. Generated target artifacts are validated against the pinned Agent-Workflow 0.9.0 schemas before being written.
