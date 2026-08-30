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

### CONTRACT-001 — Publish the shared SpecGen ↔ Agent-Workflow contract bundle

**Status:** approved; repository/package authority required before implementation

Replace duplicated, vendored cross-product compatibility fixtures with a small,
separately released Python distribution in a sibling repository. The bundle is
the immutable source of the schemas shared across the SpecGen ↔ Agent-Workflow
boundary, schema IDs, deterministic descriptors/digests, validation and
normalization helpers, contract metadata, and conformance fixtures. Any bundle
schema or helper behavior change releases a new bundle version; published
versions remain immutable and installable.

The bundle is deliberately not a shared execution framework: it must not own
SpecGen canonical authoring/compilation, Agent-Workflow task scheduling,
model/role choice, lifecycle, logging, review, sealing, or generic CRUD. The
Agent-Workflow prompt-pack schema may move into the bundle while
Agent-Workflow remains its semantic owner and interpreter. SpecGen's future
portable prompt-pack schema remains SpecGen-owned unless another consumer
actually needs it. Every cross-application semantic seam belongs in the
bundle: shared schemas and IDs, normalization/canonicalization, validation,
artifact descriptors/digests, feature/version negotiation, and conformance
fixtures. Private-only behavior remains in its owning application and does not
create a bundle release.

Every new bundle release that changes a shared artifact must ship deterministic,
tested migrations from every supported earlier bundle version to that release.
The bundle exposes a narrow transform API/CLI that validates the source,
performs an explicit version-to-version transformation, validates the result,
and emits migration provenance (source version/digest, target version/digest,
transform identifier, and timestamp supplied by the caller). Migrations never
rewrite sealed historical artifacts: they produce a derived replacement linked
to its immutable source. A change that cannot preserve an older artifact's
meaning must fail closed with an actionable manual-migration diagnostic rather
than silently inventing data.

Each generated Agent-Workflow target must declare the bundle version and
schema digest it was compiled against. The producer and consumer use the exact
same immutable bundle release for that handoff; the consumer verifies its
installed version and digest and fails closed on mismatch. Application releases
may change independently only when their changes do not alter the shared seam.
This reduces compatibility to an explicit application-to-bundle support policy
rather than falsely claiming that arbitrary SpecGen and Agent-Workflow
releases interoperate.

**Done when:** the repository/package namespace and publishing authority are
approved; an initial immutable wheel exposes only the common contract surface;
both applications consume it through narrow seams; old vendored shared
fixtures are removed after release/package smoke and cross-repository
conformance tests prove exact-match acceptance and mismatch rejection. Each
released shared-artifact change includes supported-version migration tests,
provenance-linked output, and fail-closed unsupported/manual cases.

### PORT-001 — Compile a host-independent agent task pack

**Status:** research required

SpecGen currently emits canonical JSON and review/evidence projections, plus an
`agent-workflow/prompt-pack/v1` target. It has no portable task-pack target for
agents that do not install or use Agent-Workflow. Define a separate, versioned
SpecGen-owned output contract that carries ordered phases and delegatable task
prompts, guardrails and writable scope, target-application identity, expected
outputs, result schemas/templates, machine-readable evaluation intent, and
minimal machine-oriented instructions/examples. It must render detailed
human-oriented Markdown alongside the machine-readable pack, and expose the
task DAG, dependency tree, and safe parallelism opportunities as advisory
information rather than an execution command.

The target must be useful to any competent agent runner without claiming that
it provides Agent-Workflow's durable run identity, message acknowledgement,
restart lineage, evaluation, review, or acceptance authority. Logging and
completion evidence must be representable as portable artifacts, while the
executing host remains responsible for storing and enforcing them. Research
the smallest viable manifest/resource layout, integrity and archive behavior,
and how existing canonical task/evaluation fields lower without semantic loss.
Agent-Workflow currently owns its native `agent-workflow/prompt-pack/v1`
scaffold, validator, archive, and execution interpretation; retain those as
its target contract. Transfer only the reusable specification-to-portable-pack
authoring/compiler responsibility to SpecGen, and avoid a generic
`prompt-pack/v1` name that would create contract confusion. Compile only a
signed-off canonical snapshot; a user-supplied Markdown/specification must be
imported and accepted as canonical SpecGen meaning first. The portable pack
must not select models, force parallelism, assign runtime roles, or claim that
an external host executed, logged, reviewed, or accepted its work.

**Done when:** a host-independent schema, CLI command, file layout, examples,
validation rules, and clear Agent-Workflow boundary are approved; at least one
non-Agent-Workflow consumer can follow the generated pack end-to-end without
unstated conventions. The example demonstrates both serial single-agent use
and an optional parallel execution plan from the same pack.

### DOC-001 — Make standalone and joint-use value explicit

**Status:** research required

The README identifies Agent-Workflow as a target rather than a runtime
dependency, but it leads with an Agent-Workflow-branded subtitle and its quick
start is target-heavy. Audit the README, usage guide, architecture, integration
guide, skills, and CLI help for a concise standalone path and a concise
combined-use path. Explain which artifacts are portable today, which are
Agent-Workflow-specific, and the concrete added value of using both products.

**Done when:** a new user can choose standalone authoring versus the
Agent-Workflow handoff from the primary documentation without reading an ADR;
all claims agree with the shipped CLI and target contracts.

### DOC-002 — Ship a generated system manpage for `specgen`

**Status:** research required

There is no manpage source, packaging entry, or installed `specgen(1)` manual;
the CLI help and `docs/USAGE.md` are the current reference. Define a
maintained, distribution-friendly manpage generated from a single CLI/doc
authority where practical. It must cover synopsis, commands/options,
standalone usage, the optional Agent-Workflow target, files/contracts, and
exit status without becoming a second drifting command reference.

**Done when:** `specgen(1)` is installed by the supported package/install path,
documents the released CLI accurately, and a release check detects divergence
between its command synopsis and `specgen --help`.
