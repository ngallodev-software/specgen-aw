# TypeSafe semantic-decision boundary

SpecGen may use TypeSafe-style typed judgments only as bounded semantic evidence. Canonical JSON, validation, provenance, finalization, and user/product authority remain deterministic or explicitly human-authorized.

The initial shadow boundary contains four versioned question sets:

- `evidence.relevance/v1` — rank whether already-discovered repository evidence is materially relevant/supportive;
- `unresolved_issue.authority/v1` — classify whether an issue is repository-answerable, a user decision, external research, already supported, or unclear;
- `requirement.quality/v1` — independent specificity, testability, scope, evidence, compatibility, ambiguity, and hidden-decision judgments;
- `requirement.relationship/v1` — equivalence, overlap, contradiction, and preservation-tension judgments.

`src/specgen/semantic.py` deliberately has no TypeSafe SDK dependency. It is the application-owned harness seam: stable state projectors, versioned typed questions, an adapter protocol, and digest-bound advisory receipts. A provider adapter may invoke the official TypeSafe SDK, but provider availability never changes canonical authority.

## Rollout

1. **Shadow:** collect receipts only; no authoring/finalization behavior changes.
2. **Advisory:** surface calibrated diagnostics and research hints while preserving existing deterministic behavior.
3. **Guarded automation:** only after evaluation demonstrates reliable thresholds for low-consequence actions such as evidence ordering or suppressing an unnecessary repository-answerable user question.
4. **Expansion:** add new question sets only when the semantic seam, projected state, fallback, consumer, and authority boundary are explicit.

Do not use TypeSafe for schema/reference/digest validation, canonical mutation, lifecycle authority, permissions, cryptographic checks, or deciding product intent. Generative requirement creation, repository synthesis, and planning remain reasoning-model work rather than TypeSafe classification work.

## Official SDK adapter and sidecar collection

Install the optional provider dependency with `specgen[typesafe]`. The adapter pins `typesafe-sdk==0.6.0`, matching the independently packaged Agent-Workflow TypeSafe plugin. Importing SpecGen still does not import the SDK or perform network activity.

Explicit shadow collection is available through:

```text
specgen-semantic canonical-spec.json --output semantic-assessment.json [--model MODEL]
```

The command validates the canonical snapshot first, invokes only the bounded question sets, and writes `specgen/semantic-assessment/v1alpha1`. The sidecar contains digest-bound `specgen/semantic-decision-receipt/v1alpha1` entries and is not consumed by validation or finalization. Provider failure therefore cannot change canonical behavior; the explicit shadow command fails rather than silently inventing semantic evidence.

This slice intentionally does not auto-run TypeSafe during ordinary `specgen author`, repository analysis, or target compilation. Automatic shadow collection should be added only behind explicit configuration after live SDK evidence confirms the request/response mapping and operational failure behavior.
