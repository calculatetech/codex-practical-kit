#!/usr/bin/env sh
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO=${1:-.}
if [ "$#" -gt 0 ]; then shift; fi
exec python3 "$HERE/kit.py" setup-repo "$REPO" "$@"
