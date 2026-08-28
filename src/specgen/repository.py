from __future__ import annotations

import hashlib
import json
import subprocess
import tomllib
from pathlib import Path
from typing import Any, Iterable

from .canonical import snapshot_digest
from .contracts import repo_root
from .validate import validate

_IGNORED_DIRS = {".git", ".hg", ".svn", ".venv", "venv", "node_modules", "dist", "build", "target", "__pycache__", ".dev"}
_DOC_NAMES = {"readme.md", "architecture.md", "contributing.md", "agents.md", "claude.md"}
_CONFIG_NAMES = {"pyproject.toml", "package.json", "dockerfile", "docker-compose.yml", "docker-compose.yaml"}


def _sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _run_git(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def _files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in _IGNORED_DIRS for part in relative.parts):
            continue
        yield path


def repository_baseline(root: str | Path) -> dict[str, Any]:
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError(f"repository path is not a directory: {root}")
    revision = _run_git(root, "rev-parse", "HEAD")
    if revision:
        dirty = bool(_run_git(root, "status", "--porcelain"))
        return {"kind": "git", "revision": revision, "dirty": dirty}

    digest = hashlib.sha256()
    for path in _files(root):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(bytes.fromhex(_sha256(path).split(":", 1)[1]))
    return {"kind": "directory", "revision": "sha256:" + digest.hexdigest(), "dirty": False}


def _artifact_kind(path: Path) -> tuple[str, str] | None:
    name = path.name.lower()
    suffix = path.suffix.lower()
    if name in {"openapi.json", "openapi.yaml", "openapi.yml", "swagger.json", "swagger.yaml", "swagger.yml"}:
        return "interface", "openapi"
    if suffix == ".proto":
        return "interface", "protobuf"
    if suffix in {".graphql", ".gql"}:
        return "interface", "graphql"
    if name.endswith(".schema.json"):
        return "data_contract", "json-schema"
    if name in _CONFIG_NAMES:
        return "config", name
    if name in _DOC_NAMES or path.parts[-2:-1] == ("docs",):
        return "documentation", "documentation"
    return None


def _declared_interfaces(path: Path) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    try:
        if path.name == "pyproject.toml":
            data = tomllib.loads(path.read_text(encoding="utf-8"))
            scripts = data.get("project", {}).get("scripts", {})
            if isinstance(scripts, dict):
                for name in sorted(scripts):
                    items.append({"kind": "python-console-script", "name": name})
        elif path.name == "package.json":
            data = json.loads(path.read_text(encoding="utf-8"))
            bins = data.get("bin", {})
            if isinstance(bins, str):
                items.append({"kind": "node-bin", "name": data.get("name", path.parent.name)})
            elif isinstance(bins, dict):
                for name in sorted(bins):
                    items.append({"kind": "node-bin", "name": name})
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, tomllib.TOMLDecodeError):
        return []
    return items


def _spec_paths(spec: dict[str, Any]) -> set[str]:
    paths: set[str] = set()
    for source in spec.get("provenance", {}).get("sources", []):
        if source.get("kind") == "repository" and isinstance(source.get("locator"), str):
            locator = source["locator"].strip()
            if locator and "://" not in locator:
                paths.add(locator.replace("\\", "/").lstrip("./"))
    for field in ("interfaces", "data_contracts"):
        for item in spec.get(field, []):
            value = item.get("path")
            if isinstance(value, str) and value.strip():
                paths.add(value.replace("\\", "/").lstrip("./"))
    return paths


def _agent_workflow_context() -> dict[str, Any]:
    project_root = repo_root()
    compatibility = json.loads((project_root / "compat" / "agent-workflow" / "compatibility.json").read_text(encoding="utf-8"))
    config_path = project_root / "dev" / "agent-workflow.toml"
    if not config_path.is_file():
        config_path = project_root / "dev" / "agent-workflow.example.toml"
    config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    source = config.get("source", {})
    expected = source.get("expected_product_version") or compatibility.get("target", {}).get("product_version")
    source_root = source.get("default_root", "../agent-workflow")
    override = __import__("os").environ.get(source.get("env_override", "SPECGEN_AGENT_WORKFLOW_ROOT"))
    live_root = Path(override or source_root)
    if not live_root.is_absolute():
        live_root = (project_root / live_root).resolve()
    observed = None
    version_file = live_root / "VERSION"
    if version_file.is_file():
        observed = version_file.read_text(encoding="utf-8").strip()
    contracts = sorted(
        item.get("schema_id") for item in compatibility.get("contracts", []) if item.get("schema_id")
    )
    return {
        "profile": "agent-workflow",
        "expected_version": expected,
        "observed_version": observed,
        "live_source": str(live_root),
        "version_matches": observed is None or observed == expected,
        "contracts": contracts,
    }


