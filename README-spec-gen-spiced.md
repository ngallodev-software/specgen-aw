<div align="center">

# spec-gen
### *an agent-workflow joint*

**Turn ambiguous product and engineering intent into versioned, machine-readable specifications that humans can review and agents can execute — without making everyone read a 47-page manifesto first.**

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![Spec Schema](https://img.shields.io/badge/spec%20schema-v1alpha1-purple)
![Agent--Workflow](https://img.shields.io/badge/Agent--Workflow-0.9.0%20aware-2ea44f)
![Status](https://img.shields.io/badge/status-architecture%20%2F%20alpha-orange)
![License](https://img.shields.io/badge/license-see%20LICENSE-lightgrey)

**Canonical JSON · deterministic Markdown · traceability · eval intent · repository evidence · target compilation**

</div>

---

> **About the name:** “*an agent-workflow joint*” is a deliberate nod to Spike Lee’s signature “A Spike Lee Joint” credit. The ambition is similar in spirit: a recognizable point of view, a clear authorial method, and absolutely no interest in pretending the work assembled itself.

## What is spec-gen?

**spec-gen** is a specification authoring and compilation system for agentic software development.

It is designed to take incomplete, conversational, or repository-grounded intent and progressively turn it into a **versioned canonical specification** with explicit requirements, interfaces, data contracts, decisions, acceptance criteria, evaluation intent, implementation structure, provenance, and unresolved questions.

The canonical specification is machine-readable first. Human-readable documents, evaluation assets, and execution-target artifacts are projections of that same authority. One source of truth is enough; distributed screenplay notes are not a data model.

```text
 idea / request / repository / research
                  │
                  ▼
          ┌───────────────────┐
          │   elicitation     │
          │ evidence + intent │
          └─────────┬─────────┘
                    │
                    ▼
        ┌────────────────────────┐
        │  Canonical Spec IR     │
        │ specgen/spec/v1alpha1  │
        └──────────┬─────────────┘
                   │
       ┌───────────┼───────────────┬────────────────┐
       ▼           ▼               ▼                ▼
    SPEC.md     eval assets    trace / diffs    target adapters
                                                    │
                                      ┌─────────────┴─────────────┐
                                      ▼                           ▼
                              Agent-Workflow                 future targets
```

> **Spec-gen owns specification meaning. Execution targets own execution meaning.**

That boundary is foundational: spec-gen can understand and compile for Agent-Workflow without becoming dependent on Agent-Workflow's runtime or duplicating its execution authority.

---

## Do the right spec

AI coding systems are increasingly capable of implementation, but implementation quality is still constrained by the quality of the problem definition they receive.

A useful specification for agentic work needs more than a polished Markdown document. It needs to answer questions such as:

- What is actually required?
- What is explicitly *not* required?
- Which statements are user decisions, assumptions, repository facts, or inferred conclusions?
- Which interfaces and data contracts must remain compatible?
- How does each task trace back to a requirement?
- How will each important requirement be verified?
- Which uncertainties are unresolved rather than silently invented?
- What source revision was the specification based on?
- Can the same spec be rendered for humans and compiled for an execution system without drift?

**spec-gen is being built around those questions.** The goal is not more ceremony. The goal is fewer expensive misunderstandings wearing a confident tone.

---

> **The basic rule:** if a decision matters later, it should survive the chat window.

## Core model

The canonical contract begins at:

```text
specgen/spec/v1alpha1
```

The current model includes first-class structures for:

| Area | Examples |
|---|---|
| **Intent** | problem, objectives, desired outcomes, non-goals |
| **Scope** | included, excluded, protected, constraints |
| **Requirements** | functional, non-functional, priority, rationale |
| **Interfaces** | APIs, CLIs, events, files, protocols, compatibility boundaries |
| **Data contracts** | schemas, formats, ownership, compatibility |
| **Decisions** | decision, rationale, alternatives, status |
| **Acceptance** | measurable criteria linked to requirements |
| **Evaluations** | verification intent, datasets, oracles, expected behavior |
| **Implementation** | phases, tasks, dependencies, expected outputs |
| **Risks** | failure modes, mitigations, unknowns |
| **Questions** | unresolved decisions kept explicit |
| **Traceability** | requirement → acceptance → task → evaluation |
| **Provenance** | source evidence, repository baseline, digests |
| **Extensions** | target-specific metadata without polluting the core model |

The schema is intentionally **pre-stable**. Breaking changes are expected during the `v1alpha*` period and will be versioned explicitly.

---

## Designed for agentic engineering

Spec-gen is not a document generator with JSON bolted on afterward and called “structured.”

It is designed around durable, machine-checkable specification behavior.

### Canonical machine authority

```text
Canonical JSON
    ├──► deterministic Markdown
    ├──► evaluation artifacts
    ├──► execution-target artifacts
    └──► semantic diff / trace views
```

Markdown is a projection. It is never allowed to become a second competing source of truth.

### Structural traceability

Important relationships should survive compilation:

```text
REQ-014
  ├── AC-021
  ├── TASK-008
  └── EVAL-006
```

The goal is not merely to *mention* traceability, but to make missing or broken relationships mechanically detectable. “It was somewhere in the chat” is not a traceability strategy.

### Explicit uncertainty

Unknowns belong in the model.

Spec-gen should prefer:

```text
UNRESOLVED-004: Authentication provider selection has not been decided.
```

over inventing an implementation detail that was never authorized. Confidence is not a substitute for a decision record.

### Repository-grounded brownfield specs

A specification for an existing system should be able to distinguish:

```text
requested behavior
      │
      ├── repository evidence
      ├── existing contracts
      ├── compatibility constraints
      └── contradictions / migration requirements
```

and bind that analysis to the source revision it actually examined.

### Evaluation-aware from the beginning

Verification is part of specification authoring, not something added after implementation.

```text
requirement
    ↓
acceptance criterion
    ↓
verification method
    ↓
evaluation / test / oracle
```

### Failure can improve the specification

One design direction under active assessment is **failure backpropagation**: when implementation or evaluation reveals a missing invariant, ambiguity, or false assumption, that information should flow back into durable specification knowledge instead of disappearing in an agent transcript.

---

## Agent-Workflow aware, not joined at the hip

The initial compatibility target is **Agent-Workflow `0.9.0`**.

Spec-gen tracks compatibility against exact public Agent-Workflow contracts rather than importing Agent-Workflow internals.

Currently recognized targets include:

```text
agent-workflow/prompt-pack/v1
agent-workflow/evaluation-plan/v1
agent-workflow/source-baseline/v1
agent-workflow/agent-role/v1
agent-workflow/task-result/v1
```

Compatibility fixtures are pinned under:

```text
compat/agent-workflow/0.9.0/
```

and are SHA-256-bound so compatibility can be tested against the contract version we actually designed for.

The intended lowering model is:

```text
specgen/spec/v1alpha1
          │
          ▼
 Agent-Workflow adapter
          │
          ├──► prompt-pack/v1
          ├──► evaluation-plan/v1
          ├──► task result schemas
          └──► source-baseline semantics
```

Spec-gen does **not** own Agent Runs, workers, review state, acceptance state, process supervision, or workflow execution.

Agent-Workflow does.

---

## Versioning is part of the architecture

Versioning starts on day one. Future us should not need forensic archaeology to discover what `spec.json` meant six months earlier.

Current identities:

```text
Project release:       0.1.0
Canonical spec schema: specgen/spec/v1alpha1
Agent-Workflow target: 0.9.0
```

Three version axes are intentionally separate:

1. **Project version** — the spec-gen software release.
2. **Contract version** — the canonical machine schema and related public contracts.
3. **Target compatibility** — the external contract versions a given release knows how to compile to.

A new spec-gen release does not automatically imply a new spec schema.

Likewise, support for a newer Agent-Workflow release does not require spec-gen's canonical model to become Agent-Workflow-shaped.

See [`docs/VERSIONING.md`](docs/VERSIONING.md).

---

## Architecture decisions are durable

Significant architectural decisions are recorded as ADRs.

Current accepted decisions include:

- canonical IR with derived projections;
- Agent-Workflow as a versioned compilation target, not a runtime dependency;
- machine contracts versioned from inception;
- significant design changes recorded through ADRs.

```text
docs/adr/
├── ADR-0001-canonical-ir-and-projections.md
├── ADR-0002-agent-workflow-is-a-versioned-target-not-a-dependency.md
├── ADR-0003-version-machine-contracts-from-inception.md
└── ADR-0004-significant-decisions-use-adrs.md
```

The design is expected to evolve. The decision history should not disappear when it does. Architecture amnesia is still amnesia, even when Git has all the commits.

---

## Prior-art driven, not prior-art copied

Spec-gen is being developed after source-level assessment of existing specification and agent-planning systems.

Current research candidates include:

- **specBuilder** — structured elicitation, typed requirements, traceability, immutable answers/snapshots;
- **GitHub Spec Kit** — staged specification → planning → task workflows and broad agent ergonomics;
- **OpenSpec** — explicit requirement deltas and brownfield change semantics;
- **BMAD / bmad-spec** — append-only decision memory and derived specifications;
- **Cavekit** — small durable spec surface and failure-to-invariant feedback;
- additional SDD, planning, eval, and agent-development systems as useful mechanisms emerge.

The research question is not *which framework wins?* This is not fantasy football for agent frameworks.

It is:

> **Which mechanisms actually improve correctness, traceability, portability, and agent execution enough to justify their complexity?**

Each mechanism is intended to be classified as:

```text
retain  ·  adapt  ·  reject  ·  defer
```

with rationale and licensing implications recorded.

---

## Planned authoring loop

The working direction is an iterative compiler rather than a one-shot prompt followed by a ceremonial `looks good`:

```text
                ┌──────────────────┐
                │ user intent      │
                │ repository facts │
                │ external sources │
                └────────┬─────────┘
                         ▼
                 detect uncertainty
                         │
                         ▼
                 ask / infer / record
                         │
                         ▼
                  validate structure
                         │
             ┌───────────┴───────────┐
             │                       │
         unresolved              sufficient
             │                       │
             └─────── loop ◄─────────┘
                                     │
                                     ▼
                              compile artifacts
```

The eventual system should distinguish user-authorized decisions from evidence-derived facts and model-generated proposals.

---

## Repository layout

```text
spec-gen/
├── VERSION
├── CHANGELOG.md
├── README.md
├── pyproject.toml
├── schemas/
│   └── spec/
│       └── v1alpha1.schema.json
├── compat/
│   └── agent-workflow/
│       ├── COMPATIBILITY.md
│       ├── compatibility.schema.json
│       ├── compatibility.json
│       └── 0.9.0/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DESIGN_PRINCIPLES.md
│   ├── VERSIONING.md
│   ├── AGENT_WORKFLOW_INTEGRATION.md
│   ├── ROADMAP.md
│   ├── adr/
│   └── research/
├── examples/
└── src/
    └── specgen/
```

---

## Current status

**0.1.0 is an architecture-first foundation release.** In movie terms, we have the script, storyboards, production rules, and continuity bible. We are not claiming the helicopter shot exists yet.

Already present:

- versioned `specgen/spec/v1alpha1` JSON Schema;
- explicit project/schema/target version separation;
- Agent-Workflow `0.9.0` compatibility manifest;
- pinned Agent-Workflow public schema fixtures;
- architecture and design-principle documentation;
- ADR process and initial accepted ADRs;
- prior-art assessment framework;
- valid example canonical specification;
- minimal Python package and compatibility inspection CLI.

Current CLI surface:

```bash
python -m specgen version
python -m specgen compatibility
```

Not yet claimed as implemented:

- interactive elicitation;
- repository analysis;
- deterministic Markdown rendering;
- semantic diff/history;
- evaluation generation;
- Agent-Workflow compilation;
- interactive UI/API.

Those are roadmap work and will move into this README only as they become real.

---

## Roadmap — no montage required

```text
0  Foundation + prior art
1  Canonical IR + deterministic validation
2  Markdown projection + authoring history
3  Elicitation / compiler loop
4  Repository-aware brownfield analysis
5  Evaluation model
6  Agent-Workflow compiler
7  Agent skill + optional AW plugin
8  Interactive app / API
```

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for current exit criteria and deferred work.

---

## Design principles

1. **Machine-readable authority first.**
2. **One canonical specification model.**
3. **Human documents are deterministic projections.**
4. **Uncertainty must remain visible.**
5. **Evidence and inference are different things.**
6. **Traceability should be mechanically checkable.**
7. **Evaluation belongs in the specification lifecycle.**
8. **External execution systems are targets, not hidden dependencies.**
9. **Compatibility is explicit and versioned.**
10. **Significant architecture decisions leave an ADR trail.**
11. **Prefer deterministic validation over model judgment where possible.**
12. **Complexity must earn its context and maintenance cost.**

See [`docs/DESIGN_PRINCIPLES.md`](docs/DESIGN_PRINCIPLES.md).

---

## The long-term shot

A useful end state looks something like this:

```bash
spec-gen init
spec-gen analyze --repo .

spec-gen author \
  --request feature-request.md \
  --repo .

spec-gen validate spec.json
spec-gen render spec.json --format markdown
spec-gen eval compile spec.json

spec-gen compile spec.json \
  --target agent-workflow@0.9.0
```

producing a portable artifact set such as:

```text
my-feature.spec/
├── spec.json
├── SPEC.md
├── decisions/
├── schemas/
├── evals/
├── evidence/
├── targets/
│   └── agent-workflow/
│       ├── pack.yaml
│       └── evaluation-plan.json
└── MANIFEST.json
```

Eventually, the question should not be:

> “Which version of the requirements did the agent mean?”

That is a sequel nobody asked for.

The better question is:

> **“Does the validated specification accurately encode what we decided, what the evidence supports, what remains unknown, and how we will know the implementation is correct?”**

---

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Design principles](docs/DESIGN_PRINCIPLES.md)
- [Versioning](docs/VERSIONING.md)
- [Agent-Workflow integration](docs/AGENT_WORKFLOW_INTEGRATION.md)
- [Roadmap](docs/ROADMAP.md)
- [Architecture decisions](docs/adr/README.md)
- [Prior-art research](docs/research/PRIOR_ART.md)
- [Assessment matrix](docs/research/ASSESSMENT_MATRIX.md)

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
