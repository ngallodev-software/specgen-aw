# Prompt-pack research run notes — 2026-08-29

## Scope

Four independent Luna Agent-Workflow runs were prepared to research and verify
`PACK-001` (prompt-pack path length) and `PACK-002` (portable target-application
identity). The runs are read-only and share the recorded checkout baseline;
their research conclusions will be appended after completion.

## Operational issues and learnings

1. `agent-workflow agent-run prepare` requires the prompt positional argument to
   be a regular prompt-file path. Supplying inline prose caused the CLI to
   interpret the beginning of the prose as a filesystem path and raised
   `FileNotFoundError`. Learning: create or reference a prompt file before
   preparation.
2. The first retry attempted `--role` together with explicit executor/model/
   reasoning options. The CLI rejected that combination. Learning: use a role
   alone for configured routing, or use explicit compatibility overrides without
   `--role`.
3. Automatic agent-name selection assigned an incompatible configured name for
   an exploratory class (`bridge3` requires implementation), and reusing an
   active configured name produced `agent name is already active`. Learning:
   explicitly select a configured name whose class matches the run and keep
   names unique among concurrent runs.
4. The initial temporary-prompt patch was malformed because the generated patch
   lacked the required newline before `*** End Patch`. Learning: validate patch
   framing when creating durable prompt inputs; no repository file was changed
   by that failed patch.
5. The repository was already dirty at launch due to pre-existing user work.
   Runs were explicitly prepared with `--allow-dirty` and record the exact
   source revision plus dirty-at-launch state. Learning: research-only runs can
   share the checkout only when that provenance is made explicit and agents are
   prohibited from editing.

## Run state at dispatch

| Run | Purpose | Durable state at dispatch |
|---|---|---|
| `pack001-research` | primary path-length research | running |
| `pack001-verify` | independent path-length verification | running |
| `pack002-research` | primary application-identity research | running |
| `pack002-verify` | independent application-identity verification | running |

Worker exit, structured completion, evaluation, review, and acceptance remain
separate gates. No solution is accepted from worker output alone.

## Research handoff observations

The completed handoffs converge on these provisional findings; they are not
yet an implementation decision:

- `PACK-001`: measured generated paths reached 153 characters on this checkout
  before consumer nesting. SpecGen accepts a caller-selected output root and
  does not cap the absolute path. Agent-Workflow 0.9.0 rejects symlinked pack
  roots and symlink entries during inventory/validation/archive handling. The
  leading candidate is a real-directory pack tree with a compact generated
  layout and configurable output root; archive transfer may be preferable to
  filesystem linking.
- `PACK-002`: `agent-workflow/prompt-pack/v1` requires `pack_id`, workflow, and
  phases; SpecGen emits `pack_id` from the SpecGen document ID. The canonical
  v1alpha2 model has document `id` and `title`, but no target-application
  field. Repository paths and source baselines identify checkout provenance
  and revision, not a portable application. The leading candidate is a
  separately named canonical application identifier while preserving legacy
  `pack_id` semantics.

## Additional agent/tool issues

- A research probe attempted cleanup with `rm -rf`; the worker/tool policy
  rejected the command. Learning: use recoverable or policy-compliant temporary
  directory handling and avoid destructive cleanup commands in delegated
  probes.
- Worker shells emitted pre-existing profile warnings (`pyenv: command not
  found` and `/.cargo/env: No such file or directory`). Learning: distinguish
  shell-environment noise from research failures and capture it as environment
  evidence.
- A focused PACK-002 harness first failed with `ModuleNotFoundError` when run
  without the repository import path. With the import path corrected, it hit an
  unrelated compatibility-fixture drift in
  `schemas/agent-run-contract.schema.json`. Learning: record setup failures and
  unrelated gate failures separately; neither proves or disproves PACK-002.
- One PACK-001 completion handoff initially violated the completion contract
  by putting unresolved questions in the lifecycle `unresolved` field and by
  listing a failing probe among final passing commands. The worker corrected
  the handoff and validation passed. Learning: unresolved research questions
  belong in evidence for a completed research report, while final verification
  commands must all pass.

## Current gate state

The four prepared runs produced valid completion handoffs except that
`pack001-research` still reports a live worker/status projection mismatch after
its validated handoff. Deterministic evaluation was not planned, and no
authorized acceptance has been recorded. The findings therefore remain input
for the next human review rather than accepted backlog solutions.
