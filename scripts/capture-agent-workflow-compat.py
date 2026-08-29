#!/usr/bin/env python3
"""Capture the Agent-Workflow compatibility inputs used by SpecGen."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tomllib
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git(source: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(source), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--specgen-source", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    source = args.source.resolve()
    output = args.output.resolve()
    specgen_source = args.specgen_source.resolve()
    version = (source / "VERSION").read_text(encoding="utf-8").strip()
    project = tomllib.loads((source / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    specgen_project = tomllib.loads((specgen_source / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    schemas = {
        str(path.relative_to(source)): sha256(path)
        for path in sorted((source / "schemas").glob("*.json"))
    }
    snapshot = {
        "schema": "specgen/agent-workflow-compatibility-snapshot/v1",
        "product": "agent-workflow",
        "version": version,
        "source": {
            "git_commit": git(source, "rev-parse", "HEAD"),
            "dirty": bool(git(source, "status", "--porcelain")),
        },
        "python": {
            "projects": {
                "agent-workflow": {
                    "requires_python": project.get("requires-python"),
                    "dependencies": sorted(project.get("dependencies", [])),
                },
                "specgen": {
                    "requires_python": specgen_project.get("requires-python"),
                    "dependencies": sorted(specgen_project.get("dependencies", [])),
                },
            },
        },
        "schemas": schemas,
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "SNAPSHOT.json").write_text(
        json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"captured Agent-Workflow {version}: {len(schemas)} schemas -> {output / 'SNAPSHOT.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
