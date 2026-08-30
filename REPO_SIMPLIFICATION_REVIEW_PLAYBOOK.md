# Thorough repository simplification analysis and review playbook

> Purpose: a reusable, evidence-first procedure and prompt for deciding what a
> repository can safely delete, merge, replace, or make smaller. It produces a
> review artifact; it does not authorize implementation.

## 1. What this review is for

A simplification review answers a narrow question: **what is the smallest
> coherent system that still meets the repository's stated behavior,
> compatibility, safety, provenance, and operational contracts?**

It is not a rewrite proposal, a test-count exercise, a dependency purge, or a
license to remove code that merely looks repetitive. The preferred outcome is
often a short, ranked list of deletions and bounded consolidations. “Keep it”
is a valid and useful finding when a boundary protects an actual contract.

The reviewer must distinguish these evidence classes:

| class | meaning | required support |
| --- | --- | --- |
| observed | direct current fact | path, symbol, declaration, test, command, or artifact |
| inference | conclusion from multiple facts | each material observation and reasoning |
| recommendation | proposed future action | expected benefit, risk, rollback, and validation |
| deletion candidate | code/artifact claimed unused or redundant | references/callers plus build/package/operational checks |
| open question | material uncertainty | what is unknown and the smallest check that resolves it |

Never present an inference as an observed fact, or a passing test as proof of
release, live, deployment, browser, or operational acceptance.

## 2. Inputs and authority order

Establish the authority order before evaluating anything. Prefer, in order:

1. explicit user scope and preservation requirements;
2. checked-in runtime/security/data contracts and accepted ADRs;
3. current source, package manifests, schemas, and generated-from declarations;
4. current tests, CI/release scripts, and reproducible command output;
5. current deployment/operator documentation where it names real behavior;
6. historical audits, receipts, issue trackers, and stale documents.

Historical material is leads, not authority. If an old audit and current source
conflict, record the conflict and use current verified evidence. Do not revive
removed compatibility paths merely because a historical test refers to them.

Before beginning, record:

- repository root, commit/branch, exact worktree state, audit date, reviewer;
- scope, exclusions, and whether the task is read-only or implementation;
- commands that are prohibited (for example live collection, deployment, data
  mutation, package publication, destructive cleanup);
- the contracts that cannot be weakened without an explicit product decision;
- whether generated outputs and untracked files are user-owned or disposable.

## 3. Safety rules for a read-only review

1. Capture `git status --short` before and after exploration. Preserve all
   pre-existing changes; do not normalize a dirty worktree.
2. Do not delete, overwrite, install globally, publish, deploy, migrate data,
   mutate external systems, or run live collection merely to make a review
   feel complete.
3. Treat generated output as a candidate only after proving its origin,
   tracking status, and release/build relevance. An untracked directory is not
   automatically safe to remove.
4. Use dry-runs and deterministic/offline checks before networked or stateful
   checks. State explicitly when a layer was not verified.
5. For every change candidate, search all callers, imports, entry points,
   package data declarations, scripts, docs, and tests before recommending a
   removal. Dynamic imports, subprocess invocation, plugins, reflection, and
   configuration may defeat a simple text search.
6. Never simplify away trust boundaries, authentication/authorization,
   input validation, provenance, recovery/rollback behavior, data constraints,
   observability required for incident response, or explicit accessibility
   requirements without an explicit decision to change the contract.

## 4. Review workflow

### Phase A — orient and establish a baseline

Read the repository's top-level instructions, architecture, runtime contracts,
operator workflow, package manifests, CI configuration, and the latest relevant
audits/receipts. Build a small component map: component, owner responsibility,
public entry points, persistent state, external I/O, and authoritative tests.

Run cheap read-only orientation first:

```bash
git status --short
git log -5 --oneline
rg --files -g '!*build*' -g '!*.egg-info*' | wc -l
rg -n 'version|entry.?point|console_scripts|scripts' pyproject.toml package.json Cargo.toml go.mod 2>/dev/null
```

Adapt the commands to the repository; do not create a universal wrapper just
for the audit.

