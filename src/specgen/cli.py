from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from . import __version__
from .canonical import snapshot_digest
from .contracts import known_contracts
from .validate import validate


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _compatibility() -> dict[str, Any]:
    path = _repo_root() / "compat" / "agent-workflow" / "compatibility.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _load_json(path: str) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("document root must be a JSON object")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="specgen")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("version")
    sub.add_parser("compatibility")
    sub.add_parser("contracts")

    validate_parser = sub.add_parser("validate")
    validate_parser.add_argument("path")
    validate_parser.add_argument("--json", action="store_true", dest="as_json")

    digest_parser = sub.add_parser("digest")
    digest_parser.add_argument("path")

    args = parser.parse_args(argv)
    if args.command == "version":
        print(__version__)
        return 0
    if args.command == "compatibility":
        print(json.dumps(_compatibility(), indent=2, sort_keys=True))
        return 0
    if args.command == "contracts":
        print("\n".join(known_contracts()))
        return 0
    if args.command == "validate":
        try:
            result = validate(_load_json(args.path))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"specgen: {exc}")
            return 2
        if args.as_json:
            print(json.dumps(result.as_dict(), indent=2, sort_keys=True))
        else:
            for item in result.diagnostics:
                print(f"{item.severity}: {item.code}: {item.path}: {item.message}")
            print("valid" if result.valid else "invalid")
        return 0 if result.valid else 1
    if args.command == "digest":
        try:
            document = _load_json(args.path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"specgen: {exc}")
            return 2
        if document.get("schema") != "specgen/spec/v1alpha2":
            print("specgen: digest currently supports specgen/spec/v1alpha2 only")
            return 2
        print(snapshot_digest(document))
        return 0
    return 2
