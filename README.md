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
| code | https://code.claude.com/docs/en/agent-teams | 2026-02-26 |  |
| code | https://code.claude.com/docs/en/amazon-bedrock | 2026-02-18 |  |
| code | https://code.claude.com/docs/en/analytics | 2026-02-27 |  |
| code | https://code.claude.com/docs/en/authentication | 2026-02-24 |  |
| code | https://code.claude.com/docs/en/best-practices | 2026-02-26 |  |
| code | https://code.claude.com/docs/en/checkpointing | 2026-02-07 |  |
| code | https://code.claude.com/docs/en/chrome | 2026-02-14 |  |
| code | https://code.claude.com/docs/en/claude-code-on-the-web | 2026-02-27 |  |
| code | https://code.claude.com/docs/en/cli-reference | 2026-03-05 |  |
| code | https://code.claude.com/docs/en/common-workflows | 2026-03-05 |  |
| code | https://code.claude.com/docs/en/costs | 2026-02-26 |  |
| code | https://code.claude.com/docs/en/data-usage | 2026-02-27 |  |
| code | https://code.claude.com/docs/en/desktop | 2026-02-26 |  |
| code | https://code.claude.com/docs/en/desktop-quickstart | 2026-02-20 |  |
| code | https://code.claude.com/docs/en/devcontainer | 2026-01-28 |  |
| ... | _(~827 more rows)_ | | |

<!-- tsv_preview_end -->

---

## 📦 Data Outputs

### Sitemap & Index
- **`en.tsv`** — Tab-separated table of all URLs (GitHub-friendly, Excel/Sheets import ready)
- **`en.yaml`** — Complete YAML with all sitemap fields
- **`docs.en.json`** — Manifest: URL → local path + metadata (for navigation & CI)
- **`code.xml`** — Full sitemap from code.claude.com (all languages, archived)
- **`platform.xml`** — Full sitemap from platform.claude.com (all languages, archived)

Sitemaps & manifests: [`data/sitemaps/`](data/sitemaps/) • [`data/manifests/`](data/manifests/)

### Content Mirror
- **`content/claude-docs/<host>/<path>/*.md`** — Full markdown documents with frontmatter
  - Example: `content/claude-docs/platform.claude.com/docs/en/agent-sdk/overview.md`
  - Example: `content/claude-docs/code.claude.com/docs/en/amazon-bedrock.md`
  - Each file includes YAML frontmatter: `source`, `url`, `fetched_at`, `sha256`

Directory structure: [`content/claude-docs/`](content/claude-docs/)

---

## 🔄 Automation Pipeline

Daily workflow at **02:00 UTC** (cron: `0 2 * * *`):

1. **Fetch sitemaps** from code.claude.com & platform.claude.com
2. **Parse & filter** English URLs (code: `/docs/en/`, platform: non-EN exclusion)
3. **Generate indexes**: en.yaml, en.tsv, docs.en.json manifest
4. **Fetch document content**: Download `.md` from each URL with frontmatter
5. **Organize locally**: Mirror directory structure under `content/claude-docs/`
6. **Auto-commit**: Only on data changes (no empty commits)

**Resilience**: 3-retry with exponential backoff for network failures; graceful cache fallback.

**Manual trigger**: `gh workflow run update-sitemaps.yml`

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
