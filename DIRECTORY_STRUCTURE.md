# Directory Structure & File Organization

## Overview

This project maintains three complementary data artifacts:

1. **Sitemap indexes** (`data/sitemaps/`) — URLs from upstream sources
2. **Manifests** (`data/manifests/`) — Structured metadata for navigation
3. **Content mirror** (`content/claude-docs/`) — Full markdown documents

---

## Directory Layout

```
claude-docs-sitemap/
├── data/
│   ├── sitemaps/
│   │   ├── en.yaml                    # Master index (762 English URLs)
│   │   ├── en.tsv                     # TSV export (GitHub-friendly table)
│   │   ├── code.xml                   # Archived: full sitemap from code.claude.com
│   │   └── platform.xml               # Archived: full sitemap from platform.claude.com
│   │
│   └── manifests/
│       └── docs.en.json               # Manifest: URL ↔ local_path + metadata
│
├── content/
│   └── claude-docs/                   # Markdown content mirror
│       ├── code.claude.com/
│       │   └── docs/
│       │       └── en/
│       │           ├── amazon-bedrock.md
│       │           ├── analytics.md
│       │           ├── chrome.md
│       │           └── ...
│       │
│       └── platform.claude.com/
│           └── docs/
│               └── en/
│                   ├── agent-sdk/
│                   │   ├── overview.md
│                   │   ├── core-concepts.md
│                   │   └── api.md
│                   ├── models/
│                   │   └── overview.md
│                   └── ...
│
├── scripts/
│   ├── fetch_sitemaps.py              # Fetch & parse XML sitemaps
│   ├── fetch_content.py               # Fetch markdown content + generate manifest
│   ├── update_sitemaps.sh             # Orchestration entrypoint
│   └── update_readme_preview.py       # Generate README preview table
│
├── .github/
│   └── workflows/
│       └── update-sitemaps.yml        # Daily automation (02:00 UTC)
│
├── agents/
│   └── threads.md                     # Implementation thread registry
│
├── README.md                          # Project documentation
├── DIRECTORY_STRUCTURE.md             # This file
└── .gitignore
```

---

## File Mapping Rules

### Sitemap → Content Path Mapping

**URL Structure**:
```
https://{host}/docs/{lang}/{path}/{page}
```

**Local Path**:
```
content/claude-docs/{host}/docs/{lang}/{path}/{page}.md
```

**Examples**:

| Source | URL | Local Path |
|--------|-----|------------|
| code | `https://code.claude.com/docs/en/amazon-bedrock` | `content/claude-docs/code.claude.com/docs/en/amazon-bedrock.md` |
| code | `https://code.claude.com/docs/en/common-workflows` | `content/claude-docs/code.claude.com/docs/en/common-workflows.md` |
| platform | `https://platform.claude.com/docs/en/agent-sdk/overview` | `content/claude-docs/platform.claude.com/docs/en/agent-sdk/overview.md` |
| platform | `https://platform.claude.com/docs/en/models/overview` | `content/claude-docs/platform.claude.com/docs/en/models/overview.md` |

### Normalization Rules

