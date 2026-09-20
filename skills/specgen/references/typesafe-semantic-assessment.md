# TypeSafe semantic assessment in SpecGen

Read this reference only when SpecGen semantic assessment, TypeSafe configuration, semantic sidecars, or TypeSafe result interpretation is relevant. Canonical authoring, validation, rendering, and compilation do not require TypeSafe.

## Application boundary

SpecGen owns specification meaning. TypeSafe is optional additive semantic evidence and does not mutate the canonical specification, resolve user product decisions, satisfy deterministic validation, establish provenance, finalize a spec, or authorize Agent-Workflow execution.

Current bounded question sets are:

- `evidence.relevance/v1` — relevance Score plus Noul support proposition;
- `unresolved_issue.authority/v1` — Choice identifying where resolution authority/evidence resides;
- `requirement.quality/v1` — independent quality Scores and ambiguity/hidden-decision Nouls;
- `requirement.relationship/v1` — independent Nouls for equivalence, overlap, contradiction, and preservation tension.

Keep these dimensions independent. Do not collapse them into a single “good requirement” or “conflict” flag.

## Input design

Project only the bounded state needed for the question. Preserve distinctions among observed source evidence, deterministic derived facts, prior semantic inference, user-authorized decisions, and policy. Do not pass a desired semantic answer or finalization/readiness result as input to the semantic assessment. Bind assessments to durable spec/evidence digests and source references rather than copying unnecessary sensitive content.

For evidence relevance, provide the requirement/claim and the candidate evidence needed to judge relevance/support. For unresolved authority, provide the unresolved issue and known evidence/decision context, not a guessed resolution. For requirement quality, provide the requirement and relevant acceptance/evidence context. For relationships, provide the bounded pair and preservation context needed to judge their relationship.

## Primitive interpretation

### Choice

A selected choice plus distribution/confidence identifies the most supported member of a finite set. Confidence is distribution concentration, not authority. For `unresolved_issue.authority`, `user_decision` means the evidence indicates that a user decision is required; TypeSafe has not made that decision.

### Noul

A Noul value is `P(proposition=true)`. Keep intermediate probabilities as uncertainty; do not silently convert every value above 0.5 to true. Relationship questions are intentionally independent, so apparently competing propositions can both have material probability.

### Score

A Score is an expected position on the explicitly ordered rubric, accompanied by a level distribution and confidence. It is not an exact measurement or percentage. A high score with diffuse confidence should remain distinguishable from a concentrated high score.

## Current authority and rollout

The current SpecGen assessment is `mode = shadow` and `advisory_only = true`. A semantic sidecar may inform an agent or reviewer, but it is not consumed as canonical authority by validation/finalization. Do not manufacture a deterministic equivalent score merely to compare additive semantic evidence. The deterministic SpecGen authority/fallback path must remain intact.

The 2026-09-20 live qualification successfully exercised all four question families with real Choice/Noul/Score responses. It also demonstrated meaningful uncertainty (for example, some quality Score distributions were diffuse). Treat the run as SDK/integration qualification, not as calibration of thresholds or proof that a semantic finding is correct.

## Policy and calibration

Application policy—not the SDK—decides whether and how semantic evidence affects later workflow. Do not use arbitrary confidence thresholds. Before any guarded automation, calibrate against representative SpecGen cases and measure error costs for the specific question. Until then, preserve probabilities/distributions and surface ambiguous findings for ordinary evidence gathering, reasoning, or user decision.

## Failure behavior

An explicit semantic-assessment request should report SDK/key/service/contract failure rather than fabricate evidence. Ordinary SpecGen authoring remains usable without the optional TypeSafe SDK. Do not retry identical semantic requests merely to obtain a more convenient answer.
