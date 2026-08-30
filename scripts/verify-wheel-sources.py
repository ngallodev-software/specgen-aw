#!/usr/bin/env python3
"""Fail if wheel data files differ from the current source tree."""

from __future__ import annotations

import sys
import tomllib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    raise SystemExit(f"wheel source check failed: {message}")


def main() -> int:
    if len(sys.argv) != 2:
        fail("usage: verify-wheel-sources.py WHEEL")
    wheel = Path(sys.argv[1]).resolve()
    if not wheel.is_file():
        fail(f"wheel not found: {wheel}")
    config = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    data_files = config.get("tool", {}).get("setuptools", {}).get("data-files", {})
    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())
        metadata = next((name for name in names if name.endswith(".dist-info/METADATA")), None)
        if metadata is None:
            fail("wheel has no metadata")
        dist_info = metadata.removesuffix("/METADATA")
        data_prefix = dist_info.removesuffix(".dist-info") + ".data/data/"
        expected = set()
        for destination, patterns in data_files.items():
            for pattern in patterns:
                for source in ROOT.glob(pattern):
                    if not source.is_file():
                        continue
                    relative = source.relative_to(ROOT).as_posix()
                    target = data_prefix + destination.rstrip("/") + "/" + source.name
                    expected.add(target)
                    if target not in names:
                        fail(f"missing {relative} as {target}")
                    if archive.read(target) != source.read_bytes():
                        fail(f"stale or altered component: {relative}")
        actual = {name for name in names if name.startswith(data_prefix)}
        if actual != expected:
            fail(f"wheel data-file set differs from source: extra={sorted(actual - expected)}, missing={sorted(expected - actual)}")
        if not expected:
            fail("pyproject.toml declares no data files")
    print(f"wheel source check: {len(expected)} data files match source")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
