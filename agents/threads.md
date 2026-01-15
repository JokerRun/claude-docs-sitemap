# Thread Registry

| Thread ID | Title | Focus | Key Deliverables |
|-----------|-------|-------|------------------|
| T-019bbf66-71ac-76d9-b2eb-63e40c2b473b | 配置 GitHub Actions 日常采集 | Sitemap 采集 | fetch_sitemaps.py, update-sitemaps.yml, YAML/TSV 输出 |
| T-019bbf72-f4a6-7194-a3bc-5800df8cd04b | 实现验证与多格式输出 | 测试 + 文档 | TSV export, README 文档, manifest 框架 |
| T-019bbfa6-ed35-76eb-8802-c79dd996064c | 内容采集 + 目录规范 | 文档下载 | fetch_content.py, docs.en.json manifest, DIRECTORY_STRUCTURE.md |

---

## Implementation Status

| Component | Status | Files |
|-----------|--------|-------|
| Sitemap Fetch | ✓ | `scripts/fetch_sitemaps.py` |
| Content Fetch | ✓ | `scripts/fetch_content.py` |
| Workflow | ✓ | `.github/workflows/update-sitemaps.yml` |
| Data Output | ✓ | `data/sitemaps/`, `data/manifests/`, `content/claude-docs/` |
| Documentation | ✓ | `README.md`, `DIRECTORY_STRUCTURE.md` |
| Dependencies | ✓ | `pyproject.toml` (uv-managed) |

---

## Architecture

- **Source**: Fetch XML sitemaps from code.claude.com, platform.claude.com
- **Filter**: English URLs only (code: `/docs/en/`, platform: non-EN exclusion)
- **Export**: YAML (source of truth), TSV (human-friendly), JSON manifest (machine-friendly)
- **Content**: Download `.md` documents → save with frontmatter → generate manifest
- **Storage**: Git-tracked (sitemaps, manifests, content)
- **Schedule**: Daily 02:00 UTC via GitHub Actions

---

## Next Steps

1. Monitor first GH Actions run (network resilience)
2. Git scaling: repo size monitoring
3. Change detection: ETag caching (future optimization)
