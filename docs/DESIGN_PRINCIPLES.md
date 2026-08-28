# Design Principles

> Document version: 0.1.1 · Applies to SpecGen 0.1.1

Normative unless superseded by an accepted ADR. Execution policy is in [ENGINEERING_POLICY.md](ENGINEERING_POLICY.md).

1. **Canonical meaning belongs to SpecGen.** Canonical structured state is authoritative; renderings and target artifacts are projections.
2. **Agent-Workflow-aware, never Agent-Workflow-dependent.** Basic authoring/validation/rendering cannot require Agent-Workflow.
3. **Compile to public contracts, never private implementation modules.**
4. **Version every machine contract from day one.** Breaking semantics get a new identifier; existing contract files are not silently mutated.
5. **Compatibility is narrow, explicit, and testable.** Product versions and exact public contracts are named.
6. **Human-readable artifacts are projections, not competing authorities.**
7. **Traceability is structural.** Durable objects have stable IDs and explicit links.
8. **Provenance is evidence, not decoration.** Evidence, decisions, inferences, and assumptions remain distinguishable.
9. **Separate authoring, specification, and execution lifecycles.** Events explain history; snapshots define current meaning; execution targets own execution state.
10. **Evaluation intent belongs in the specification lifecycle.** Execution may occur elsewhere.
11. **LLMs propose; deterministic contracts constrain.** Prefer schema and deterministic validation where possible.
12. **Preserve useful ambiguity instead of fabricating certainty.**
13. **Prior art is mined selectively and credited explicitly.**
14. **Architecture remains mutable; significant decisions remain visible.**
15. **Complexity must earn its cost.** Lean common paths beat speculative abstraction.
16. **Tests protect seams, not line counts.** Prefer E2E and critical integration coverage; unit tests are exceptional.
17. **Documentation is a versioned interface.** Keep it focused, linked, non-duplicative, and updated only when relevant claims change.
