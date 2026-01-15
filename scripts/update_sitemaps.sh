#!/usr/bin/env bash
set -euo pipefail

python3 scripts/fetch_sitemaps.py

# 可选：简单 sanity check（文件非空）
test -s data/sitemaps/en.json
