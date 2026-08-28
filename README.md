<!-- document-version: 0.1.5; applies-to: SpecGen 0.1.5 -->
<div align="center">

# spec-gen
### *an agent-workflow joint*

**Turn ambiguous engineering intent into versioned specifications humans can review and agents can execute — without a 47-page manifesto.**

![Version](https://img.shields.io/badge/version-0.1.5-blue)
![Spec Schema](https://img.shields.io/badge/spec%20schema-v1alpha2-purple)
![Agent--Workflow](https://img.shields.io/badge/Agent--Workflow-0.9.0%20aware-2ea44f)
![Status](https://img.shields.io/badge/status-alpha-orange)

**Canonical JSON · append-only decisions · immutable snapshots · traceability · preservation · eval intent · target compilation**

</div>

> “*an agent-workflow joint*” is a deliberate nod to Spike Lee's “A Spike Lee Joint” credit: recognizable lineage, clear authorship, no claim that the work assembled itself.

## Do the right spec

Spec-gen is a machine-first specification authoring/compiler project. It keeps user decisions, source evidence, assumptions, requirements, acceptance, evaluation intent, and implementation structure explicit enough to validate and hand off without relying on chat memory.

**Current contracts:**

- project `0.1.5`;
- canonical snapshot `specgen/spec/v1alpha2`;
- retained compatibility snapshot `specgen/spec/v1alpha1`;
- authoring event `specgen/authoring-event/v1alpha1`;
- semantic delta `specgen/semantic-delta/v1alpha1`;
- elicitation plan `specgen/elicitation-plan/v1alpha1`;
- Agent-Workflow compatibility target `0.9.0`.

The basic rule: **if a decision matters later, it should survive the chat window.**

## Architecture at a glance

Authoring history, canonical state, projections, semantic deltas, and target adapters are separate authorities. See the single-source [authority-flow and snapshot diagrams](docs/ARCHITECTURE.md#authority-and-flow).

> **Spec-gen owns specification meaning. Execution targets own execution meaning.**

Agent-Workflow is the first-class compilation target, not a runtime dependency. See [Agent-Workflow integration](docs/AGENT_WORKFLOW_INTEGRATION.md).

## What `v1alpha2` adds

The first deliberate canonical revision adds stable lifecycle-aware IDs, current/proposed state, immutable snapshot identity, typed provenance, preservation coverage for load-bearing claims, and explicit invariants. `v1alpha1` remains unchanged for compatibility. See [versioning](docs/VERSIONING.md) and [architecture](docs/ARCHITECTURE.md#canonical-contract-boundaries).

## Working tree

```text
schemas/spec/        versioned canonical/event contracts
compat/              pinned external compatibility authority
dev/                 moving development-source declarations
docs/                focused reference docs + ADRs + research
examples/            minimal contract examples
scripts/              development/packaging helpers
src/specgen/          lean implementation core
```

Phases 1–3 now provide the deterministic contract core plus human projection/history/diff seams: `contracts.py`, `canonical.py`, `validate.py`, `render.py`, `history.py`, `diff.py`, `modes.py`, `elicitation.py`, and `compiler.py`. See the [roadmap](docs/ROADMAP.md).

Current CLI seams:

```bash
specgen contracts
specgen validate path/to/spec.json
specgen validate path/to/spec.json --json
specgen digest path/to/spec.json
specgen render path/to/spec.json [--output SPEC.md]
specgen diff before.json after.json
specgen events append events.ndjson event.json
specgen modes
specgen author assess spec.json --mode agent-workflow
specgen author finalize spec.json --mode agent-workflow --output finalized.json
```

## Engineering policy

Tests protect important seams, not a scorecard. Default to E2E and critical integration coverage; unit tests are exceptional. Tests are not run during ordinary checkpoints unless requested, and are run at phase-end only when the phase could have broken behavior.

Documentation is a versioned interface: focused, linked, non-duplicative, and updated when relevant claims change. Diagrams have one authoritative source. Code stays lean and architecture-backed.

See [ENGINEERING_POLICY.md](docs/ENGINEERING_POLICY.md).

## Opinionated Agent-Workflow authoring

`agent-workflow` mode is stricter than generic authoring: it requires phased tasks, requirement coverage, result contracts, evaluation intent, and resolved blockers so the result is shaped for later prompt-pack compilation. It remains a portable SpecGen snapshot; see [ADR-0006](docs/adr/ADR-0006-authoring-modes-and-agent-workflow-profile.md).

## Development against Agent-Workflow

```bash
python scripts/sync-agent-workflow-dev.py
SPECGEN_AGENT_WORKFLOW_ROOT=/path/to/agent-workflow python scripts/sync-agent-workflow-dev.py --check
```

The generated `.dev/` links observe a live checkout; they never rewrite release compatibility declarations. See [dev/README.md](dev/README.md).

## Reference

| Need | Go here |
|---|---|
| Architecture + canonical diagrams | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Engineering/testing/docs policy | [docs/ENGINEERING_POLICY.md](docs/ENGINEERING_POLICY.md) |
| Versioning/contracts | [docs/VERSIONING.md](docs/VERSIONING.md) |
| Agent-Workflow boundary | [docs/AGENT_WORKFLOW_INTEGRATION.md](docs/AGENT_WORKFLOW_INTEGRATION.md) |
| Roadmap | [docs/ROADMAP.md](docs/ROADMAP.md) |
| ADR history | [docs/adr/README.md](docs/adr/README.md) |
| Prior-art findings | [docs/research/PRIOR_ART_DEEP_REVIEW_01.md](docs/research/PRIOR_ART_DEEP_REVIEW_01.md) |

## Credits & influences

Spec-gen is intentionally built in public view of the ideas that influenced it.

Some concepts here are original combinations; others are adaptations of patterns that already exist in good open-source work. Where an idea came from somewhere recognizable, we would rather say so plainly than quietly sand off the serial numbers.

### Agent-Workflow

**Agent-Workflow** is the primary architectural relative and the first execution target for spec-gen.

Spec-gen borrows or aligns with several Agent-Workflow design ideas, including:

- explicit versioned machine contracts;
- JSON Schema as a public compatibility boundary;
- SHA-256-bound provenance and compatibility fixtures;
- deterministic artifacts and manifests;
- task/result contracts;
- evaluation-plan concepts;
- source baselines;
- logical execution roles;
- public interfaces over private implementation imports;
- the principle that execution state, evaluation state, review state, and acceptance state are different authorities.

The projects deliberately remain separate:

> **Agent-Workflow owns execution meaning. Spec-gen owns specification meaning.**

The subtitle **“an agent-workflow joint”** acknowledges that lineage without implying a runtime dependency.

### specBuilder

The open-source **specBuilder** project by `dshills` was one of the first systems we examined closely when shaping spec-gen.

Ideas under assessment or adapted in spirit include:

- structured specification elicitation;
- explicit typed requirements;
- stable requirement identifiers;
- requirement dependencies;
- acceptance criteria attached to requirements;
- traceability;
- versioned/immutable answer history;
- machine-readable and human-readable outputs.

Spec-gen does not adopt specBuilder's schema as its canonical model, but its work helped sharpen several questions about elicitation authority, history, traceability, and compilation.

### GitHub Spec Kit

**GitHub Spec Kit** is an important reference for specification-driven agent workflows.

Relevant inspiration includes:

- staged progression from specification to planning to tasks to implementation;
- keeping specification work distinct from implementation work;
- broad coding-agent interoperability;
- workflow ergonomics for turning intent into actionable engineering work.

Spec-gen's canonical authority differs: machine-readable structured state comes first, with Markdown treated as a projection rather than the primary specification authority.

### OpenSpec

**OpenSpec** influenced our thinking about brownfield change modeling.

Ideas being assessed include:

- explicit added / modified / removed requirement deltas;
- change-oriented specification workflows;
- scenario-linked requirements;
- representing evolution without pretending every change is a greenfield rewrite.

Spec-gen may ultimately expose delta artifacts while retaining a complete canonical specification as the primary authority.

### BMAD / bmad-spec

**BMAD**, particularly its `bmad-spec` workflow, is a useful reference for durable authoring memory.

Ideas under assessment include:

- append-only decision/history logs;
- separating durable decision memory from rendered specifications;
- deriving current specification state from an auditable sequence of decisions and constraints.

This is especially relevant to an unresolved spec-gen architecture question: whether authoring history should be represented primarily as immutable snapshots, append-only events, explicit deltas, or a combination.

### Cavekit

**Cavekit** is a useful counterweight to framework inflation.

Ideas that influenced the design conversation include:

- keeping the durable specification surface small;
- making invariants survive individual agent sessions;
- feeding implementation failures back into durable specification knowledge;
- requiring complexity to justify its context and maintenance cost.

That last point is now one of spec-gen's explicit design principles.

### Standards and common engineering practice

Spec-gen also builds on established, non-project-specific practices rather than reinventing them:

- **JSON Schema Draft 2020-12** for machine contract validation;
- **Semantic Versioning** concepts for software releases;
- explicit schema-version identifiers for compatibility;
- **Architecture Decision Records (ADRs)** for durable architecture decisions;
- cryptographic digests for provenance and reproducibility;
- traceability relationships between requirements, acceptance criteria, implementation tasks, and verification.

### Naming credit

The phrase:

> **spec-gen — an agent-workflow joint**

is a deliberate affectionate nod to filmmaker **Spike Lee's** long-running **“A Spike Lee Joint”** credit.

No association or endorsement is implied. We just appreciate a good authorship credit — especially one with more personality than “powered by.”

### Attribution policy

As the project evolves:

- substantial borrowed mechanisms should be credited here or in the relevant design/research document;
- copied or adapted source code must retain whatever notices its license requires;
- architectural inspiration should be distinguished from direct code reuse;
- prior-art assessments should record what was **retained, adapted, rejected, or deferred**;
- significant adaptations should be traceable through ADRs or research notes.

If we learn that an idea we believed was original has clear prior art, the right response is to update the credit — not defend the mythology.


---

## Project name

The current working public name is:

# **spec-gen**
### *an agent-workflow joint*

The product remains independently architected and may be used without Agent-Workflow. The subtitle reflects the shared design lineage and first-class compatibility target—not a runtime dependency. It is a credit, not a coupling mechanism.

---

<div align="center">

**Do the right spec. Trace the decisions. Compile with confidence.**

</div>
