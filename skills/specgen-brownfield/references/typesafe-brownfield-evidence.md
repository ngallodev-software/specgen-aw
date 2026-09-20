# TypeSafe evidence in brownfield SpecGen work

Read this only when TypeSafe semantic assessment is enabled during brownfield specification work. The deterministic repository-analysis and brownfield-plan artifacts remain the baseline.

Use TypeSafe only after deterministic discovery has produced a bounded candidate set. It can help assess semantic relevance/support of candidate evidence and can help identify whether an unresolved issue appears repository-answerable, user-authoritative, externally researchable, already supported, or unclear. It does not replace repository search, graph traversal, source inspection, provenance, drift checks, or user authority.

For evidence relevance, pass the specific requirement/claim and a bounded evidence candidate with durable path/symbol/source references. Do not send the entire repository merely to ask whether one item is relevant. Retain the Score distribution and the Noul support probability; do not equate “relevant” with “proves the requirement.”

For unresolved authority, a `repository_answerable` result is a reason to investigate the repository, not proof of an answer. A `user_decision` result is a routing signal to ask the user a decision-shaped question, not permission for the model to choose. `external_research` identifies an evidence source class; `already_supported` still requires the cited support to exist; `unclear` preserves uncertainty.

Semantic findings belong in the semantic/brownfield analysis side of the workflow and remain separate from `repository-analysis/v1alpha1`. Bind them to the deterministic repository-analysis digest/source refs so drift can invalidate stale semantic evidence.

Load `references/typesafe-semantic-assessment.md` from the general `specgen` skill for Choice/Noul/Score interpretation and authority rules.
