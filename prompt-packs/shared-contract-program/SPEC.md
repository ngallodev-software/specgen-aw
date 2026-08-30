# Shared SpecGen and Agent-Workflow contract bundle

> Spec `shared-contract-program-20260830` · version `0.1.0` · snapshot `SNAP-001` · current · draft

**Target application:** `agent-workflow-spec-contracts`

## Snapshot

- **Created:** 2026-08-30T00:00:00Z
- **Sequence:** 1
- **Parent:** —
- **Digest:** sha256:3a2ef430ab034126132e54e718dbedb61a56afcc0fb732b2f9796567ac06b258
- **Authoring events:** —

## Intent

SpecGen and Agent-Workflow duplicate cross-boundary schemas and compatibility fixtures while lacking a deterministic, migration-capable shared contract authority.

### Objectives

- Publish a small immutable shared Python contract bundle.
- Make native target handoffs exact-version and digest verified.
- Preserve sealed artifacts through derived deterministic migration.

### Outcomes

- _None._

### Non-goals

- Create shared scheduling, lifecycle, review, logging, or generic CRUD.
- Force a model, role, or parallel execution topology.
- Make portable SpecGen packs parse as native Agent-Workflow packs.

## Context

`{}`

## Scope

### Included

- shared schema/ID/validation/digest/negotiation/migration seams
- SpecGen producer integration
- Agent-Workflow consumer integration
- cross-repository conformance

### Excluded

- external registry publication until repository/signing authority is approved

### Protected

- _None._

### Constraints

- _None._

## Requirements

### `REQ-001` — A separately released bundle owns every shared SpecGen-Agent-Workflow semantic seam: schemas and IDs, normalization, validation, descriptors/digests, negotiation, migrations, and conformance fixtures.

- **Priority:** must
- **Provenance Refs:** SRC-001
- **Statement:** A separately released bundle owns every shared SpecGen-Agent-Workflow semantic seam: schemas and IDs, normalization, validation, descriptors/digests, negotiation, migrations, and conformance fixtures.
- **Type:** functional
- **Verification Refs:** AC-001, EVAL-001

### `REQ-002` — SpecGen-generated native targets declare exact bundle version and digest; Agent-Workflow rejects a mismatch before execution.

- **Priority:** must
- **Provenance Refs:** SRC-001
- **Statement:** SpecGen-generated native targets declare exact bundle version and digest; Agent-Workflow rejects a mismatch before execution.
- **Type:** functional
- **Verification Refs:** AC-002, EVAL-002

### `REQ-003` — Every supported shared-artifact version transition has deterministic validated migration that emits provenance-linked derived artifacts and fails closed when meaning cannot be preserved.

- **Priority:** must
- **Provenance Refs:** SRC-001
- **Statement:** Every supported shared-artifact version transition has deterministic validated migration that emits provenance-linked derived artifacts and fails closed when meaning cannot be preserved.
- **Type:** functional
- **Verification Refs:** AC-003, EVAL-003

### `REQ-004` — SpecGen retains canonical authoring and compilation; Agent-Workflow retains runtime interpretation, scheduling, execution, evaluation, review, and sealing.

- **Priority:** must
- **Provenance Refs:** SRC-001
- **Statement:** SpecGen retains canonical authoring and compilation; Agent-Workflow retains runtime interpretation, scheduling, execution, evaluation, review, and sealing.
- **Type:** functional
- **Verification Refs:** AC-004, EVAL-004

## Interfaces

_None._

## Data contracts

_None._

## Decisions

_None._

## Acceptance criteria

### `AC-001` — The bundle wheel exposes only documented shared contract seams, all source schemas are immutable/versioned, and both applications import it through narrow adapters.

- **Criterion:** The bundle wheel exposes only documented shared contract seams, all source schemas are immutable/versioned, and both applications import it through narrow adapters.
- **Requirement Ids:** REQ-001
- **Verification Method:** wheel inventory and cross-repository conformance tests

### `AC-002` — An exact producer/consumer bundle match is accepted and version or digest mismatches fail before Agent Run preparation/execution.

- **Criterion:** An exact producer/consumer bundle match is accepted and version or digest mismatches fail before Agent Run preparation/execution.
- **Requirement Ids:** REQ-002
- **Verification Method:** installed producer-consumer acceptance journey

### `AC-003` — Supported old fixtures migrate to validated derived current artifacts with source/target digest provenance; unsupported changes return an actionable manual migration error and sealed sources remain byte-identical.

- **Criterion:** Supported old fixtures migrate to validated derived current artifacts with source/target digest provenance; unsupported changes return an actionable manual migration error and sealed sources remain byte-identical.
- **Requirement Ids:** REQ-003
- **Verification Method:** migration fixture matrix

### `AC-004` — The bundle contains no application lifecycle/scheduler/authoring implementation and docs/test boundaries prove each application retains its named authority.

