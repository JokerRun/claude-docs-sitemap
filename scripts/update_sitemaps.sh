#!/usr/bin/env bash
set -euo pipefail

python3 scripts/fetch_sitemaps.py

# Sanity check：检查输出文件是否存在和非空
if [ ! -f data/sitemaps/en.yaml ]; then
  echo "✗ Error: en.yaml not generated" >&2
  exit 1
fi

if [ ! -s data/sitemaps/en.yaml ]; then
  echo "✗ Error: en.yaml is empty" >&2
  exit 1
fi

echo "✓ Sanity check passed: all outputs generated"
