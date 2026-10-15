# P3-01 — Focused verification and no-drift review

## Objective

Verify the refinement improved specification authoring without moving execution
or review lifecycle authority into SpecGen.

## Required checks

- Changed contracts validate; do not run schema churn checks for untouched
  contracts merely to inflate evidence.
- The existing critical-seam/integration path proves the revised
  Agent-Workflow-readiness behavior.
- If brownfield behavior changed, one focused authoring journey proves that
  observed behavior remains evidence and preserve/change decisions remain
  explicit.
- If Agent-Workflow lowering changed, compile/validate one representative prompt
  pack against the pinned public target contract.
- Packaging smoke is required only if package data or entry points changed.
- Review the final diff against `SPEC.md` non-goals.

## Test policy

Prefer existing E2E/critical integration seams. Do not add unit tests by default.
A low-level test must protect a valuable boundary that cannot be covered
reasonably through the public behavior.

## Acceptance

The implementation closes the identified authoring gaps, introduces no duplicate
canonical or lifecycle authority, and leaves CaveKit/Codebase Memory optional.

## Writable paths

This is a verification task. Do not edit production code, schemas, generated
archives, or unrelated repositories. Documentation corrections are allowed only
when they reconcile a demonstrated implementation/documentation mismatch.

## Stop conditions

Stop and report if any required check hangs, if a versioned contract changes, or
if the diff introduces a second canonical or lifecycle authority.