### Phase B — map real behavior, not file names

For each important entry point, trace the concrete flow from command/request to
side effect and result. Capture only flows that matter to the scope:

```text
entry point → request/config normalization → policy/authorization → domain service
→ persistence/external adapter → result/receipt/report
```

Record where the following authorities live when relevant:

- routing/network policy and egress selection;
- identity, permissions, and case/tenant selection;
- canonical datastore and projections/caches;
- state-machine transitions, receipts, cancellation, and recovery;
- provider/plugin contracts and subprocess boundaries;
- schema/version/packaging/release metadata.

Use code-graph tooling first when available for symbols, callers, dependencies,
fan-in/out, and call paths. Confirm graph freshness and compare Git status
before and after indexing. If it is unavailable, stale, or writes unapproved
residue, fall back to narrow `rg`, package manifests, and decisive source/test
reads. Do not substitute a repository-wide dump for a targeted call-flow.

### Phase C — hunt simplification opportunities

Apply this order to every candidate:

1. **Delete:** unreachable code, duplicate generated output, obsolete
   compatibility layers, unused flags, dead docs, or unused dependencies.
2. **Reuse:** an existing repository service, standard-library feature, native
   platform capability, or already-declared dependency already meets the need.
3. **Consolidate:** two sources claim the same authority (version, installer,
   CLI, doc, test matrix, configuration, lifecycle).
4. **Shrink:** a proven shared lifecycle or wrapper can become one internal
   helper without erasing semantic differences.
5. **Defer:** evidence is insufficient, behavior differs, or a change crosses
   a high-risk contract.

Useful search targets include:

- duplicated installers, CI wrappers, test runners, release scripts, and docs;
- multiple version declarations, feature flags, defaults, and schemas;
- one-implementation interfaces, factories, adapters, forwarding modules, and
  configuration never read outside tests;
- copy-pasted lifecycle code (start/finish/error/receipt/retry) with truly
  identical invariants;
- direct datastore access bypassing the declared application facade;
- path bootstraps, `sys.path` changes, hand-rolled JSON/config parsing, homegrown
  retry/cache/URL/UUID/date helpers that duplicate stable built-ins;
- generated trees, caches, build products, archives, and vendored copies;
- optional dependencies whose imports and package behavior prove unnecessary.

Do not flag a boundary only because it has one implementation. A subprocess
adapter, plugin seam, data facade, or separate component may be deliberately
protecting deployment independence, trust, provenance, test isolation, or a
stable external contract.

### Phase D — falsify each candidate

For each proposal, actively try to disprove it:

| proposal | minimum falsification checks |
| --- | --- |
| delete function/module | callers/imports, dynamic loading/config strings, CLI/package entry points, tests, docs, installed artifact |
| delete generated output | generator source, tracking/ignore status, build/release inclusion, byte/content comparison, clean build reproduction |
| merge docs | canonical links, operator install locations, release packaging, stale-copy detection, redirect/forwarding plan |
| consolidate versions | package build metadata, runtime `--version`, release scripts, generated manifests, docs/badges, compatibility policy |
| extract shared helper | all callers, divergent error/persistence/provenance paths, one characterization test for failure behavior |
| replace a dependency | direct/indirect imports, extras/entry points, isolated install, package smoke, license/feature parity |
| simplify persistence | transaction boundaries, schema/migration ownership, concurrency, IDs/types, integrity constraints, backup/export behavior |
| simplify routing/security | explicit policy check, failure mode, audit metadata, dry-run and negative-path test; default to defer |

If evidence disagrees, report the disagreement. The right outcome is often a
research ticket rather than a refactor.

### Phase E — validate in layers

Use the repository's canonical commands. Report exact commands and results,
including failures and warnings. Keep these layers separate:

| layer | evidence it can establish | does not establish |
| --- | --- | --- |
| static/source | references, declarations, obvious duplication | runtime behavior or packaging |
| focused test | characterization of the changed seam | component/system behavior |
| component test | local component contract | cross-component/release behavior |
| canonical offline matrix | declared offline integration coverage | live network/deployment/acceptance |
| build/wheel/install smoke | package layout and entry points | operational deployment |
| CI/release | automation in that environment | production acceptance |
| dry-run | command shaping and preflight logic | successful live collection/operation |
| live check | actual external behavior | broad regression freedom |