def analyze_repository(root: str | Path, spec: dict[str, Any] | None = None, mode: str = "guided") -> dict[str, Any]:
    root = Path(root).resolve()
    baseline = repository_baseline(root)
    if spec is not None and not validate(spec).valid:
        raise ValueError("repository analysis requires a valid canonical spec")

    evidence: list[dict[str, Any]] = []
    interfaces: list[dict[str, Any]] = []
    contracts: list[dict[str, Any]] = []
    evidence_by_path: dict[str, str] = {}

    candidates: dict[str, tuple[Path, str, str]] = {}
    for path in _files(root):
        classified = _artifact_kind(path)
        relative = path.relative_to(root).as_posix()
        if classified:
            candidates[relative] = (path, classified[0], classified[1])
    if spec is not None:
        for relative in _spec_paths(spec):
            path = root / relative
            if path.is_file() and relative not in candidates:
                candidates[relative] = (path, "source", "spec-reference")

    for index, relative in enumerate(sorted(candidates), start=1):
        path, kind, description = candidates[relative]
        evid = f"EVID-{index:04d}"
        evidence_by_path[relative] = evid
        evidence.append({"id": evid, "kind": kind, "path": relative, "digest": _sha256(path), "description": description})

        if kind == "interface":
            interfaces.append({"id": f"IFACE-{len(interfaces)+1:04d}", "kind": description, "path": relative, "evidence_ref": evid})
        elif kind == "data_contract":
            contracts.append({"id": f"DATA-{len(contracts)+1:04d}", "kind": description, "path": relative, "evidence_ref": evid})

        for declared in _declared_interfaces(path):
            interfaces.append({
                "id": f"IFACE-{len(interfaces)+1:04d}",
                "kind": declared["kind"],
                "name": declared["name"],
                "path": relative,
                "evidence_ref": evid,
            })

    contradictions: list[dict[str, Any]] = []
    if spec is not None:
        for relative in sorted(_spec_paths(spec)):
            if not (root / relative).is_file():
                contradictions.append({
                    "id": f"CONFLICT-{len(contradictions)+1:04d}",
                    "kind": "missing_evidence",
                    "severity": "blocker",
                    "message": f"specification references repository path that does not exist: {relative}",
                    "path": relative,
                })
        discovered_interface_paths = {item["path"] for item in interfaces}
        for item in spec.get("interfaces", []):
            path = item.get("path")
            if item.get("lifecycle", "active") == "active" and isinstance(path, str) and path not in discovered_interface_paths and (root / path).is_file():
                contradictions.append({
                    "id": f"CONFLICT-{len(contradictions)+1:04d}",
                    "kind": "interface_gap",
                    "severity": "warning",
                    "message": f"declared interface {item['id']} points to a file not recognized as a durable interface artifact",
                    "spec_ref": item["id"], "path": path,
                })
        discovered_contract_paths = {item["path"] for item in contracts}
        for item in spec.get("data_contracts", []):
            path = item.get("path")
            if item.get("lifecycle", "active") == "active" and isinstance(path, str) and path not in discovered_contract_paths and (root / path).is_file():
                contradictions.append({
                    "id": f"CONFLICT-{len(contradictions)+1:04d}",
                    "kind": "data_contract_gap",
                    "severity": "warning",
                    "message": f"declared data contract {item['id']} points to a file not recognized as a durable contract artifact",
                    "spec_ref": item["id"], "path": path,
                })

    result: dict[str, Any] = {
        "schema": "specgen/repository-analysis/v1alpha1",
        "repository": {"path": str(root), "name": root.name},
        "baseline": baseline,
        "evidence": evidence,
        "interfaces": interfaces,
        "data_contracts": contracts,
        "contradictions": contradictions,
    }
    if mode == "agent-workflow":
        result["target_context"] = _agent_workflow_context()
    if spec is not None:
        result["spec"] = {
            "id": spec["id"],
            "snapshot_id": spec["snapshot"]["id"],
            "digest": snapshot_digest(spec),
        }
    return result
