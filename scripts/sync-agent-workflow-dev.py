#!/usr/bin/env python3
"""Link the local Agent-Workflow development checkout into SpecGen."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tomllib
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    if path.is_file():
        h.update(path.read_bytes())
    else:
        for child in sorted(p for p in path.rglob("*") if p.is_file()):
            h.update(str(child.relative_to(path)).encode())
            h.update(child.read_bytes())
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    root = repo_root()
    config_path = root / "dev" / "agent-workflow.toml"
    config = tomllib.loads(config_path.read_text(encoding="utf-8"))["agent_workflow"]
    source = Path(os.environ.get("SPECGEN_AGENT_WORKFLOW_ROOT", config["source_root"])).resolve()
    if not source.is_dir():
        raise SystemExit(f"Agent-Workflow source root not found: {source}")
    observed_version = (source / "VERSION").read_text(encoding="utf-8").strip()
    if observed_version != config["product_version"]:
        raise SystemExit(f"expected Agent-Workflow {config['product_version']}, found {observed_version}")

    link_root = root / ".dev" / "agent-workflow" / "current"
    lock_path = root / ".dev" / "agent-workflow" / "lock.json"
    links = {}
    for relative in config["paths"]:
        target = source / relative
        if not target.exists():
            raise SystemExit(f"configured Agent-Workflow path not found: {target}")
        link = link_root / relative
        links[relative] = {"target": str(target), "sha256": digest(target)}
        if args.check:
            if not link.is_symlink() or link.resolve() != target:
                raise SystemExit(f"development link missing or stale: {link}")
            continue
        link.parent.mkdir(parents=True, exist_ok=True)
        if link.is_symlink() or link.is_file():
            link.unlink()
        elif link.is_dir():
            shutil.rmtree(link)
        link.symlink_to(target, target_is_directory=target.is_dir())

    if not args.check:
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        lock_path.write_text(
            json.dumps(
                {
                    "product": config["name"],
                    "product_version": config["product_version"],
                    "source_snapshot": config["source_snapshot"],
                    "source_root": str(source),
                    "links": links,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
    print(f"{'Checked' if args.check else 'Linked'} Agent-Workflow {observed_version} from {source}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
