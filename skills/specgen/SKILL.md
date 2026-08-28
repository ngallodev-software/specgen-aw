---
name: specgen
description: Author, validate, trace, render, and compile durable machine-readable specifications with explicit uncertainty and Agent-Workflow-ready implementation/evaluation intent.
---

# SpecGen Skill

Use SpecGen when product or engineering intent needs to survive a chat session as a validated, traceable, versioned specification. Use it especially for brownfield changes, phased implementation, explicit acceptance/evaluation intent, preservation claims, or Agent-Workflow prompt-pack compilation.

Do not use SpecGen merely to make a prettier requirements document. The canonical JSON snapshot is the specification authority; Markdown, semantic deltas, evaluation plans, and Agent-Workflow artifacts are derived projections.

## Authority rules

1. `spec.json` owns current specification meaning.
2. Authoring events preserve why decisions changed; they do not replace the current snapshot.
3. `SPEC.md` is a deterministic human projection.
4. Semantic deltas are comparisons between immutable snapshots.
5. Repository analysis is evidence-first and read-only; never infer arbitrary source semantics from filename/regex guesses.
6. Agent-Workflow artifacts are target projections. Never edit them to redefine the canonical specification.
7. Preserve stable IDs for semantic objects that survive a revision.
8. Keep unresolved decisions explicit. Never invent a technology/product decision just to make readiness pass.

## Choose an authoring mode

- `express` — lowest ceremony; use when the request is already narrow and the caller accepts unresolved detail.
- `guided` — default general authoring; requires acceptance coverage for active requirements.
- `strict` — unresolved questions and missing verification intent block finalization.
- `agent-workflow` — strict implementation-readiness profile: phased tasks, requirement/task coverage, task result contracts, evaluation intent, and resolved blockers.

Inspect the actual mode guardrails rather than reproducing them from memory:

```bash
specgen modes
specgen author assess candidate.json --mode guided
```

## Default authoring loop

1. Load or create a candidate `specgen/spec/v1alpha2` JSON document. Consult the installed/public schema; do not create an alternate model.
2. Preserve existing stable IDs when revising an existing spec.
3. Record important user decisions, corrections, evidence, assumptions, and unresolved questions durably. Authoring-history events use `specgen/authoring-event/v1alpha1` and append through:

```bash
specgen events append events.ndjson event.json
```

4. Update the candidate canonical snapshot from authorized decisions/evidence.
5. Assess readiness under the selected mode:

```bash
specgen author assess candidate.json --mode MODE
```

6. Resolve blockers by asking for missing product decisions or collecting evidence. Do not guess them.
7. Finalize only when the selected mode is ready:

```bash
specgen author finalize candidate.json --mode MODE --output spec.json
```

8. Produce review projections as needed:

```bash
specgen render spec.json --output SPEC.md
specgen diff prior.json spec.json
specgen evals intent spec.json
```

## Brownfield repositories

Analyze the exact repository state that informed the spec:

```bash
specgen repo analyze /path/to/repo --spec spec.json --mode MODE > repository-analysis.json
```

Use discovered durable declarations and explicit referenced evidence as facts. Surface contradictions and missing evidence. Semantic conclusions that require code understanding belong in agent reasoning and must be recorded as decisions/inferences rather than presented as deterministic discovery.

Before reusing an older analysis:

```bash
specgen repo drift repository-analysis.json /path/to/repo
```

If drift is material, regenerate analysis before finalization/target compilation.

## Traceability and preservation

Keep important chains mechanically intact:

```text
requirement -> acceptance criterion -> evaluation -> implementation task -> result contract
source evidence -> preservation claim -> requirement/interface/decision
```

A broken reference is a specification defect, not something to patch in rendered Markdown.

## Evaluation intent

Every important active requirement should say how correctness will be assessed. Keep public, hidden, and external oracle semantics distinct. For Agent-Workflow compilation, hidden/external oracle intent needs a digest-bound `metadata.oracle_ref` and must map through requirement/acceptance coverage to implementation tasks.

Do not add tests or evaluations merely to increase a count. Verification should protect important externally observable behavior and target seams.

## Agent-Workflow mode and compilation

Use `agent-workflow` mode when the intended handoff is phased autonomous implementation:

```bash
specgen author assess candidate.json --mode agent-workflow
specgen author finalize candidate.json --mode agent-workflow --output spec.json
```

If the specification contains repository provenance, create a repository analysis bound to the finalized snapshot and compile with the live repository root:

```bash
specgen repo analyze /path/to/repo --spec spec.json --mode agent-workflow > repository-analysis.json
specgen agent-workflow compile spec.json \
  --repository-analysis repository-analysis.json \
  --repository-root /path/to/repo \
  --output targets/agent-workflow
```

Without repository provenance:

```bash
specgen agent-workflow compile spec.json --output targets/agent-workflow
```

Compilation is fail-closed. Unsupported result schemas, stale repository evidence, directory-only baselines, evaluation metadata that cannot be represented, incompatible per-evaluation scorers, or ambiguous hidden/external oracle mappings must be resolved in the canonical spec/evidence rather than silently dropped.

The generated directory is an Agent-Workflow prompt-pack source tree. `MANIFEST.sha256` is the source checksum sidecar. Do not create `MANIFEST.json` manually; Agent-Workflow owns that reserved archive-integrity artifact.

## Optional Agent-Workflow host

When the `agent-workflow-spec` plugin is installed and explicitly enabled in Agent-Workflow 0.9.0, selected SpecGen operations are available under:

```bash
agent-workflow spec compatibility
agent-workflow spec assess spec.json --mode agent-workflow
agent-workflow spec analyze /path/to/repo --spec spec.json --mode agent-workflow
agent-workflow spec finalize candidate.json --mode agent-workflow --output spec.json
agent-workflow spec compile spec.json --output targets/agent-workflow [...]
```

The plugin is only a host adapter. SpecGen remains independently usable and Agent-Workflow retains execution/review/acceptance authority.

## Stop conditions

Stop and surface the issue instead of manufacturing completeness when:

- a blocking question remains unresolved;
- evidence referenced by the spec is missing or stale;
- stable-ID traceability is broken;
- a preservation claim cannot be represented or intentionally excluded with rationale;
- the target contract cannot faithfully carry evaluation/result/source semantics;
- compilation would require private Agent-Workflow implementation imports or another execution authority.
