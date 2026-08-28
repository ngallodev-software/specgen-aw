from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from . import __version__
from .canonical import snapshot_digest
from .diff import semantic_delta
from .history import append_event
from .compiler import finalize_candidate
from .elicitation import assess
from .modes import mode_descriptions, mode_names
from .render import render_markdown
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
    sub.add_parser("modes")

    author_parser = sub.add_parser("author")
    author_sub = author_parser.add_subparsers(dest="author_command", required=True)
    assess_parser = author_sub.add_parser("assess")
    assess_parser.add_argument("path")
    assess_parser.add_argument("--mode", choices=mode_names(), default="guided")
    finalize_parser = author_sub.add_parser("finalize")
    finalize_parser.add_argument("path")
    finalize_parser.add_argument("--mode", choices=mode_names(), default="guided")
    finalize_parser.add_argument("--output", required=True)

    validate_parser = sub.add_parser("validate")
    validate_parser.add_argument("path")
    validate_parser.add_argument("--json", action="store_true", dest="as_json")

    digest_parser = sub.add_parser("digest")
    digest_parser.add_argument("path")

    render_parser = sub.add_parser("render")
    render_parser.add_argument("path")
    render_parser.add_argument("--output")

    diff_parser = sub.add_parser("diff")
    diff_parser.add_argument("before")
    diff_parser.add_argument("after")

    events_parser = sub.add_parser("events")
    events_sub = events_parser.add_subparsers(dest="events_command", required=True)
    append_parser = events_sub.add_parser("append")
    append_parser.add_argument("log")
    append_parser.add_argument("event")

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
    if args.command == "modes":
        for name, description in mode_descriptions().items():
            print(f"{name}: {description}")
        return 0
    if args.command == "author" and args.author_command == "assess":
        try:
            plan = assess(_load_json(args.path), args.mode)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"specgen: {exc}")
            return 2
        print(json.dumps(plan, indent=2, sort_keys=True, ensure_ascii=False))
        return 0 if plan["ready"] else 1
    if args.command == "author" and args.author_command == "finalize":
        try:
            document = finalize_candidate(_load_json(args.path), args.mode)
            Path(args.output).write_text(
                json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"specgen: {exc}")
            return 2
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
    if args.command == "render":
        try:
            document = _load_json(args.path)
            result = validate(document)
            if not result.valid:
                raise ValueError("cannot render invalid canonical snapshot")
            output = render_markdown(document)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"specgen: {exc}")
            return 2
        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
        else:
            print(output, end="")
        return 0
    if args.command == "diff":
        try:
            before = _load_json(args.before)
            after = _load_json(args.after)
            if not validate(before).valid or not validate(after).valid:
                raise ValueError("cannot diff invalid canonical snapshots")
            delta = semantic_delta(before, after)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"specgen: {exc}")
            return 2
        print(json.dumps(delta, indent=2, sort_keys=True, ensure_ascii=False))
        return 0
    if args.command == "events" and args.events_command == "append":
        try:
            event = _load_json(args.event)
            append_event(args.log, event)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"specgen: {exc}")
            return 2
        return 0
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
