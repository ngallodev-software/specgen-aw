# SpecGen dogfooding working review — 2026-08-29

## Purpose

This review captures the authoring experience of turning a small operational
request into durable implementation intent. It deliberately discusses neither
tool behavior nor validation outcomes.

## The experience

The request began as a familiar coordination concern: a parent needs to learn
about meaningful child events without mistaking a notification for authority.
Writing the intent down made the important distinction feel natural rather
than procedural:

- the durable journal remains the record of what happened;
- a human-visible alert is a convenience;
- a wake signal is an invitation to inspect the durable record;
- completion, review, and acceptance remain separate decisions.

The most useful moment in authoring was choosing the scope of the watcher.
The appropriate unit is a workflow, not a worktree and not an individual
worker. A workflow has one parent coordination context and may have many child
runs. One host-owned watcher therefore follows that coordination context for
its lifetime. A child finishing changes the child state; it does not decide
the lifetime of the shared watcher.

This framing also made responsibility clear. Workers may publish progress and
completion evidence. The host owns observation, notification, wake delivery,
and any later decision to stop the watcher. This avoids a subtle but costly
mental model in which the first finished worker accidentally appears to own
the rest of the workflow.

## Decisions worth preserving

### One watcher per workflow

Share one watcher across all registered children of a workflow/orchestrator
identity. It should continue past individual child completion and stop only
under host-owned workflow policy or an explicit host action.

### Alerts are not authority

An alert should contain a bounded, identity-bearing summary that directs the
orchestrator to durable evidence. It must not become an alternate completion,
review, or acceptance channel.

### Waking is advisory

A wake request improves responsiveness for a waiting orchestrator. It cannot
be relied upon for correctness: durable replay must still make every event
discoverable after an interruption, duplicate wake, or missed delivery.

### Host ownership is explicit

The watcher belongs to the workflow host. Child workers cannot stop, replace,
or inherit it merely by completing their own assignment. This is both easier
to reason about and safer when several worktrees are active at once.

## Implementation handoff

The corresponding implementation intent is kept with the Agent-Workflow
working artifacts under:

```text
/lump/apps/agent-workflow/implementation-output/workflow-lifetime-watch-20260829/
```

The intended small implementation has two parts: introduce the host-owned
notification/wake seam, then independently exercise the shared-watcher
lifetime across multiple child runs.

Implementation-facing observations and suggestions are intentionally kept out
of this experience review. They are recorded separately in
[`SPECGEN_DOGFOODING_TECHNICAL_NOTES_20260829.md`](SPECGEN_DOGFOODING_TECHNICAL_NOTES_20260829.md),
so this document can stay focused on the operational model the specification
made easier to express.

## Closing perspective

The value of the exercise is not ceremony. It is the ability to make a small
operational promise legible: the parent can be promptly awakened, the workflow
does not disappear when one child ends, and the durable record remains the
place where decisions are made.
