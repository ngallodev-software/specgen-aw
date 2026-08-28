#!/usr/bin/env python3
"""Validate and materialize SpecGen's development link to Agent-Workflow.

Release compatibility under compat/agent-workflow remains authoritative. This
script creates ignored local symlinks and an observed lock/drift report only.
"""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "dev" / "agent-workflow.toml"
EXAMPLE_CONFIG = ROOT / "dev" / "agent-workflow.example.toml"
COMPAT = ROOT / "compat" / "agent-workflow" / "compatibility.json"
LOCK = ROOT / ".dev" / "agent-workflow" / "lock.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def schema_id(path: Path) -> str | None:
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    sid = d.get("$id")
    if isinstance(sid, str) and sid.startswith("agent-workflow/"):
        return sid
    p = d.get("properties", {}).get("schema", {})
    if isinstance(p, dict):
        return p.get("const") or p.get("default")
    return None


def load():
    config_path = CONFIG if CONFIG.is_file() else EXAMPLE_CONFIG
    with config_path.open("rb") as f:
        cfg = tomllib.load(f)
    return cfg, json.loads(COMPAT.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    cfg, compat = load()
    if cfg.get("schema") != "specgen/dev-source-link/v1alpha1":
        raise SystemExit(f"unsupported dev config schema: {cfg.get('schema')!r}")
    src_cfg = cfg["source"]
    env = src_cfg.get("env_override")
    raw_root = Path(os.environ.get(env, "") or src_cfg["default_root"]).expanduser()
    root = (raw_root if raw_root.is_absolute() else ROOT / raw_root).resolve()
    report = {
        "schema": "specgen/dev-source-lock/v1alpha1",
        "source": str(root),
        "expected_snapshot": src_cfg.get("expected_snapshot"),
        "expected_product_version": src_cfg["expected_product_version"],
        "contracts": [], "references": [], "links": [], "drift": [], "ok": True,
    }
    if not root.is_dir():
        report["ok"] = False
        report["drift"].append({"kind": "missing-source-root", "path": str(root)})
        return emit(report, args.json, 2)

    vp = root / src_cfg["version_file"]
    actual = vp.read_text(encoding="utf-8").strip() if vp.is_file() else None
    report["actual_product_version"] = actual
    if actual != src_cfg["expected_product_version"]:
        report["ok"] = False
        report["drift"].append({"kind": "product-version", "expected": src_cfg["expected_product_version"], "actual": actual})

    expected = {x["schema_id"]: x for x in compat.get("contracts", [])}
    for c in cfg.get("contracts", []):
        p = root / c["path"]
        row = {"schema_id": c["schema_id"], "path": c["path"], "exists": p.is_file()}
        if p.is_file():
            row["sha256"] = sha256(p)
            row["observed_schema_id"] = schema_id(p)
        e = expected.get(c["schema_id"])
        row["expected_sha256"] = e.get("sha256") if e else None
        row["matches_release_fixture"] = bool(e) and row.get("sha256") == e.get("sha256")
        if not row["exists"]:
            report["ok"] = False; report["drift"].append({"kind": "missing-contract", "schema_id": c["schema_id"]})
        elif not e:
            report["ok"] = False; report["drift"].append({"kind": "undeclared-contract", "schema_id": c["schema_id"]})
        elif not row["matches_release_fixture"]:
            report["ok"] = False; report["drift"].append({"kind": "contract-digest", "schema_id": c["schema_id"]})
        report["contracts"].append(row)

    for r in cfg.get("references", []):
        p = root / r["path"]
        row = {"path": r["path"], "role": r["role"], "exists": p.exists(), "sha256": sha256(p) if p.is_file() else None}
        report["references"].append(row)
        if not p.exists():
            report["ok"] = False; report["drift"].append({"kind": "missing-reference", "path": r["path"]})

    if not args.check:
        managed = ROOT / cfg["link"]["root"]
        managed.mkdir(parents=True, exist_ok=True)
        for item in cfg["link"].get("paths", []):
            src = root / item["source"]
            dst = managed / item["target"]
            if not src.exists():
                report["ok"] = False; report["drift"].append({"kind": "missing-link-source", "path": item["source"]}); continue
            try:
                dst.parent.resolve(strict=False).relative_to((ROOT / ".dev").resolve(strict=False))
            except ValueError:
                raise RuntimeError(f"unsafe managed target: {dst}")
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.is_symlink() or dst.exists():
                if dst.is_dir() and not dst.is_symlink(): shutil.rmtree(dst)
                else: dst.unlink()
            dst.symlink_to(src, target_is_directory=src.is_dir())
            report["links"].append({"target": str(dst.relative_to(ROOT)), "source": str(src), "kind": item["kind"]})
        LOCK.parent.mkdir(parents=True, exist_ok=True)
        LOCK.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return emit(report, args.json, 0 if report["ok"] else 1)


def emit(report, as_json, code):
    if as_json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"Agent-Workflow source: {report['source']}")
        print(f"Expected version: {report['expected_product_version']}")
        print(f"Actual version:   {report.get('actual_product_version', 'missing')}")
        print(f"Contracts:        {len(report.get('contracts', []))}")
        print(f"Status:           {'OK' if report.get('ok') else 'DRIFT'}")
        for d in report.get("drift", []): print(f"  - {d['kind']}: {d.get('schema_id') or d.get('path') or d}")
    return code

if __name__ == "__main__":
    raise SystemExit(main())
