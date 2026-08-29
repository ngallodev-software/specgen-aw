#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
DATA_HOME=${XDG_DATA_HOME:-"$HOME/.local/share"}
VENV=${SPECGEN_VENV:-${AGENT_TOOLS_VENV:-"$DATA_HOME/agent-tools/venv"}}
PYTHON=${PYTHON:-python3}
BIN_DIR=${SPECGEN_BIN_DIR:-"$HOME/.local/bin"}
AGENT_WORKFLOW_ROOT=${AGENT_WORKFLOW_SOURCE_ROOT:-}

if [[ -z "$AGENT_WORKFLOW_ROOT" ]]; then
  for candidate in /lump/apps/agent-workflow "$ROOT/../agent-workflow"; do
    if [[ -f "$candidate/VERSION" && -f "$candidate/pyproject.toml" ]]; then
      AGENT_WORKFLOW_ROOT=$(cd "$candidate" && pwd)
      break
    fi
  done
fi

if [[ ! -x "$VENV/bin/python" ]]; then
  "$PYTHON" -m venv "$VENV"
fi

"$VENV/bin/python" -m pip install --disable-pip-version-check --editable "$ROOT"

EXPECTED_AW_VERSION=$(sed -n 's/.*"product_version": "\([^"]*\)".*/\1/p' "$ROOT/compat/agent-workflow/compatibility.json")
if [[ -n "$AGENT_WORKFLOW_ROOT" ]]; then
  ACTUAL_AW_VERSION=$(tr -d '\n' < "$AGENT_WORKFLOW_ROOT/VERSION")
  if [[ "$ACTUAL_AW_VERSION" != "$EXPECTED_AW_VERSION" ]]; then
    echo "Agent-Workflow $ACTUAL_AW_VERSION is incompatible; SpecGen requires $EXPECTED_AW_VERSION" >&2
    exit 1
  fi
  "$VENV/bin/python" -m pip install --disable-pip-version-check --editable "$AGENT_WORKFLOW_ROOT"
  echo "Installed Agent-Workflow $ACTUAL_AW_VERSION into shared $VENV"
elif [[ -x "$VENV/bin/agent-workflow" ]]; then
  INSTALLED_AW_VERSION=$(
    "$VENV/bin/python" -c 'from importlib.metadata import version; print(version("agent-workflow"))' 2>/dev/null || true
  )
  if [[ "$INSTALLED_AW_VERSION" != "$EXPECTED_AW_VERSION" ]]; then
    echo "Agent-Workflow ${INSTALLED_AW_VERSION:-not found} is incompatible; SpecGen requires $EXPECTED_AW_VERSION" >&2
    exit 1
  fi
  echo "Using compatible Agent-Workflow $INSTALLED_AW_VERSION from shared $VENV"
else
  echo "Agent-Workflow not installed; SpecGen target support remains unavailable until version $EXPECTED_AW_VERSION is installed" >&2
fi
"$VENV/bin/python" -m pip check

mkdir -p "$BIN_DIR"
SPECGEN_LINK="$BIN_DIR/specgen"
destination="$SPECGEN_LINK"
if [[ -e "$destination" && ! -L "$destination" ]]; then
  echo "refusing to replace non-symlink path: $destination" >&2
  exit 1
fi
if [[ -L "$destination" ]]; then
  unlink "$destination"
fi
ln -s "$VENV/bin/specgen" "$destination"
if [[ -x "$VENV/bin/agent-workflow" ]]; then
  destination="$BIN_DIR/agent-workflow"
  if [[ -e "$destination" && ! -L "$destination" ]]; then
    echo "refusing to replace non-symlink path: $destination" >&2
    exit 1
  fi
  [[ -L "$destination" ]] && unlink "$destination"
  ln -s "$VENV/bin/agent-workflow" "$destination"
fi

skill_roots=(
  "${SPECGEN_SKILLS_ROOT:-$HOME/.agents/skills}"
  "${CODEX_HOME:-$HOME/.codex}/skills"
  "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills"
  "${PI_HOME:-$HOME/.pi}/agent/skills"
  "${OPENCODE_CONFIG_DIR:-${XDG_CONFIG_HOME:-$HOME/.config}/opencode}/skills"
)
for skill_root in "${skill_roots[@]}"; do
  mkdir -p "$skill_root"
  for skill_dir in "$ROOT"/skills/*; do
    [[ -d "$skill_dir" ]] || continue
    destination="$skill_root/$(basename "$skill_dir")"
    if [[ -e "$destination" && ! -L "$destination" ]]; then
      echo "refusing to replace non-symlink skill path: $destination" >&2
      exit 1
    fi
    [[ -L "$destination" ]] && unlink "$destination"
    ln -s "$skill_dir" "$destination"
  done
done

echo "Installed SpecGen $(tr -d '\n' < "$ROOT/VERSION") into shared $VENV"
echo "Executable: $SPECGEN_LINK"
echo "Skills linked for: ${#skill_roots[@]} harness roots"
