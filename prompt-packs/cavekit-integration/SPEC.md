# SpecGen-AW Cavekit Integration Specification

> Status: proposed integration contract. Canonical SpecGen model unchanged.

## Goal

Add Cavekit-derived coverage, brownfield parity, review, validation, and
revision discipline to SpecGen-AW while retaining the existing canonical JSON
authority, evidence-first repository analysis, Agent-Workflow target boundary,
and separate technical/review/acceptance/release statuses.

## Invariants

1. `specgen/spec/v1alpha2` remains the sole current specification authority.
2. Requirements, acceptance criteria, implementation tasks, evaluations,
   findings, waivers, and receipts use stable IDs and explicit versions.
3. Every non-waived criterion maps to at least one implementation task and one
   validation/evidence owner before an Agent-Workflow pack is compiled.
4. Task dependencies form an acyclic graph; the ready frontier is derived from
   completed task state and never inferred from Markdown formatting.
5. Brownfield extraction is read-only and distinguishes observed behavior,
   desired behavior, compatibility obligation, implementation gap, and
   intentional change.
6. Every gate emits a structured receipt, including skipped, unavailable,
   degraded, overridden, failed, and passed outcomes.
7. A blocking finding cannot be bypassed by cycle exhaustion; promotion needs a
   typed waiver with approver, scope, reason, risk, expiry, and evidence.
8. Review or extraction findings never mutate the canonical spec implicitly.
9. Markdown and Agent-Workflow prompt-pack files are deterministic projections.
10. SpecGen does not import Cavekit runtime code or make Cavekit a dependency.

## Proposed records

- `criterion`: `id`, `requirement_id`, `text`, `validation_method`, `status`,
  `task_ids`, `receipt_ids`, `evidence_refs`.
- `task`: `id`, `phase`, `title`, `criterion_ids`, `dependencies`, `owner`,
  `result_contract`.
- `evidence_ref`: `id`, `source_path`, `line_start`, `line_end`, `sha256`,
  `kind`, `captured_at`, `extractor_version`.
- `parity_finding`: `id`, `criterion_id`, `classification`, `evidence_refs`,
  `disposition`, `spec_amendment_needed`.
- `review_finding`: `id`, `severity`, `source`, `affected_ids`, `evidence_refs`,
  `disposition`, `spec_amendment_needed`.
- `waiver`: `id`, `affected_ids`, `approver`, `scope`, `reason`, `risk`,
  `expires_at`, `receipt_id`.
- `gate_receipt`: `id`, `gate`, `status`, `started_at`, `finished_at`,
  `commands`, `evidence_refs`, `findings`, `waiver_ids`, `revision`.

Exact field names and schemas are implementation decisions subject to the
existing SpecGen schema/version rules; this list is not permission to create a
parallel specification model.

## Lifecycle

```text
repository evidence -> proposed extraction -> parity review -> approved spec
       -> criteria/task DAG -> Agent Runs -> gate receipts -> acceptance
       -> release/revision event
```

Research and extraction do not write `spec.json`. Promotion requires explicit
approval, and revision uses append-only authoring events.

## Scope

In scope: typed records, validators, read-only brownfield evidence, criterion
coverage, DAG frontier, structured review/validation receipts, explicit waivers,
CLI/API entry points, deterministic Markdown/Agent-Workflow projections, and
regression tests.

Out of scope: copying Cavekit’s Go/TUI runtime, adopting its Markdown parser,
adding Cavekit as a runtime dependency, broad command aliases, implicit
speculative execution, or weakening Agent-Workflow lifecycle authority.
