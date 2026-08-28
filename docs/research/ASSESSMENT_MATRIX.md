# Prior-Art Mechanism Assessment Matrix

> Document version: 0.2.0 · Applies to SpecGen 0.2.0

This is the comparison frame for the deep review. Statuses are hypotheses until source-level assessment is complete.

| Mechanism | specBuilder | Spec Kit | OpenSpec | Cavekit | BMAD bmad-spec | Initial SpecGen direction |
|---|---|---|---|---|---|---|
| Canonical machine schema | strong | weak/Markdown-oriented | moderate/spec text conventions | weak/single Markdown | derived Markdown + memlog | **strong, versioned JSON IR** |
| Human-readable projection | yes | primary | primary | primary | yes | **derived from IR** |
| Typed elicitation/Q&A | strong | workflow prompts | workflow-driven | grill skill | facilitated workflows | **yes, with explicit affected IDs/paths** |
| Immutable/versioned answers | strong | limited | change history via files | limited | append-only memlog | **open decision** |
| Append-only decision log | indirect | limited | change dirs/deltas | backprop in spec | strong memlog | **open decision** |
| Explicit deltas | snapshot diff | artifact evolution | strong | amend/backprop | re-derive from log | **likely useful as derived change set** |
| Traceability | strong | cross-artifact checks | scenarios/change linkage | task/invariant references | stable capability IDs | **structural IDs/edges** |
| Deterministic schema validation | strong | checklists/scripts | conventions/validation | check skill | self-validation | **core requirement** |
| Evaluation generation | acceptance-focused | task/checklist oriented | scenarios | tests/backprop | success signals | **first-class evaluation intent + target compilers** |
| Brownfield change model | moderate | improving | strong | strong/right-sized | adaptable | **first-class evidence + source baseline** |
| Target agent portability | exports | very broad | broad | skill ecosystem | broad | **adapter architecture** |
| Execution engine | no/exports | agent workflow | no/assistant workflow | build loop | workflow framework | **out of core; Agent-Workflow target** |
| Right-size ceremony | moderate | often heavier | strong | very strong | adaptive | **explicit principle** |

## Most promising mechanisms to reuse/adapt

1. **specBuilder:** question/answer provenance, snapshot diff, strict JSON Schema, issue-to-question linkage, export separation.
2. **OpenSpec:** explicit change/delta semantics for brownfield evolution.
3. **BMAD bmad-spec:** append-only decision log and single-writer derived spec model.
4. **Cavekit:** right-sized workflow and failure-to-invariant backpropagation.
5. **Spec Kit:** broad agent integration ergonomics, staged Spec → Plan → Tasks workflow, cross-artifact quality checks.

The core review should decide mechanism-by-mechanism rather than selecting one project as the base architecture.
