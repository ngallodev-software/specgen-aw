#!/usr/bin/env python3
"""Build a self-describing SpecGen release archive from explicit inputs."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import shutil
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--version", required=True)
    parser.add_argument("--commit", default="unknown")
    args = parser.parse_args()
    dist, output = args.dist.resolve(), args.output.resolve()
    artifacts = sorted(p for p in dist.iterdir() if p.is_file() and p.name.startswith(f"specgen-{args.version}") and p.suffix in {".whl", ".gz"})
    if not artifacts:
        raise SystemExit("release archive failed: no wheel or sdist in dist")
    staging = output.parent / f"specgen-{args.version}-release"
    if staging.exists():
        raise SystemExit(f"release archive failed: staging directory exists: {staging}")
    staging.mkdir(parents=True)
    try:
        manifest = {"application": "specgen", "version": args.version, "commit": args.commit, "build_timestamp": None, "files": {}}
        artifact_dir = staging / "artifacts"
        artifact_dir.mkdir()
        for source in artifacts:
            target = artifact_dir / source.name
            shutil.copyfile(source, target)
        for relative in ("compat", "schemas", "docs", "skills", "README.md", "README.html", "LICENSE", "CHANGELOG.md", "VERSION", "pyproject.toml"):
            source, target = ROOT / relative, staging / relative
            if source.is_dir():
                shutil.copytree(source, target)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
        for path in sorted(p for p in staging.rglob("*") if p.is_file()):
            manifest["files"][path.relative_to(staging).as_posix()] = digest(path)
        (staging / "release-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (staging / "SHA256SUMS").write_text("\n".join(f"{value}  {name}" for name, value in sorted(manifest["files"].items())) + "\n", encoding="utf-8")
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as archive:
                for path in sorted(staging.rglob("*")):
                    info = archive.gettarinfo(path, arcname=path.relative_to(output.parent))
                    info.mtime = 0
                    if path.is_file():
                        with path.open("rb") as handle:
                            archive.addfile(info, handle)
                    else:
                        archive.addfile(info)
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    print(f"release archive: {output} ({len(manifest['files'])} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
