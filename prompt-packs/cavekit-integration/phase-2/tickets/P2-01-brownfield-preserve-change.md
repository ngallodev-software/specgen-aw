# P2-01 — Brownfield preserve/change/unresolved authoring discipline

## Objective

Harvest CaveKit's useful parity mindset as an authoring discipline while
preserving SpecGen's existing evidence and canonical boundaries.

## Required behavior

- Reuse `specgen/repository-analysis/v1alpha1`,
  `specgen/brownfield-plan/v1alpha1`, and
  `specgen/brownfield-analysis/v1alpha1`.
- For each material existing behavior relevant to the requested change, the
  authoring workflow should drive toward one of three outcomes: preserve,
  intentionally change, or unresolved.
- Observed current behavior never becomes desired behavior automatically.
- Code-answerable questions are investigated; product/policy/acceptance choices
  are asked of the user.
- Approved preserve/change decisions flow through existing canonical
  requirements, preservation claims, decisions, risks, provenance, and
  authoring events.
- Keep deterministic repository evidence separate from semantic inference.

## Preferred implementation shape

Start with the brownfield skill and planner guardrails. Change Python behavior
only if a concrete gap cannot be solved cleanly at that authoring surface.

## Stop conditions

Stop before creating a new parity database, second evidence model, canonical
schema revision, mandatory MCP dependency, or automatic promotion from findings
to canonical meaning.

## Acceptance

A brownfield agent can explain which material behaviors are preserved, which are
explicitly changing, and which still require a decision, while the authoritative
spec remains unchanged until normal authoring actions record the approved
choice.

## Writable paths

Prefer the brownfield skill, planner, and their focused tests. Write only
implementation, skill, test, and maintained-documentation paths required by the
refinement; do not modify generated artifacts or external repositories.

## Tests

Run the focused brownfield authoring journey and the repository's bounded
critical-seam checks. Record evidence that observed behavior remains evidence
until a preserve/change decision is explicitly authored.
