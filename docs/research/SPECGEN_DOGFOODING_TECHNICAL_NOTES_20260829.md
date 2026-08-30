# SpecGen dogfooding technical notes — 2026-08-29

## Scope

These notes cover the small `agent-workflow-lifecycle-watch-20260829`
specification and its Agent-Workflow prompt-pack target. They separate
SpecGen authoring/compilation observations from the target application's
implementation work.

## Artifacts

The canonical and derived artifacts are located at:

```text
/lump/apps/agent-workflow/implementation-output/workflow-lifetime-watch-20260829/
```

They include the canonical `spec.json`, repository analysis, brownfield plan,
rendered `SPEC.md`, and the generated two-task prompt pack.

## Observed authoring constraint

Repository provenance locators are deterministic repository paths. A locator
written as `src/agent_workflow/orchestrator_supervisor.py:watch` was treated as
a non-existent path; the canonical locator must be the file path
`src/agent_workflow/orchestrator_supervisor.py`.

### Suggestion

Keep path locators deterministic, but provide an optional structured symbol
field for repository provenance. This would allow a spec to bind both the file
and the intended symbol without overloading a path string:

```json
{
  "kind": "repository",
  "locator": "src/agent_workflow/orchestrator_supervisor.py",
  "symbol": "watch"
}
```

Until then, record symbol evidence in the source description or a separate
brownfield-analysis finding.

## Fail-closed compilation detail

Agent-Workflow target compilation refuses repository analysis containing a
blocker. This preserves the chain from canonical provenance to the repository
baseline, but the compile error identifies only a conflict ID.

### Suggestion

Include the blocker message and the offending source ID/locator directly in
the compile diagnostic. This avoids a separate analysis-file search for a
simple provenance repair while preserving fail-closed behavior.

## Brownfield capability visibility

The generated brownfield plan reports `codebase_memory.available: false` even
though this authoring session has a ready codebase-memory service for the
target repository. The plan is produced by a command-line subprocess, so it
can only detect an MCP client registration or executable fallback that is
visible in that subprocess; it cannot discover the session-owned MCP tools the
author used for semantic research.

### Suggestion

Allow an optional, explicit capability attestation on brownfield planning, or
accept a small externally generated capability record. The plan could then say
that semantic research used an available session MCP service without pretending
that the CLI process invoked it. The record should identify the project and
index state, but should not turn graph output into deterministic repository
evidence.

## Dirty-baseline precision

The repository analysis and drift report retain the Git revision and the fact
that the target checkout is dirty. They do not include a digest of the dirty
tracked/untracked content. Consequently, two different dirty states at the
same commit remain indistinguishable to a later drift check.

### Suggestion

For an explicitly allowed dirty baseline, include optional, redaction-safe
content fingerprints for the tracked patch and the untracked-path inventory.
Then drift can distinguish an unchanged dirty checkout from a materially
different one. If a host cannot safely produce those fingerprints, the report
should say that dirty-state drift is indeterminate rather than implying the
revision alone is a complete baseline.

## Independent specification review

An independent Luna review found that the original three requirements described
an adapter but did not define its implementation boundary. The revised canonical
snapshot (`SNAP-002`, version `0.1.1`) now adds:

- `IFACE-001`, a best-effort host notification/wake adapter with no lifecycle
  or watcher-control authority;
- `NOTIFY-001`, a record limited to durable event identity, orchestrator and
  sender identity, event kind, and a redacted summary of at most 512 Unicode
  characters;
- an explicit order: durable inbox import and source-cursor advancement precede
  adapter invocation;
- at-least-once advisory delivery, with consumer deduplication by `event_id`;
- focused acceptance evidence for two children, ordering, bounds, adapter
  failure, duplicate delivery, and host recovery from the durable inbox.

The revision also corrects a subtle wording error: after a source event is
imported, a failed alert need not cause that source event to be imported again
on restart. The durable **inbox** record is the recovery point; its presence is
what must remain observable regardless of alert delivery.

## Generated-target placement

Compiling a replacement prompt pack inside the analyzed implementation
repository exposed a dependency cycle. Repository analysis had catalogued the
previous generated pack as source evidence. Moving that pack aside to make an
empty compiler destination correctly caused fail-closed compilation to report
that evidence as missing.

The enhanced generated pack is therefore kept outside the target repository:

```text
/lump/apps/specgen-aw/implementation-output/workflow-lifetime-watch-20260829/prompt-pack/
```

The canonical specification and repository evidence remain in the
Agent-Workflow artifact directory. This avoids treating compiler output as a
required input to the source-repository analysis.

### Suggestion

Add a declared generated-output exclusion or an atomic replacement mode to
SpecGen repository analysis/compilation. Such an exclusion should be explicit
in the canonical spec or compiler invocation and recorded in the analysis; it
must not silently omit ordinary source paths. That would permit an in-repository
generated target without creating self-referential evidence.

## Archive-format discoverability

`agent-workflow pack archive --help` names the source and output arguments but
does not state that the output must end in `.tar.zst`. An attempted `.tar.gz`
archive fails with that requirement only after invocation.

### Suggestion

Include the required suffix in the usage text and one minimal example. This is
a small documentation improvement that makes deterministic archive generation
discoverable without a trial invocation.

## Target-application design gaps represented by the spec

The existing Agent-Workflow supervisor already supports one active watcher per
orchestrator identity, a single-writer lease, and durable replay of registered
child journals. The new intent is deliberately small:

- one host-owned watcher is shared across all children in a workflow;
- notification and wake delivery occur only after durable replay;
- notification is bounded, advisory, and non-authoritative;
- a child completion cannot terminate the shared watcher;
- restart replay remains the fallback when a wake is absent or duplicated.

The target currently lacks a public, declarative host notification/wake adapter
contract. That is the implementation seam; it should be added as a minimal
adapter invoked by the supervisor, not as a second lifecycle system.

## Evaluation suggestion

The generated pack uses focused supervisor-inbox tests. Its most important
additional scenario is an installed, two-child journey:

1. start one workflow watcher;
2. complete child A and observe one advisory notification;
3. prove the watcher stays active;
4. deliver/replay child B;
5. restart the watcher after a simulated adapter failure and prove the durable
   event remains discoverable.

This should remain an independent review task, not an extra watcher process.

## Explicit non-goals retained

- Herd is not required; it may later become a presentation adapter.
- Worker Git permission and host commit-seal policy remain a separate change.
- Notifications do not grant completion, review, or acceptance authority.
