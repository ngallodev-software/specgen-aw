# CaveKit methodology reference

CaveKit is treated as prior art, not as a dependency or authority.

The original comparison identified three useful idea clusters:

- coverage/dependency visibility;
- brownfield discovery and preservation awareness;
- explicit handling of review/revision findings.

The current SpecGen 0.2.0 source already implements substantial equivalents for
all three clusters through canonical acceptance/evaluation/task relationships,
dependency validation, repository/brownfield analysis, authoring events, and
Agent-Workflow lowering.

Accordingly, this plan retains only the residual methodology:

1. make missing observable acceptance obvious before implementation handoff;
2. make preserve/change/unresolved decisions explicit during brownfield
   authoring;
3. ensure external findings become explicit authoring decisions when accepted.

Rejected CaveKit mechanisms include Markdown/parser authority, mutable tracking
ledgers, runtime frontier/completion state, shell/PID state, implicit continue
behavior, and any attempt to make CaveKit itself part of SpecGen's runtime.

Original local research paths may still be useful for attribution or a future
fresh comparison, but implementation must not depend on those paths being
present or on a pre-existing Codebase Memory index.
