#!/usr/bin/env python3
"""Render the README and its curated documentation index to browsable HTML."""

from __future__ import annotations

import re
import os
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
LINKED = (
    "docs/USAGE.md",
    "docs/BROWNFIELD_AUTHORING.md",
    "docs/ARCHITECTURE.md",
    "docs/ENGINEERING_POLICY.md",
    "docs/VERSIONING.md",
    "docs/DELIVERY_WORKFLOW.md",
    "docs/AGENT_WORKFLOW_INTEGRATION.md",
    "docs/ROADMAP.md",
    "docs/adr/README.md",
    "docs/adr/ADR-0001-canonical-ir-and-projections.md",
    "docs/adr/ADR-0002-agent-workflow-is-a-versioned-target-not-a-dependency.md",
    "docs/adr/ADR-0003-version-machine-contracts-from-inception.md",
    "docs/adr/ADR-0004-significant-decisions-use-adrs.md",
    "docs/adr/ADR-0005-authoring-history-events-snapshots-and-derived-deltas.md",
    "docs/adr/ADR-0006-authoring-modes-and-agent-workflow-profile.md",
    "docs/adr/ADR-0007-brownfield-analysis-is-evidence-first-and-read-only.md",
    "docs/adr/ADR-0008-agent-assisted-brownfield-analysis-is-separate-and-optional.md",
    "docs/research/PRIOR_ART_DEEP_REVIEW_01.md",
)
CSS = """
:root { color-scheme: light dark; --bg:#f6f8fa; --panel:#fff; --ink:#24292f; --muted:#57606a; --accent:#0969da; --line:#d0d7de; }
@media (prefers-color-scheme: dark) { :root { --bg:#0d1117; --panel:#161b22; --ink:#e6edf3; --muted:#8b949e; --accent:#58a6ff; --line:#30363d; } }
* { box-sizing:border-box; } body { margin:0; background:var(--bg); color:var(--ink); font:16px/1.65 system-ui,-apple-system,Segoe UI,sans-serif; }
main { max-width:1100px; margin:0 auto; padding:2rem 1.25rem 4rem; } article { background:var(--panel); border:1px solid var(--line); border-radius:12px; padding:clamp(1.25rem,3vw,3rem); box-shadow:0 4px 18px #00000012; }
h1,h2,h3 { line-height:1.25; margin-top:1.8em; } h1 { margin-top:0; font-size:2.35rem; } h2 { border-bottom:1px solid var(--line); padding-bottom:.35rem; } a { color:var(--accent); } code { padding:.15em .35em; border-radius:5px; background:color-mix(in srgb,var(--muted) 15%,transparent); } pre { overflow:auto; padding:1rem; border-radius:8px; background:#161b22; color:#e6edf3; } table { display:block; overflow:auto; border-collapse:collapse; } th,td { border:1px solid var(--line); padding:.55rem .75rem; text-align:left; } th { background:color-mix(in srgb,var(--accent) 12%,transparent); } blockquote { margin-left:0; padding:.5rem 1rem; border-left:4px solid var(--accent); color:var(--muted); } .mermaid { background:var(--panel); padding:1rem; border:1px solid var(--line); border-radius:8px; overflow:auto; }
nav { margin-bottom:1rem; color:var(--muted); } nav a { margin-right:1rem; }
"""


def html_links(value: str, source: Path) -> str:
    def replace(match: re.Match[str]) -> str:
        label, target = match.group(1), match.group(2)
        if target.startswith(("http:", "https:", "#", "mailto:")):
            return match.group(0)
        path, fragment = (target.split("#", 1) + [""])[:2]
        if path.endswith(".md"):
            path = path[:-3] + ".html"
        return f"[{label}]({path}{('#' + fragment) if fragment else ''})"

    return re.sub(r"\[([^]]+)\]\(([^)]+)\)", replace, value)


def render(source: Path, output: Path, title: str) -> None:
    body = html_links(source.read_text(encoding="utf-8"), source)
    body = re.sub(r"<pre><code class=\"language-mermaid\">(.*?)</code></pre>", r'<div class="mermaid">\1</div>', body, flags=re.S)
    rendered = markdown.markdown(body, extensions=["fenced_code", "tables", "toc", "sane_lists"])
    rendered = re.sub(r"<pre><code class=\"language-mermaid\">(.*?)</code></pre>", r'<div class="mermaid">\1</div>', rendered, flags=re.S)
    readme_href = os.path.relpath(ROOT / "README.html", output.parent).replace(os.sep, "/")
    index_href = os.path.relpath(ROOT / "docs" / "index.html", output.parent).replace(os.sep, "/")
    navigation = f'<nav><a href="{readme_href}">README</a><a href="{index_href}">Documentation index</a></nav>'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(f"<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>{title}</title><style>{CSS}</style></head><body><main>{navigation}<article>{rendered}</article></main><script type=\"module\">import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs'; mermaid.initialize({{startOnLoad:true,theme:'neutral'}});</script></body></html>\n", encoding="utf-8")


def main() -> int:
    render(ROOT / "README.md", ROOT / "README.html", "SpecGen")
    for relative in LINKED:
        source = ROOT / relative
        render(source, source.with_suffix(".html"), source.stem.replace("_", " "))
    index = ROOT / "docs" / "index.html"
    links = "\n".join(f"<li><a href=\"{Path(path).relative_to('docs').with_suffix('.html').as_posix()}\">{Path(path).stem.replace('_', ' ')}</a></li>" for path in LINKED)
    index.write_text(f"<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>SpecGen documentation</title><style>{CSS}</style></head><body><main><nav><a href=\"../README.html\">README</a></nav><article><h1>SpecGen documentation</h1><p>Generated from the repository's authoritative Markdown documentation.</p><ul>{links}</ul></article></main></body></html>\n", encoding="utf-8")
    print(f"rendered README, documentation index, and {len(LINKED)} linked documents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
