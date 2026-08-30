# Backlog

## Open items

### PACK-001 — Prevent prompt-pack path-length failures

**Status:** complete

Prompt-pack output can become deeply nested under an implementation-output
directory before it is consumed by the target repository. Investigate a
portable way to keep working paths below filesystem limits before real-world
packs expose the problem.

The proposed symlink approach—mapping a long generated location such as
`implementation-output/<long-pack-name>/prompt-pack` to a short path such as
`<target-repository>/prompt-packs/<short-pack-name>`—is only a candidate, not an
approved design. Research must cover symlink support and permissions across
supported hosts, Windows/junction behavior, archive and validation semantics,
worktree/source-baseline safety, cleanup, and whether a shorter generated
layout or configurable output root solves the problem more reliably.

**Done when:** a documented, host-independent strategy is selected, its
failure modes are understood, and the relevant generation/validation and
Agent-Workflow boundaries are identified. Do not implement the symlink proposal
until that research is complete.

Resolution: use a compact real-directory output root and reject symlinked
Agent-Workflow targets. The compiler keeps archive, validation, and source
provenance inside the selected root; archive transfer remains the portable
escape hatch for deeply nested consumers. Implemented in
`src/specgen/agent_workflow.py` with critical-seam coverage.

### PACK-002 — Add a portable target-application identifier to prompt packs

**Status:** complete

Current verification found no explicit target-application identity in the
prompt-pack contract. `pack_id` is derived from the SpecGen document ID and the
generated README uses the specification title; neither is a declared,
stable application identifier. Repository paths and source baselines are
provenance, not a portable application identity, because they vary by machine.

Research and propose a non-path symbol/string for the application the pack is
intended to modify. Determine its authority and lifecycle (for example,
canonical SpecGen input versus target manifest), naming/uniqueness rules,
backward compatibility, rendering, validation, archive behavior, and how it
interacts with packs that target a new or not-yet-existing application.

**Done when:** the contract location, semantics, validation rules, and
generation/consumption behavior are specified with an explicit portable
example, and the design is approved before implementation.

Resolution: `target_application_id` is an optional canonical v1alpha2 field,
validated as lowercase kebab-case (1–63 characters). It is preserved in
rendered and generated prompt-pack human-facing projections, while legacy
`pack_id` and path provenance remain unchanged. The 0.9.1 public Agent-Workflow
contracts are unchanged and the compatibility fixture is pinned to the clean
0.9.1 release commit.
