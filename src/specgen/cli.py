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
from .repository import analyze_repository
from .drift import repository_drift
from .contracts import known_contracts
from .evals import evaluation_intent
from .agent_workflow import compile_prompt_pack, compile_evaluation_plan
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

    eval_parser = sub.add_parser("evals")
    eval_sub = eval_parser.add_subparsers(dest="eval_command", required=True)
    eval_intent_parser = eval_sub.add_parser("intent")
    eval_intent_parser.add_argument("path")

    aw_parser = sub.add_parser("agent-workflow")
    aw_sub = aw_parser.add_subparsers(dest="aw_command", required=True)
    aw_compile = aw_sub.add_parser("compile")
    aw_compile.add_argument("path")
    aw_compile.add_argument("--output", required=True)

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

    repo_parser = sub.add_parser("repo")
    repo_sub = repo_parser.add_subparsers(dest="repo_command", required=True)
    analyze_parser = repo_sub.add_parser("analyze")
    analyze_parser.add_argument("path")
    analyze_parser.add_argument("--spec")
    analyze_parser.add_argument("--mode", choices=mode_names(), default="guided")
    drift_parser = repo_sub.add_parser("drift")
    drift_parser.add_argument("analysis")
    drift_parser.add_argument("path")

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
    if args.command == "evals" and args.eval_command == "intent":
        try:
            document = _load_json(args.path)
            if not validate(document).valid:
                raise ValueError("cannot derive evaluation intent from invalid canonical snapshot")
            intent = evaluation_intent(document)
            if not validate(intent).valid:
                raise ValueError("generated evaluation intent failed its public contract")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"specgen: {exc}")
            return 2
        print(json.dumps(intent, indent=2, sort_keys=True, ensure_ascii=False))
        return 0
    if args.command == "agent-workflow" and args.aw_command == "compile":
        try:
            document = _load_json(args.path)
            pack, prompts = compile_prompt_pack(document)
            plan = compile_evaluation_plan(document)
            out = Path(args.output)
            out.mkdir(parents=True, exist_ok=True)
            (out / "pack.yaml").write_text(json.dumps(pack, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
            for rel, content in prompts.items():
                target = out / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
            if plan is not None:
                (out / "evaluation-plan.json").write_text(json.dumps(plan, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"specgen: {exc}")
            return 2
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
    if args.command == "repo" and args.repo_command == "analyze":
        try:
            spec = _load_json(args.spec) if args.spec else None
            report = analyze_repository(args.path, spec, args.mode)
            if not validate(report).valid:
                raise ValueError("generated repository analysis failed its public contract")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"specgen: {exc}")
            return 2
        print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
        return 1 if any(item["severity"] == "blocker" for item in report["contradictions"]) else 0
    if args.command == "repo" and args.repo_command == "drift":
        try:
            report = repository_drift(_load_json(args.analysis), args.path)
            if not validate(report).valid:
                raise ValueError("generated repository drift report failed its public contract")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"specgen: {exc}")
            return 2
        print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
        return 1 if report["drifted"] else 0
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