1. **Query strings & fragments**: Removed (not stored in path)
2. **Trailing slashes**: Normalized (e.g., `/docs/en/foo/` → `.../foo.md`, not `.../foo/index.md`)
3. **Path case**: Preserved as-is from URL
4. **Special characters**: Pass-through (URLs don't contain path-unsafe characters)

---

## Manifest Format

**File**: `data/manifests/docs.en.json`

**Structure**: Array of objects

```json
[
  {
    "source": "platform.claude.com",
    "url": "https://platform.claude.com/docs/en/agent-sdk/overview",
    "local_path": "content/claude-docs/platform.claude.com/docs/en/agent-sdk/overview.md",
    "fetched_at": "2026-01-15T02:00:00Z",
    "sha256": "a1b2c3d4e5f6..."
  },
  {
    "source": "code.claude.com",
    "url": "https://code.claude.com/docs/en/amazon-bedrock",
    "local_path": "content/claude-docs/code.claude.com/docs/en/amazon-bedrock.md",
    "fetched_at": "2026-01-15T02:00:00Z",
    "sha256": "f6e5d4c3b2a1..."
  }
]
```

**Use Cases**:
- Fast URL → file lookup (no filesystem scan needed)
- Detect content changes (compare `sha256`)
- Track fetch history (`fetched_at`)
- Source attribution (`source`)

---

## Markdown Document Format

Each `.md` file includes YAML frontmatter for metadata:

```yaml
---
source: platform.claude.com
url: https://platform.claude.com/docs/en/agent-sdk/overview
fetched_at: 2026-01-15T02:00:00Z
sha256: a1b2c3d4e5f6...
---

# Original content from upstream...

## Section 1
...
```

**Frontmatter Fields**:
- `source` — Origin domain (code.claude.com or platform.claude.com)
- `url` — Original URL (without `.md` extension)
- `fetched_at` — ISO 8601 timestamp of fetch
- `sha256` — Content hash (useful for change detection)

---

## Storage Strategy

### Git Storage
- ✅ All `.md` files committed to Git (762 total, ~10–50 MB, manageable)
- ✅ Manifests (`docs.en.json`) tracked in Git
- ✅ Sitemaps (`*.yaml`, `*.xml`) tracked for audit trail
- ✅ Allow incremental updates on daily runs

### Why Git for Content?
1. **Auditability**: Full commit history of doc changes
2. **Diff review**: Easy to see what changed in each run
3. **Rollback**: Revert to previous versions if needed
4. **No external dependencies**: No object store, database, or CDN needed
5. **Scale**: 762 files is well within Git's capabilities

---

## Daily Workflow

1. **Fetch sitemaps** (fetch_sitemaps.py)
   - GET code.claude.com/docs/sitemap.xml
   - GET platform.claude.com/sitemap.xml
   - Parse → filter English URLs → output to `data/sitemaps/en.yaml`

2. **Fetch content** (fetch_content.py)
   - Load URLs from `data/sitemaps/en.yaml`
   - For each URL: GET `{url}.md`
   - Save to local path with frontmatter
   - Generate `data/manifests/docs.en.json`

3. **Update docs** (update_readme_preview.py)
   - Generate preview table for README
   - Update `README.md` (keep content between markers)

4. **Commit & push**
   - Only if changes detected
   - Commit message: `chore(docs): update EN sitemap, manifests, and content (YYYY-MM-DD)`

---

## Design Decisions

### Why "Sorted by domain" instead of "flat structure"?
- **Collision avoidance**: code.claude.com and platform.claude.com may have overlapping paths
- **Clear separation**: Which source contributed this file?
- **Isolation**: Updates to one source don't affect the other
- **Scalability**: Easy to add more sources (e.g., claude.ai docs)

### Why manifest alongside content?
- **Index efficiency**: Rapid URL lookups without filesystem scans
- **Change detection**: SHA256 allows incremental updates
- **Machine-friendly**: Structured format (JSON) for CI/API integration
- **Small footprint**: ~10 KB for 762 entries (vs. 700+ file I/O)

### Why not multiple `index.md` per directory?
- **Unnecessary complexity**: URLs already provide clear paths
- **Maintenance burden**: Who generates the index content?
- **Conflict risk**: What if upstream adds a doc named "index"?
- **Canonical source**: Manifest already provides directory listing

---

## Future Extensions

### If you need full-text search:
1. Parse `.md` files → build inverted index
2. Store in `data/indexes/` (e.g., `.json` or SQLite)
3. Rebuild daily in CI

### If you need rendered HTML:
1. Add pipeline step: `fetch_content.py` → `render_content.py`
2. Output to `content/claude-docs-rendered/`
3. Useful for full-page screenshots, PDF export, or hosting

### If you need multi-language support:
1. Extend `is_platform_en()` to accept language parameter
2. Generate separate manifests: `docs.{lang}.json`
3. Mirror structure: `content/claude-docs/{host}/docs/{lang}/`

---

## Maintenance Checklist

- [ ] Monitor first automated run at 02:00 UTC
- [ ] Verify commit message format in GitHub
- [ ] Check manifest file size (should grow ~1% per day)
- [ ] Set Git LFS for content if repo size exceeds 1 GB
- [ ] Document any upstream URL pattern changes
- [ ] Review error logs for persistent fetch failures
