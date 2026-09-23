<!-- document-version: 0.2.9; applies-to: SpecGen 0.2.9 -->
<div align="center">

# SpecGen-AW

**Versioned specification authoring and compilation for reviewable human intent and executable agent workflows.**

![Version](https://img.shields.io/badge/version-0.2.9-blue)
![Spec Schema](https://img.shields.io/badge/spec%20schema-v1alpha2-purple)
![Agent--Workflow](https://img.shields.io/badge/Agent--Workflow-0.11.9%20target-2ea44f)
![Status](https://img.shields.io/badge/status-alpha-orange)
![License](https://img.shields.io/badge/license-Apache--2.0-green)

</div>

SpecGen is a machine-first specification authoring and compilation project. It
keeps user decisions, source evidence, requirements, acceptance criteria,
evaluation intent, implementation structure, provenance, and unresolved questions
explicit enough to validate, review, and hand off without relying on chat memory.

> **SpecGen owns specification meaning. Execution targets own execution meaning.**

Agent-Workflow is the first-class compilation target, not a runtime dependency.
SpecGen can therefore be used to author and validate specifications independently,
then compile a validated snapshot into Agent-Workflow-native prompt-pack resources
when execution is required.

## Current contracts

- project `0.2.9`;
- canonical snapshot `specgen/spec/v1alpha2`;
- retained snapshot `specgen/spec/v1alpha1`;
- authoring event `specgen/authoring-event/v1alpha1`;
- semantic delta `specgen/semantic-delta/v1alpha1`;
- elicitation plan `specgen/elicitation-plan/v1alpha1`;
- repository analysis `specgen/repository-analysis/v1alpha1`;
- repository drift `specgen/repository-drift/v1alpha1`;
- brownfield research plan `specgen/brownfield-plan/v1alpha1`;
- agent-assisted brownfield analysis `specgen/brownfield-analysis/v1alpha1`;
- evaluation intent `specgen/evaluation-intent/v1alpha1`;
- Agent-Workflow target `0.11.9`.

## Installation

Run `scripts/install.sh` from a checkout to create or reuse the per-user shared
environment at `${XDG_DATA_HOME:-$HOME/.local/share}/agent-tools/venv`. The
`specgen` executable is linked into `~/.local/bin`; the installer links the
SpecGen skills into the generic agent, Codex, Claude, Pi, and OpenCode skill
directories. If the local Agent-Workflow checkout is available, its pinned
compatible version is installed into the same environment. Set
`AGENT_TOOLS_VENV` or `SPECGEN_VENV` to override the environment location.

Published contract identifiers are versioned independently from the software release. `v1alpha1` remains immutable; `v1alpha2` is the current canonical contract.

The pinned `specgen-agent-workflow-contracts` dependency is installed directly
from its GitHub source repository.

## Quick start

```bash
specgen contracts
specgen validate spec.json
specgen author assess spec.json --mode agent-workflow
specgen render spec.json --output SPEC.md
specgen repo analyze /path/to/repo --spec spec.json --mode agent-workflow > repository-analysis.json
specgen brownfield plan /path/to/repo --spec spec.json --mode agent-workflow > brownfield-plan.json
specgen evals intent spec.json
specgen agent-workflow compile spec.json \
  --repository-analysis repository-analysis.json \
  --repository-root /path/to/repo \
  --output targets/agent-workflow
```

If the canonical spec contains repository provenance, Agent-Workflow compilation requires a repository analysis bound to the exact canonical snapshot. The live Git state is rechecked before `source-baseline.json` is emitted; stale or directory-only baselines fail closed.

The Agent-Workflow target directory is a native prompt-pack source tree. It includes phase/ticket resources, packaged result-contract JSON Schemas, `evaluation-plan.json` when representable, `source-baseline.json` when repository analysis is supplied, and `MANIFEST.sha256`. `MANIFEST.json` is intentionally not generated because Agent-Workflow reserves that filename for its own deterministic archive-integrity manifest.

SpecGen also ships a general agent skill at `skills/specgen/SKILL.md`, a targeted brownfield skill at `skills/specgen-brownfield/SKILL.md`, and an optional Agent-Workflow 0.11.9 plugin entry point, `agent-workflow-spec`. The plugin delegates to the same SpecGen API/CLI authorities; it does not create another specification model or make Agent-Workflow a SpecGen runtime dependency.

## Authoring modes

`express`, `guided`, `strict`, and `agent-workflow` are policy profiles over one canonical schema. `agent-workflow` is intentionally stricter: active requirements must be carried by implementation tasks and evaluation intent; tasks need structured result contracts; blockers must be resolved before target compilation.

Repository analysis is evidence-first and read-only. It recognizes durable declarations and explicitly referenced evidence; it does not pretend to semantically parse arbitrary source code. For existing systems, `specgen brownfield plan` adds a targeted research layer and automatically selects a graph-assisted strategy when the optional `codebase-memory-cli` executable is available. Semantic agent findings remain a separate `specgen/brownfield-analysis/v1alpha1` artifact rather than contaminating deterministic repository evidence.

## CLI surface

```text
specgen version
specgen compatibility
specgen contracts
specgen modes
specgen validate SPEC [--json]
specgen digest SPEC
specgen render SPEC [--output SPEC.md]
specgen diff BEFORE AFTER
specgen events append LOG EVENT
specgen author assess SPEC --mode MODE
specgen author finalize SPEC --mode MODE --output SPEC
specgen repo analyze REPO [--spec SPEC] [--mode MODE]
specgen repo drift ANALYSIS REPO
specgen brownfield capabilities
specgen brownfield plan REPO [--spec SPEC] [--mode MODE]
specgen evals intent SPEC
specgen agent-workflow compile SPEC --output DIR
    [--repository-analysis ANALYSIS] [--repository-root REPO]
```

## Architecture boundaries

Authoring events explain **why** state changed. The immutable canonical snapshot defines **what the specification means**. Markdown and semantic deltas are derived projections. Agent-Workflow prompt packs/evaluation/source-baseline resources are derived target artifacts and may not redefine canonical requirements.

See the canonical diagrams and responsibility table in [Architecture](docs/ARCHITECTURE.md), and the exact Agent-Workflow lowering rules in [Agent-Workflow Integration](docs/AGENT_WORKFLOW_INTEGRATION.md).

For programmatic integrations, `specgen.api` is the stable application facade over validation, authoring readiness/finalization, repository analysis/drift, brownfield planning/capability inspection, history, rendering/diffing, evaluation intent, compatibility inspection, and Agent-Workflow compilation.
It also provides small deterministic create/load/write/event conveniences; timestamps remain caller-supplied so the library does not hide provenance in wall-clock side effects.

## Engineering policy

Code stays lean and architecture-backed. Tests protect critical seams rather than a scorecard; E2E/integration coverage is preferred and unit tests are exceptional. Documentation is a maintained interface, diagrams have one authoritative source, and checkpoint overlays are self-applying and deletion-aware.

See [Engineering Policy](docs/ENGINEERING_POLICY.md).

## Documentation index

Browse the rendered [HTML documentation index](docs/index.html) or use the
authoritative Markdown links below.

| Need | Go here |
|---|---|
| Application usage | [docs/USAGE.md](docs/USAGE.md) |
| Brownfield authoring | [docs/BROWNFIELD_AUTHORING.md](docs/BROWNFIELD_AUTHORING.md) |
| Architecture and authority diagrams | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Engineering/testing/docs policy | [docs/ENGINEERING_POLICY.md](docs/ENGINEERING_POLICY.md) |
| Versioning/contracts | [docs/VERSIONING.md](docs/VERSIONING.md) |
| Branching, CI, release, and promotion flow | [docs/DELIVERY_WORKFLOW.md](docs/DELIVERY_WORKFLOW.md) |
| Agent-Workflow target boundary | [docs/AGENT_WORKFLOW_INTEGRATION.md](docs/AGENT_WORKFLOW_INTEGRATION.md) |
| Roadmap | [docs/ROADMAP.md](docs/ROADMAP.md) |
| ADR history | [docs/adr/README.md](docs/adr/README.md) |
| Prior-art assessment | [docs/research/PRIOR_ART_DEEP_REVIEW_01.md](docs/research/PRIOR_ART_DEEP_REVIEW_01.md) |

## Credits & influences

SpecGen openly credits the work that informed its architecture and integrations: Agent-Workflow, Codebase Memory CLI, specBuilder, GitHub Spec Kit, OpenSpec, BMAD/bmad-spec, Cavekit, JSON Schema, ADR practice, semantic-versioning concepts, and cryptographic provenance patterns. Substantial adaptations are classified as retain/adapt/reject/defer in the research notes; architectural inspiration is kept distinct from direct code reuse and license obligations.