Do not run a full matrix merely by habit when the review is read-only and a
targeted check proves the claim. Conversely, do not claim broad safety from a
single focused test.

### Phase F — write an implementable, non-authorizing report

Use the required report format below. Rank items by expected maintenance
reduction and contract risk, not by how easy they are to describe. Every item
must say exactly what to do next and exactly what would prove it safe.

## 5. Required report format

```markdown
# <Repository> simplification follow-up — <YYYY-MM-DD>

## 1. Machine summary

| field | value |
| --- | --- |
| repo | ... |
| audit mode | read-only / implementation receipt |
| baseline | branch, commit, dirty-worktree statement |
| graph/tooling | available/fresh/unavailable and residue check |
| tests run | exact scope and aggregate result |
| live/external mutation | not run / exact authorized action |
| verdict | NO_REWRITE / REWRITE / BLOCKED |
| confidence | high / medium / low, with reason |

## 2. Executive conclusion

State whether a rewrite is warranted and the three highest-value actions.
State what must remain as an intentional boundary.

## 3. Prior-audit reconciliation

| prior ID/claim | current status | current evidence | disposition |
| --- | --- | --- | --- |

## 4. Architecture and decisive flows

Include only the components, authority boundaries, and flows that explain the
recommendations. Mark observed facts versus inferences.

## 5. Ranked simplification ledger

| id | priority | class | finding | evidence | benefit | smallest safe action | risk/dependencies | validation | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Allowed classes: `delete`, `stdlib`, `native`, `reuse`, `consolidate`,
`boundary`, `shrink`, `dependency`, `research`. Status is `new`, `confirmed`,
`implemented`, `deferred`, or `rejected`.

## 6. Deletion and replacement assessment

Separate proven deletions, candidates needing a clean-build/package smoke, and
items intentionally retained. Name the existing library/platform facility when
recommending replacement, and include an isolated proof plan.

## 7. Do-not-simplify boundaries

List every safety, data, provenance, compatibility, or operator boundary the
review relied on. Explain the contract in one sentence each.

## 8. Proposed phase order

For each phase: scope, checkpoint/rollback, one owner, preconditions,
independent validation, and the condition that blocks the next phase.

## 9. Validation matrix

| layer | command/check | result | limitation |
| --- | --- | --- | --- |

## 10. Open questions and stop conditions

State unresolved questions, the minimal next research action, and conditions
under which no change should be made.
```

## 6. Full reusable prompt template

Copy this template and replace every bracketed field. It is intentionally
complete so an independent reviewer can reproduce the work without relying on
conversation memory.

