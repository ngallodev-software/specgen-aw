#!/usr/bin/env bash
set -u

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
BRANCH=$(git -C "$ROOT" symbolic-ref --quiet --short HEAD || true)
[[ "$BRANCH" == "release-tooling" ]] || exit 0
REVISION=$(git -C "$ROOT" rev-parse HEAD 2>/dev/null || true)
[[ "$REVISION" =~ ^[0-9a-fA-F]{40}$ ]] || exit 0

TOKEN=$(git -C "$ROOT" config --local --get specgen.jenkinsToken || true)
[[ -n "$TOKEN" ]] || exit 0

AUTH_FILE=${SPECGEN_JENKINS_AUTH_FILE:-"$HOME/.config/osint-suite/jenkins.env"}
if [[ -f "$AUTH_FILE" && ! -L "$AUTH_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$AUTH_FILE"
fi
AUTH_USER=${SPECGEN_JENKINS_USER:-${OSINT_JENKINS_USER:-}}
AUTH_TOKEN=${SPECGEN_JENKINS_TOKEN:-${OSINT_JENKINS_TOKEN:-}}
[[ -n "$AUTH_USER" && -n "$AUTH_TOKEN" ]] || exit 0

JENKINS_URL=${SPECGEN_JENKINS_URL:-http://127.0.0.1:8080}
case "$JENKINS_URL" in
  http://127.0.0.1:*|https://127.0.0.1:*|http://localhost:*|https://localhost:*) ;;
  *) exit 0 ;;
esac

CRUMB=$(curl --silent --show-error --max-time 5 --user "$AUTH_USER:$AUTH_TOKEN" \
  "$JENKINS_URL/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,\":\",//crumb)" 2>/dev/null || true)
[[ "$CRUMB" =~ ^[A-Za-z0-9_.-]+:[^[:space:]]+$ ]] || exit 0

curl --fail --silent --show-error --max-time 10 \
  -X POST \
  --user "$AUTH_USER:$AUTH_TOKEN" \
  --header "$CRUMB" \
  --data-urlencode "SPECGEN_REVISION=$REVISION" \
  "$JENKINS_URL/job/specgen-aw-local/buildWithParameters?token=${TOKEN}" \
  >/dev/null 2>&1 &
exit 0
