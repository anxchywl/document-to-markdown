#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
python3.13 -m venv "$root/.venv"
"$root/.venv/bin/python" -m pip install -r "$root/requirements.txt"
echo "ready: put files in $root/sources and run $root/convert.py"