```text
You are conducting a thorough, evidence-first simplification analysis and
repository review of [REPOSITORY_PATH] on [DATE]. This is [READ_ONLY /
IMPLEMENTATION-AUTHORIZED] work. The objective is to identify the smallest
safe reductions in code, dependencies, duplicated authority, generated noise,
and operational complexity while preserving the repository's actual contracts.

Scope:
- Include: [COMPONENTS / DIRECTORIES / FEATURES].
- Exclude: [DIRECTORIES / EXTERNAL SYSTEMS / OUT-OF-SCOPE AREAS].
- Preserve: [USER-REQUIRED BEHAVIORS, COMPATIBILITY, SECURITY, DATA,
  PROVENANCE, ACCESSIBILITY, PERFORMANCE BOUNDARIES].
- Do not: [LIVE COLLECTION, DEPLOYMENT, DATA MUTATION, INSTALLATION, PUBLISH,
  DELETE/OVERWRITE, COMMIT/PUSH, OR OTHER FORBIDDEN ACTIONS].
- Existing artifacts to reconcile: [PRIOR AUDITS, RESULTS, RECEIPTS, PLANS].

Authority and discipline:
1. Read local AGENTS/instructions, architecture, runtime/security/data
   contracts, operator workflow, accepted ADRs, manifests, CI, and the listed
   prior artifacts before drawing conclusions.
2. Treat current source/contracts/tests as authority over historical reports.
   Classify every conclusion as observed fact, inference, recommendation,
   deletion candidate, or open question.
3. Capture Git porcelain before and after. Preserve all user-owned dirty work.
   If tooling creates unauthorized residue, stop using it and report it.
4. Use code-graph tooling first for structure, symbols, callers, dependency
   paths, fan-in/out, and impact. Verify index freshness and exact-worktree
   scope; use a non-persistent index unless repository-local persistence is
   explicitly authorized. If unavailable/stale/residue-producing, use narrow
   searches and decisive source, manifest, test, and docs reads.
5. Never infer that duplicated-looking code is removable. Search imports,
   callers, dynamic/plugin/config references, entry points, package data,
   scripts, tests, docs, and installed/build artifacts. Preserve deliberate
   isolation boundaries unless evidence proves they are obsolete.
6. Do not recommend a rewrite unless staged changes demonstrably cannot
   preserve the stated contracts. Large files or many tests alone are not
   rewrite evidence.
7. Apply the simplification ladder to each candidate: delete; reuse existing
   repository capability; use standard library/native platform; consolidate a
   true duplicate authority; shrink a proven repeated lifecycle; otherwise
   defer. Do not add a framework, service, broker, abstraction, or dependency
   to make the review appear complete.
8. Do not weaken validation, security, access control, routing policy,
   provenance, receipts, persistence integrity, migrations, recovery, or
   accessibility without an explicit product decision. For routing/data cases,
   test failure paths and fail-closed behavior, not just happy paths.
9. Use repository-canonical validation commands when practical. Report exact
   command, result, warnings, environment assumptions, and what the check does
   not prove. Separate static, focused, component, offline matrix, packaging,
   CI/release, dry-run, and live evidence.

Required investigation:
- Establish baseline repository state, component map, public entry points,
  canonical state stores, external I/O, package/release authorities, and tests.
- Trace the decisive flows from entry point through normalization/policy/domain
  service/persistence or external adapter to result/receipt.
- Reconcile every relevant prior-audit claim against current source and label it
  confirmed, implemented, stale, disproven, deferred, or still unverified.
- Search for dead code, generated/build noise, duplicate docs/installers/test
  wrappers/version declarations, one-implementation abstractions, delegating
  wrappers, unused configuration, redundant dependencies, hand-rolled stdlib
  helpers, direct data-store bypasses, and identical lifecycle code.
- Falsify each promising candidate using the appropriate caller/import/build/
  package/contract checks. Include a minimal safe remediation and rollback.
- Identify explicit do-not-simplify boundaries and explain why they remain.

Deliver one Markdown report using this exact structure:
1. Machine summary.
2. Executive conclusion and rewrite verdict.
3. Prior-audit reconciliation table.
4. Architecture map and decisive call flows.
5. Ranked simplification ledger: ID, priority, class, finding, evidence,
   benefit, smallest safe action, risk/dependencies, validation, status.
6. Deletion/replacement assessment, separated into proven, needs proof, and
   intentionally retained.
7. Do-not-simplify contract boundaries.
8. Proposed phased order with checkpoint, rollback, owner, preconditions, and
   independent validation.
9. Validation matrix with commands/results/limitations.
10. Open questions, minimal next research action, and stop conditions.

Write concise evidence locators (path:symbol or path:line) rather than large
source excerpts. Do not modify repository code or existing review artifacts
unless implementation authority is separately granted.
```

## 7. Review quality gate

The report is ready only when:

- its baseline makes dirty-worktree ownership and mutation scope unambiguous;
- every material finding has current evidence and a clear classification;
- every deletion/replacement proposal has a falsification plan;
- safety/data/provenance boundaries are named rather than assumed;
- validation results and their limits are reported separately;
- recommendations are phased, reversible, and small enough to review;
- it says “defer” where evidence is insufficient.

If any condition is missing, the correct result is an incomplete review, not a
confident simplification plan.
