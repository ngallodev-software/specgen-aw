#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
BRANCH=$(git -C "$ROOT" symbolic-ref --quiet --short HEAD || true)
[[ "$BRANCH" == "release-tooling" ]] || exit 0

TOKEN=$(git -C "$ROOT" config --local --get specgen.jenkinsToken || true)
if [[ -z "$TOKEN" ]]; then
  echo "missing local Git config: specgen.jenkinsToken" >&2
  exit 1
fi

curl --fail --silent --show-error --max-time 10 \
  -X POST "http://127.0.0.1:8080/job/specgen-aw-local/build?token=${TOKEN}" \
  >/dev/null
echo "Triggered local Jenkins job specgen-aw-local for $BRANCH"
