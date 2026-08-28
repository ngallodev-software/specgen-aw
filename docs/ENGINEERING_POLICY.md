# Engineering Policy

> Document version: 0.2.0 · Applies to SpecGen 0.2.0

Normative project policy. Keep this document concise; change it only when engineering policy changes.

## Source

- Keep production code lean, explicit, and architecture-backed.
- Rough out a component's responsibility, contract, and place in the architecture before implementing it.
- Do not add abstraction, extensibility, agents, hooks, services, or helpers without a concrete need.
- Prefer the smallest implementation that preserves correctness, compatibility, provenance, and maintainability.

## Testing

Tests exist to protect valuable behavior, not to increase a count.

- Prefer end-to-end tests and critical seam integration tests.
- Do not add unit tests by default. Add one only when the behavior is important, cannot be exercised economically at a higher-value seam, and the unit test materially improves fault isolation or safety.
- Do not expand the test surface for trivial getters, wrappers, schema plumbing, or implementation details.
- Do not run tests during ordinary implementation checkpoints unless explicitly requested.
- Run the relevant test set at the end of an implementation phase when that phase could have broken behavior, or when explicitly requested.
- Test count is not a project quality metric. Coverage of critical behavior and boundaries is.

## Documentation and help

Documentation is a maintained interface, not an implementation by-product.

- Do not create documentation merely to record that work occurred.
- Keep documents focused and link to deeper material rather than duplicating it.
- README, help, man pages, and overview docs are concise entry points/reference indexes, not monoliths.
- Each implementation phase updates every existing document, help surface, or man page whose claims changed.
- Maintained reference documents carry an explicit document version and applicable project version; update them when their content changes.
- Accepted ADRs remain historical records; supersede rather than rewrite substantive decisions.
- A diagram has one authoritative source. Other documents link to it instead of copying it.
- Use diagrams only where structure or flow is materially clearer visually. Do not diagram for decoration.
- Diagram sources live inside the documentation that explains them (prefer Mermaid for repository-native diagrams), never as orphaned artifacts.

## Checkpoints and overlays

- Implementation checkpoints should be changes-only, self-applying overlays.
- Every overlay includes a deletion manifest, even when empty.
- The apply script validates repository context before mutation.
- Deletions are limited to explicit safe relative paths; absolute paths and `..` are rejected.
- Added/modified files are applied only after validation succeeds.
