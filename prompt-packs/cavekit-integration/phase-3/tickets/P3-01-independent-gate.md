# P3-01 — Independent integration gate

## Objective

Review the completed implementation against `SPEC.md`, the comparison, and all
prior ticket receipts. Inspect architecture boundaries, source provenance,
schema/version consistency, test evidence, and packaging.

## Required gates

1. compile/format/static checks;
2. unit and schema tests;
3. CLI and brownfield integration tests;
4. Agent-Workflow prompt-pack compilation/validation;
5. packaging and install smoke;
6. independent review and acceptance decision.

No release or merge is accepted with unresolved blocking findings unless a
valid typed waiver exists and is still within scope and expiry.

## Writable paths

Only the independent gate report, review evidence, and authorized completion
metadata; do not alter implementation files.

## Acceptance criteria

Every invariant has evidence, all required tests have bounded results, and the
gate produces an explicit accepted, rejected, or accepted-with-follow-up
decision.

## Stop conditions

Stop on any unresolved blocking finding, missing receipt, schema drift, or
unverified acceptance layer.
