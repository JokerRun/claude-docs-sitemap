# Claude Docs Sitemap Dataset

Automated daily English sitemap collection from Claude documentation sources.

> **📊 [View Complete Table →](data/sitemaps/en.tsv)** • **Raw Download**: [en.tsv](https://raw.githubusercontent.com/JokerRun/claude-docs-sitemap/main/data/sitemaps/en.tsv)

---

## Quick Stats

| Metric | Value |
|--------|-------|
| **Total URLs** | 762 (EN only) |
| **code.claude.com** | 48 URLs |
| **platform.claude.com** | 714 URLs |
| **Last Updated** | Daily @ 02:00 UTC |
| **Format** | TSV, YAML, XML |

---

## 📋 Data Preview

<!-- tsv_preview_start -->
| source | loc | lastmod | priority |
|--------|--------|--------|--------|
| code | https://code.claude.com/docs/en/amazon-bedrock | 2025-12-16 |  |
| code | https://code.claude.com/docs/en/analytics | 2025-11-06 |  |
| code | https://code.claude.com/docs/en/checkpointing | 2025-11-06 |  |
| code | https://code.claude.com/docs/en/chrome | 2025-12-19 |  |
| code | https://code.claude.com/docs/en/claude-code-on-the-web | 2026-01-07 |  |
| code | https://code.claude.com/docs/en/cli-reference | 2026-01-10 |  |
| code | https://code.claude.com/docs/en/common-workflows | 2026-01-14 |  |
| code | https://code.claude.com/docs/en/costs | 2025-11-06 |  |
| code | https://code.claude.com/docs/en/data-usage | 2026-01-07 |  |
| code | https://code.claude.com/docs/en/desktop | 2026-01-11 |  |
| code | https://code.claude.com/docs/en/devcontainer | 2025-12-08 |  |
| code | https://code.claude.com/docs/en/discover-plugins | 2026-01-11 |  |
| code | https://code.claude.com/docs/en/github-actions | 2025-12-08 |  |
| code | https://code.claude.com/docs/en/gitlab-ci-cd | 2026-01-12 |  |
| code | https://code.claude.com/docs/en/google-vertex-ai | 2025-12-07 |  |
| ... | _(~747 more rows)_ | | |

<!-- tsv_preview_end -->

---

## 📦 Available Formats

- **`en.tsv`** — Tab-separated table (GitHub-friendly, Excel/Sheets import ready)
- **`en.yaml`** — Complete YAML with all sitemap fields
- **`code.xml`** — Full sitemap from code.claude.com (all languages)
- **`platform.xml`** — Full sitemap from platform.claude.com (all languages)

All files in: [`data/sitemaps/`](data/sitemaps/)

---

## 🔄 Automation

- **Schedule**: Every day at **02:00 UTC** (cron: `0 2 * * *`)
- **Trigger**: Manual: `gh workflow run update-sitemaps.yml`
- **Auto-commit**: Only when data changes (no empty commits)
- **Resilience**: 3-retry with exponential backoff for network failures

---

## 🌍 Language Filter

| Source | Rule | Example |
|--------|------|---------|
| **code** | Must contain `/docs/en/` | ✓ `code.claude.com/docs/en/amazon-bedrock` |
| **platform** | Exclude non-EN paths | ✓ `platform.claude.com/docs/en/models/overview` |
| | | ✗ `platform.claude.com/docs/zh-TW/...` |

---

## 💡 Usage

### Python (Pandas)
```python
import pandas as pd
df = pd.read_csv('data/sitemaps/en.tsv', sep='\t')
df_code = df[df['source'] == 'code']
```

### Excel / Google Sheets
Download [en.tsv](data/sitemaps/en.tsv) → Open directly

### CLI
```bash
curl -s https://raw.githubusercontent.com/JokerRun/claude-docs-sitemap/main/data/sitemaps/en.tsv | head -20
```

---

## 📚 References

- [threads.md](agents/threads.md) — Implementation thread registry
- [GitHub Workflow](https://github.com/JokerRun/claude-docs-sitemap/actions/workflows/update-sitemaps.yml)
- Source: [code.claude.com](https://code.claude.com/docs) | [platform.claude.com](https://platform.claude.com/docs)

---

**Last commit**: Check [git log](https://github.com/JokerRun/claude-docs-sitemap/commits/main) for history
