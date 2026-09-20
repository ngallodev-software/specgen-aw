"""CLI helper for configured SpecGen semantic shadow collection."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .application import load_document
from .semantic import shadow_assessment
from .semantic_config import configured_semantic_client, load_semantic_config
from .validate import validate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="specgen-semantic")
    parser.add_argument("spec", help="canonical SpecGen JSON snapshot")
    parser.add_argument("--output", required=True, help="semantic-assessment sidecar path")
    parser.add_argument("--config", help="config.toml path; otherwise SPECGEN_CONFIG, ./config.toml, then ~/.config/specgen/config.toml")
    parser.add_argument("--model", help="temporary TypeSafe model override")
    args = parser.parse_args(argv)

    config = load_semantic_config(args.config)
    if args.model is not None:
        from dataclasses import replace
        config = replace(config, model=args.model)
    client = configured_semantic_client(config)
    document = load_document(args.spec)
    result = validate(document)
    if not result.valid:
        raise SystemExit("semantic shadow collection requires a valid canonical SpecGen snapshot")
    assessment = shadow_assessment(document, client)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(assessment, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0
