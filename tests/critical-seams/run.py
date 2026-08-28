#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from specgen.cli import main as cli_main

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        try:
            code = cli_main(list(args))
        except SystemExit as exc:
            code = int(exc.code or 0)
    return subprocess.CompletedProcess(args, code, stdout.getvalue(), stderr.getvalue())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    checks = 0
    version_check = subprocess.run(
        [sys.executable, str(ROOT / "tests" / "release" / "verify_versions.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    require(version_check.returncode == 0, f"version agreement: {version_check.stderr or version_check.stdout}")
    checks += 1
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
    for contract in ("specgen/spec/v1alpha2", "specgen/authoring-event/v1alpha1", "specgen/semantic-delta/v1alpha1", "specgen/elicitation-plan/v1alpha1", "specgen/repository-analysis/v1alpha1", "specgen/repository-drift/v1alpha1"):
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

    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "brownfield"
        (repo / "contracts").mkdir(parents=True)
        (repo / "api").mkdir()
        (repo / "pyproject.toml").write_text(
            '[project]\nname = "brownfield"\nversion = "0.1.0"\n[project.scripts]\nbrown = "brownfield:main"\n',
            encoding="utf-8",
        )
        (repo / "contracts" / "thing.schema.json").write_text(
            '{"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object"}\n',
            encoding="utf-8",
        )
        (repo / "api" / "openapi.yaml").write_text('openapi: "3.1.0"\ninfo:\n  title: Brownfield\n  version: "1"\npaths: {}\n', encoding="utf-8")
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        subprocess.run(["git", "-C", str(repo), "config", "user.email", "specgen@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(repo), "config", "user.name", "SpecGen Seam"], check=True)
        subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
        subprocess.run(["git", "-C", str(repo), "commit", "-qm", "fixture"], check=True)

        analysis_result = run("repo", "analyze", str(repo), "--mode", "agent-workflow")
        require(analysis_result.returncode == 0, f"repo analyze: {analysis_result.stderr or analysis_result.stdout}")
        analysis = json.loads(analysis_result.stdout)
        require(analysis["schema"] == "specgen/repository-analysis/v1alpha1", "repo analyze: wrong contract")
        require(analysis["baseline"]["kind"] == "git" and len(analysis["baseline"]["revision"]) == 40, "repo analyze: git baseline missing")
        kinds = {item["kind"] for item in analysis["interfaces"]}
        require({"openapi", "python-console-script"}.issubset(kinds), f"repo analyze: interface discovery missing: {sorted(kinds)}")
        require(any(item["kind"] == "json-schema" for item in analysis["data_contracts"]), "repo analyze: json-schema discovery missing")
        require(analysis["target_context"]["expected_version"] == "0.9.0", "repo analyze: Agent-Workflow context missing")
        analysis_path = Path(tmp) / "analysis.json"
        analysis_path.write_text(analysis_result.stdout, encoding="utf-8")
        validation = run("validate", str(analysis_path), "--json")
        require(validation.returncode == 0, f"repo analysis contract validation: {validation.stdout}")
    checks += 1

    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "drift"
        repo.mkdir()
        tracked = repo / "thing.schema.json"
        tracked.write_text('{"type":"object"}\n', encoding="utf-8")
        analysis_result = run("repo", "analyze", str(repo))
        require(analysis_result.returncode == 0, f"repo drift setup: {analysis_result.stderr or analysis_result.stdout}")
        analysis_path = Path(tmp) / "analysis.json"
        analysis_path.write_text(analysis_result.stdout, encoding="utf-8")
        clean = run("repo", "drift", str(analysis_path), str(repo))
        require(clean.returncode == 0 and json.loads(clean.stdout)["drifted"] is False, f"repo drift clean: {clean.stderr or clean.stdout}")
        tracked.write_text('{"type":"string"}\n', encoding="utf-8")
        changed = run("repo", "drift", str(analysis_path), str(repo))
        changed_doc = json.loads(changed.stdout)
        require(changed.returncode == 1 and changed_doc["drifted"] is True, f"repo drift changed: {changed.stderr or changed.stdout}")
        require(any(item["kind"] == "modified" and item["path"] == "thing.schema.json" for item in changed_doc["changes"]), "repo drift: modified evidence missing")
    checks += 1

    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "missing"
        repo.mkdir()
        spec = json.loads((FIXTURES / "valid.spec.json").read_text(encoding="utf-8"))
        spec["provenance"]["sources"].append({
            "id": "SRC-REPO", "kind": "repository", "description": "Expected repository evidence", "locator": "missing.txt"
        })
        spec_path = Path(tmp) / "spec.json"
        spec_path.write_text(json.dumps(spec), encoding="utf-8")
        result = run("repo", "analyze", str(repo), "--spec", str(spec_path))
        require(result.returncode == 1, f"repo missing evidence: expected blocker; got {result.stderr or result.stdout}")
        report = json.loads(result.stdout)
        require(any(item["kind"] == "missing_evidence" and item["path"] == "missing.txt" for item in report["contradictions"]), "repo missing evidence: contradiction missing")
    checks += 1

    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "plain"
        repo.mkdir()
        (repo / "README.md").write_text("# plain\n", encoding="utf-8")
        first = run("repo", "analyze", str(repo))
        second = run("repo", "analyze", str(repo))
        require(first.returncode == second.returncode == 0, f"directory baseline: {first.stderr or second.stderr}")
        a, b = json.loads(first.stdout), json.loads(second.stdout)
        require(a["baseline"] == b["baseline"] and a["baseline"]["kind"] == "directory", "directory baseline: not deterministic")
    checks += 1

    print(f"critical seams: {checks} checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
