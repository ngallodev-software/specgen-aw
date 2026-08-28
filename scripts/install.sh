#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
VENV=${SPECGEN_VENV:-"$ROOT/.venv"}
PYTHON=${PYTHON:-python3}

if [[ ! -x "$VENV/bin/python" ]]; then
  "$PYTHON" -m venv "$VENV"
fi

"$VENV/bin/python" -m pip install --disable-pip-version-check --editable "$ROOT"
echo "Installed SpecGen $(tr -d '\n' < "$ROOT/VERSION") into $VENV"
