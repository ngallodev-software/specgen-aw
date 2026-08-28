#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures"
ENV = dict(os.environ, PYTHONPATH=str(ROOT / "src"))


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "specgen", *args],
        cwd=ROOT,
        env=ENV,
        text=True,
        capture_output=True,
        check=False,
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    checks = 0
    cases = [
        ("valid snapshot", "valid.spec.json", 0, None),
        ("valid authoring event", "valid.authoring-event.json", 0, None),
        ("broken reference", "broken-reference.spec.json", 1, "ref.verification"),
        ("dependency cycle", "dependency-cycle.spec.json", 1, "task.dependency_cycle"),
        ("stale digest", "stale-digest.spec.json", 1, "snapshot.digest"),
    ]
    for name, fixture, expected_code, expected_diagnostic in cases:
        result = run("validate", str(FIXTURES / fixture), "--json")
        require(result.returncode == expected_code, f"{name}: expected exit {expected_code}, got {result.returncode}: {result.stderr or result.stdout}")
        payload = json.loads(result.stdout)
        require(payload["valid"] is (expected_code == 0), f"{name}: validity mismatch")
        if expected_diagnostic:
            codes = {item["code"] for item in payload["diagnostics"]}
            require(expected_diagnostic in codes, f"{name}: missing {expected_diagnostic}; got {sorted(codes)}")
        checks += 1

    digest = run("digest", str(FIXTURES / "valid.spec.json"))
    require(digest.returncode == 0, f"digest: {digest.stderr or digest.stdout}")
    value = digest.stdout.strip()
    require(value.startswith("sha256:") and len(value) == 71, "digest: expected sha256:<64 hex>")
    checks += 1

    contracts = run("contracts")
    require(contracts.returncode == 0, f"contracts: {contracts.stderr or contracts.stdout}")
    for contract in ("specgen/spec/v1alpha2", "specgen/authoring-event/v1alpha1", "specgen/semantic-delta/v1alpha1", "specgen/elicitation-plan/v1alpha1"):
        require(contract in contracts.stdout, f"contracts: {contract} missing")
    checks += 1

    modes = run("modes")
    require(modes.returncode == 0, f"modes: {modes.stderr or modes.stdout}")
    for name in ("express", "guided", "strict", "agent-workflow"):
        require(f"{name}:" in modes.stdout, f"modes: {name} missing")
    checks += 1

    aw_blocked = run("author", "assess", str(FIXTURES / "valid.spec.json"), "--mode", "agent-workflow")
    require(aw_blocked.returncode == 1, f"agent-workflow guardrails: expected blocked; got {aw_blocked.stdout}")
    blocked_plan = json.loads(aw_blocked.stdout)
    require(blocked_plan["schema"] == "specgen/elicitation-plan/v1alpha1", "agent-workflow guardrails: wrong plan contract")
    require(blocked_plan["blocker_count"] >= 3, "agent-workflow guardrails: expected phased/result/evaluation blockers")
    checks += 1

    aw_ready = run("author", "assess", str(FIXTURES / "agent-workflow-ready.spec.json"), "--mode", "agent-workflow")
    require(aw_ready.returncode == 0, f"agent-workflow ready assessment: {aw_ready.stderr or aw_ready.stdout}")
    ready_plan = json.loads(aw_ready.stdout)
    require(ready_plan["ready"] is True and ready_plan["blocker_count"] == 0, "agent-workflow ready assessment: expected ready")
    plan_path = Path(tempfile.mkdtemp()) / "elicitation-plan.json"
    plan_path.write_text(aw_ready.stdout, encoding="utf-8")
    plan_validation = run("validate", str(plan_path), "--json")
    require(plan_validation.returncode == 0, f"elicitation plan validation: {plan_validation.stdout}")
    checks += 1

    with tempfile.TemporaryDirectory() as tmp:
        finalized = Path(tmp) / "finalized.json"
        result = run("author", "finalize", str(FIXTURES / "agent-workflow-ready.spec.json"), "--mode", "agent-workflow", "--output", str(finalized))
        require(result.returncode == 0, f"candidate finalize: {result.stderr or result.stdout}")
        final_doc = json.loads(finalized.read_text(encoding="utf-8"))
        require(str(final_doc["snapshot"].get("content_digest", "")).startswith("sha256:"), "candidate finalize: digest missing")
        validation = run("validate", str(finalized), "--json")
        require(validation.returncode == 0, f"candidate finalize validation: {validation.stdout}")
    checks += 1

    rendered_a = run("render", str(FIXTURES / "valid.spec.json"))
    rendered_b = run("render", str(FIXTURES / "valid.spec.json"))
    require(rendered_a.returncode == rendered_b.returncode == 0, f"render: {rendered_a.stderr or rendered_b.stderr}")
    require(rendered_a.stdout == rendered_b.stdout, "render: output is not deterministic")
    require("REQ-001" in rendered_a.stdout and "Traceability" in rendered_a.stdout, "render: critical content missing")
    checks += 1

    delta = run("diff", str(FIXTURES / "valid.spec.json"), str(FIXTURES / "modified.spec.json"))
    require(delta.returncode == 0, f"diff: {delta.stderr or delta.stdout}")
    delta_doc = json.loads(delta.stdout)
    require(delta_doc["schema"] == "specgen/semantic-delta/v1alpha1", "diff: wrong contract")
    require(any(item.get("entity_id") == "REQ-002" and item["kind"] == "added" for item in delta_doc["changes"]), "diff: REQ-002 addition missing")
    require(not any(item["path"].startswith("$.snapshot") for item in delta_doc["changes"]), "diff: snapshot bookkeeping leaked into semantic changes")
    checks += 1

    delta_path = Path(tempfile.mkdtemp()) / "delta.json"
    delta_path.write_text(delta.stdout, encoding="utf-8")
    delta_validation = run("validate", str(delta_path), "--json")
    require(delta_validation.returncode == 0, f"diff contract validation: {delta_validation.stdout}")
    checks += 1

    with tempfile.TemporaryDirectory() as tmp:
        log = Path(tmp) / "events.ndjson"
        first = run("events", "append", str(log), str(FIXTURES / "valid.authoring-event.json"))
        require(first.returncode == 0, f"events first append: {first.stderr or first.stdout}")
        gap = run("events", "append", str(log), str(FIXTURES / "gap.authoring-event.json"))
        require(gap.returncode == 2 and "sequence must be 2" in gap.stdout, f"events gap should fail: {gap.stderr or gap.stdout}")
        second = run("events", "append", str(log), str(FIXTURES / "second.authoring-event.json"))
        require(second.returncode == 0, f"events second append: {second.stderr or second.stdout}")
        lines = log.read_text(encoding="utf-8").splitlines()
        require(len(lines) == 2, "events: expected exactly two persisted events")
        require([json.loads(line)["sequence"] for line in lines] == [1, 2], "events: persisted sequence mismatch")
    checks += 1

    print(f"critical seams: {checks} checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
