from __future__ import annotations

import argparse
import json
from importlib.resources import files
from pathlib import Path

from . import __version__


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _compatibility() -> dict:
    path = _repo_root() / "compat" / "agent-workflow" / "compatibility.json"
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="specgen")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("version")
    sub.add_parser("compatibility")
    args = parser.parse_args(argv)
    if args.command == "version":
        print(__version__)
        return 0
    if args.command == "compatibility":
        print(json.dumps(_compatibility(), indent=2, sort_keys=True))
        return 0
    return 2
