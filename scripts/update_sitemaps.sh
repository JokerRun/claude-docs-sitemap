#!/usr/bin/env bash
set -euo pipefail

# Step 1: Fetch and parse sitemaps
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

echo "✓ Sitemap generation passed"

# Step 2: Fetch document content
python3 scripts/fetch_content.py

# Sanity check：检查 manifest 是否生成
if [ ! -f data/manifests/docs.en.json ]; then
  echo "✗ Error: docs.en.json manifest not generated" >&2
  exit 1
fi

if [ ! -s data/manifests/docs.en.json ]; then
  echo "✗ Error: docs.en.json manifest is empty" >&2
  exit 1
fi

echo "✓ Content fetch and manifest generation passed"

echo "✓ All steps completed successfully"
