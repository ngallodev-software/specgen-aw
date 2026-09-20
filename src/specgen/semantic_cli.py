"""CLI helper for explicit SpecGen semantic shadow collection."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .application import load_document
from .semantic import shadow_assessment
from .typesafe_adapter import TypeSafeSemanticDecisionClient
from .validate import validate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="specgen-semantic")
    parser.add_argument("spec", help="canonical SpecGen JSON snapshot")
    parser.add_argument("--output", required=True, help="semantic-assessment sidecar path")
    parser.add_argument("--model", help="optional TypeSafe model override")
    args = parser.parse_args(argv)

    document = load_document(args.spec)
    result = validate(document)
    if not result.valid:
        raise SystemExit("semantic shadow collection requires a valid canonical SpecGen snapshot")
    assessment = shadow_assessment(document, TypeSafeSemanticDecisionClient(model=args.model))
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(assessment, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0
