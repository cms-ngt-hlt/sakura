#!/bin/bash
# Make sure the local proxy file PROXY (relative to this directory) holds valid
# CMS VOMS credentials. The local copy is reused while it is still valid for at
# least PROXY_MIN_VALID; otherwise a new proxy is created with voms-proxy-init
# and copied here. The proxy in /tmp is never trusted on its own, since a node
# may hold a stale one from an earlier session.
#
# Usage: bash ensure_proxy.sh [pipeline.cfg]
set -euo pipefail

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
CFG="${1:-$HERE/pipeline.cfg}"

# shellcheck source=pipeline.cfg
source "$CFG"

[[ -n "${PROXY:-}" ]] || { echo "ERROR: PROXY is empty in $CFG" >&2; exit 1; }
PROXY_MIN_VALID="${PROXY_MIN_VALID:-24:00}"
PROXY_VALID="${PROXY_VALID:-168:00}"
LOCAL_PROXY="$HERE/$PROXY"

for tool in voms-proxy-info voms-proxy-init; do
  command -v "$tool" >/dev/null || { echo "ERROR: $tool is not available" >&2; exit 1; }
done

proxy_ok() {
  [[ -r "$1" ]] &&
    voms-proxy-info -file "$1" -exists -valid "$PROXY_MIN_VALID" -acexists cms >/dev/null 2>&1
}

if proxy_ok "$LOCAL_PROXY"; then
  echo "Using local proxy $LOCAL_PROXY ($(voms-proxy-info -file "$LOCAL_PROXY" -timeleft) s left)"
  exit 0
fi

if [[ -e "$LOCAL_PROXY" ]]; then
  echo "Local proxy $LOCAL_PROXY is invalid, lacks the cms VO, or expires within $PROXY_MIN_VALID; renewing it."
else
  echo "No local proxy at $LOCAL_PROXY; creating one."
fi

voms-proxy-init --voms cms -rfc --valid "$PROXY_VALID" ||
  { echo "ERROR: voms-proxy-init failed" >&2; exit 1; }
NEW_PROXY=$(voms-proxy-info -path) ||
  { echo "ERROR: cannot locate the new proxy" >&2; exit 1; }

if [[ ! "$NEW_PROXY" -ef "$LOCAL_PROXY" ]]; then
  cp "$NEW_PROXY" "$LOCAL_PROXY"
  chmod 600 "$LOCAL_PROXY"
fi

proxy_ok "$LOCAL_PROXY" ||
  { echo "ERROR: $LOCAL_PROXY is still not valid for $PROXY_MIN_VALID after renewal" >&2; exit 1; }
echo "Copied new proxy to $LOCAL_PROXY ($(voms-proxy-info -file "$LOCAL_PROXY" -timeleft) s left)"