- **Criterion:** The bundle contains no application lifecycle/scheduler/authoring implementation and docs/test boundaries prove each application retains its named authority.
- **Requirement Ids:** REQ-004
- **Verification Method:** source inventory and independent review

## Evaluations

### `EVAL-001` — Evaluations

- **Acceptance Ids:** AC-001
- **Command:** python, -m, pytest, -q, tests
- **Kind:** acceptance
- **Requirement Ids:** REQ-001

### `EVAL-002` — Evaluations

- **Acceptance Ids:** AC-002
- **Command:** python, -m, pytest, -q, tests/acceptance
- **Kind:** acceptance
- **Requirement Ids:** REQ-002

### `EVAL-003` — Evaluations

- **Acceptance Ids:** AC-003
- **Command:** python, -m, pytest, -q, tests/migrations
- **Kind:** acceptance
- **Requirement Ids:** REQ-003

### `EVAL-004` — Evaluations

- **Acceptance Ids:** AC-004
- **Command:** python, -m, pytest, -q, tests
- **Kind:** acceptance
- **Requirement Ids:** REQ-004

## Implementation tasks

### `TASK-001` — Characterize and freeze the shared seam inventory

- **Dependencies:** —
- **Expected Outputs:** file-by-file extraction inventory for both repositories, approved bundle public API and ownership matrix, baseline fixture digests
- **Requirement Ids:** REQ-001, REQ-004
- **Result Contract:** `{"schema":"agent-workflow/task-result/v1"}`
- **Role Hint:** analysis

### `TASK-002` — Create the immutable shared contract bundle

- **Dependencies:** TASK-001
- **Expected Outputs:** sibling Python package with schemas, descriptors, validation, negotiation, migrations, CLI/API, wheel tests, supported-version policy and immutable fixtures
- **Requirement Ids:** REQ-001, REQ-003, REQ-004
- **Result Contract:** `{"schema":"agent-workflow/task-result/v1"}`
- **Role Hint:** implementation

### `TASK-003` — Integrate SpecGen as bundle-versioned native target producer

- **Dependencies:** TASK-002
- **Expected Outputs:** SpecGen adapter uses bundle APIs, native target declares bundle version/digest, producer mismatch and packaging tests
- **Requirement Ids:** REQ-001, REQ-002, REQ-004
- **Result Contract:** `{"schema":"agent-workflow/task-result/v1"}`
- **Role Hint:** implementation

### `TASK-004` — Integrate Agent-Workflow as bundle-versioned native target consumer

- **Dependencies:** TASK-002
- **Expected Outputs:** native validation uses bundle APIs, preparation rejects incompatible bundle provenance, consumer mismatch and installed-product tests
- **Requirement Ids:** REQ-001, REQ-002, REQ-004
- **Result Contract:** `{"schema":"agent-workflow/task-result/v1"}`
- **Role Hint:** implementation

### `TASK-005` — Prove migration and cross-product conformance

- **Dependencies:** TASK-003, TASK-004
- **Expected Outputs:** exact-match/mismatch conformance matrix, migration fixture matrix, independent phase review and release evidence
- **Requirement Ids:** REQ-002, REQ-003, REQ-004
- **Result Contract:** `{"schema":"agent-workflow/task-result/v1"}`
- **Role Hint:** review

## Implementation phases

### `PHASE-001` — Inventory and bundle foundation

- **Description:** Freeze scope before extraction; create only the shared contract package.
- **Mandatory Order:** TASK-001, TASK-002
- **Task Ids:** TASK-001, TASK-002

### `PHASE-002` — Parallel producer and consumer integration

- **Description:** Run in parallel after the bundle is independently reviewed; DAG permits but does not force concurrency.
- **Task Ids:** TASK-003, TASK-004

### `PHASE-003` — Cross-product verification and sealing

- **Description:** Verify compatibility, migrations, boundaries, package installation, and independent review.
- **Mandatory Order:** TASK-005
- **Task Ids:** TASK-005

## Risks

### `RISK-001` — Publishing authority not yet selected

- **Description:** Local implementation can proceed, but external publication remains blocked pending repository/registry/signing authority.

## Unresolved questions

_None._

## Preservation claims

### `PRES-001` — Sealed historical artifacts are immutable; migration creates a linked derivative.

- **Source Ref:** SRC-001
- **Statement:** Sealed historical artifacts are immutable; migration creates a linked derivative.
- **Status:** represented
- **Target Refs:** REQ-003

## Provenance sources

### `SRC-001` — Provenance sources

- **Description:** Approved shared-contract architecture and migration requirements.
- **Kind:** user_decision
- **Locator:** shared-contract-program-20260830

## Extensions

`{}`

## Traceability

- `REQ-001` — **verified_by** → `AC-001`
- `REQ-002` — **verified_by** → `AC-002`
- `REQ-003` — **verified_by** → `AC-003`
- `REQ-004` — **verified_by** → `AC-004`
