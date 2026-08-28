#!/usr/bin/env python3
"""Fail-closed release check for SpecGen and Agent-Workflow versions."""

from __future__ import annotations

import json
import os
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))


def fail(message: str) -> None:
    raise SystemExit(f"version check failed: {message}")


def text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"cannot read {path}: {exc}")


def main() -> int:
    specgen_version = text(ROOT / "VERSION").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", specgen_version):
        fail(f"invalid SpecGen VERSION: {specgen_version!r}")

    project_version = tomllib.loads(text(ROOT / "pyproject.toml"))["project"]["version"]
    module_match = re.search(r'^__version__\s*=\s*["\']([^"\']+)', text(ROOT / "src/specgen/__init__.py"), re.M)
    if not module_match:
        fail("src/specgen/__init__.py has no __version__")
    if {specgen_version, project_version, module_match.group(1)} != {specgen_version}:
        fail(f"SpecGen versions disagree: VERSION={specgen_version}, pyproject={project_version}, module={module_match.group(1)}")

    maintained = [
        ROOT / "README.md",
        ROOT / "dev" / "README.md",
        ROOT / "docs" / "AGENT_WORKFLOW_INTEGRATION.md",
        ROOT / "docs" / "ARCHITECTURE.md",
        ROOT / "docs" / "DESIGN_PRINCIPLES.md",
        ROOT / "docs" / "ENGINEERING_POLICY.md",
        ROOT / "docs" / "ROADMAP.md",
        ROOT / "docs" / "VERSIONING.md",
        ROOT / "docs" / "adr" / "README.md",
        ROOT / "docs" / "research" / "ASSESSMENT_MATRIX.md",
        ROOT / "docs" / "research" / "PRIOR_ART.md",
        ROOT / "docs" / "research" / "PRIOR_ART_DEEP_REVIEW_01.md",
        ROOT / "docs" / "research" / "SOURCES_NEEDED.md",
        ROOT / "compat" / "agent-workflow" / "COMPATIBILITY.md",
    ]
    for path in maintained:
        body = text(path)
        if not re.search(rf"(?:document-version:|Document version:)\s*{re.escape(specgen_version)}", body):
            fail(f"{path.relative_to(ROOT)} does not declare SpecGen {specgen_version}")
        if path == ROOT / "README.md":
            applies = rf"applies-to:\s*SpecGen\s*{re.escape(specgen_version)}"
        else:
            applies = rf"Applies to SpecGen\s*{re.escape(specgen_version)}"
        if not re.search(applies, body):
            fail(f"{path.relative_to(ROOT)} has no matching applicability version")

    compatibility = json.loads(text(ROOT / "compat" / "agent-workflow" / "compatibility.json"))
    target = compatibility["target"]
    aw_version = target["product_version"]
    if compatibility["specgen_version"] != specgen_version:
        fail("compatibility metadata has the wrong SpecGen version")
    if target["name"] != "agent-workflow":
        fail("compatibility target is not Agent-Workflow")

    config_path = ROOT / "dev" / "agent-workflow.toml"
    if not config_path.is_file():
        config_path = ROOT / "dev" / "agent-workflow.example.toml"
    config = tomllib.loads(text(config_path))
    source = config["source"]
    if source["expected_product_version"] != aw_version:
        fail("development config and compatibility metadata disagree on Agent-Workflow version")
    live_root = Path(os.environ.get(source.get("env_override", "SPECGEN_AGENT_WORKFLOW_ROOT"), source["default_root"]))
    if not live_root.is_absolute():
        live_root = (ROOT / live_root).resolve()
    live_version = text(live_root / source["version_file"]).strip()
    if live_version != aw_version:
        fail(f"Agent-Workflow app VERSION={live_version}, expected {aw_version}")

    from specgen.agent_workflow import AW_VERSION
    from specgen.repository import _agent_workflow_context

    if AW_VERSION != aw_version:
        fail(f"specgen.agent_workflow.AW_VERSION={AW_VERSION}, expected {aw_version}")
    context = _agent_workflow_context()
    if context["expected_version"] != aw_version or context["observed_version"] != aw_version or not context["version_matches"]:
        fail(f"repository Agent-Workflow context is inconsistent: {context}")

    print(f"version checks: SpecGen {specgen_version}; Agent-Workflow app/module {aw_version}; all consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
