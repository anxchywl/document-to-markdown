#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$root/bin"
swiftc -O "$root/scripts/ocr-page.swift" -o "$root/bin/ocr-page" -framework Vision -framework ImageIO
echo "built $root/bin/ocr-page"
