"""Optional Agent-Workflow 0.9.0 plugin adapter for SpecGen.

This module is loaded only through Agent-Workflow's public trusted plugin API.
SpecGen core has no runtime dependency on Agent-Workflow.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from . import __version__
from .agent_workflow import AW_VERSION
from .api import (
    agent_workflow_compatibility,
    analyze_repository,
    assess,
    compile_agent_workflow_target,
    finalize_candidate,
    mode_names,
    write_agent_workflow_target,
)

PLUGIN_NAME = "agent-workflow-spec"


def _load_json(path: str) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("document root must be a JSON object")
    return value


def _write_json(path: str, value: dict[str, Any]) -> None:
    Path(path).write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def configure(parser: argparse.ArgumentParser) -> None:
    sub = parser.add_subparsers(dest="spec_command", required=True)
    sub.add_parser("compatibility", help="show SpecGen's pinned Agent-Workflow compatibility")

    assess_parser = sub.add_parser("assess", help="assess specification authoring readiness")
    assess_parser.add_argument("path")
    assess_parser.add_argument("--mode", choices=mode_names(), default="agent-workflow")

    analyze_parser = sub.add_parser("analyze", help="analyze repository evidence for a specification")
    analyze_parser.add_argument("repository")
    analyze_parser.add_argument("--spec")
    analyze_parser.add_argument("--mode", choices=mode_names(), default="agent-workflow")

    finalize_parser = sub.add_parser("finalize", help="finalize a ready canonical specification")
    finalize_parser.add_argument("path")
    finalize_parser.add_argument("--mode", choices=mode_names(), default="agent-workflow")
    finalize_parser.add_argument("--output", required=True)

    compile_parser = sub.add_parser("compile", help="compile an Agent-Workflow prompt pack")
    compile_parser.add_argument("path")
    compile_parser.add_argument("--output", required=True)
    compile_parser.add_argument("--repository-analysis")
    compile_parser.add_argument("--repository-root")


def _fail(message: str, code: int = 2) -> None:
    print(f"specgen: {message}", file=sys.stderr)
    raise SystemExit(code)


def execute(args: argparse.Namespace, context: Any) -> Any:
    if context.host_version != AW_VERSION:
        _fail(
            f"{PLUGIN_NAME} {__version__} is verified for Agent-Workflow {AW_VERSION}; "
            f"host reports {context.host_version}"
        )
    try:
        if args.spec_command == "compatibility":
            return agent_workflow_compatibility()
        if args.spec_command == "assess":
            return assess(_load_json(args.path), args.mode)
        if args.spec_command == "analyze":
            spec = _load_json(args.spec) if args.spec else None
            return analyze_repository(args.repository, spec, args.mode)
        if args.spec_command == "finalize":
            document = finalize_candidate(_load_json(args.path), args.mode)
            _write_json(args.output, document)
            return {
                "status": "finalized",
                "spec_id": document["id"],
                "snapshot_id": document["snapshot"]["id"],
                "output": str(Path(args.output)),
            }
        if args.spec_command == "compile":
            document = _load_json(args.path)
            analysis = _load_json(args.repository_analysis) if args.repository_analysis else None
            files = compile_agent_workflow_target(
                document,
                repository_analysis=analysis,
                repository_root=args.repository_root,
            )
            output = write_agent_workflow_target(args.output, files)
            return {
                "status": "compiled",
                "spec_id": document["id"],
                "output": str(output),
                "files": sorted(files),
            }
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        _fail(str(exc))
    _fail(f"unsupported plugin command: {getattr(args, 'spec_command', None)!r}")


def plugin():
    from agent_workflow.plugin_api import PluginCommand, PluginDescriptor

    return PluginDescriptor(
        name=PLUGIN_NAME,
        version=__version__,
        commands=(
            PluginCommand(
                name="spec",
                summary="author and compile SpecGen implementation specifications",
                configure=configure,
                execute=execute,
            ),
        ),
        resources=(
            "specgen://contracts",
            "specgen://modes",
            "specgen://agent-workflow-compatibility",
        ),
        metadata={
            "agent_workflow_version": AW_VERSION,
            "canonical_spec": "specgen/spec/v1alpha2",
        },
    )
