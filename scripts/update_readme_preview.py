#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-update README.md with TSV preview (top 15 rows).
Run after fetch_sitemaps.py to keep preview current.
"""

import csv
import re
import sys

def generate_preview_table(tsv_path: str, max_rows: int = 15) -> str:
    """Read TSV and generate Markdown table (top N rows)."""
    rows = []
    with open(tsv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for i, row in enumerate(reader):
            if i < max_rows:
                rows.append(row)
            else:
                break
    
    if not rows:
        return ""
    
    header = ['source', 'loc', 'lastmod', 'priority']
    
    # Build markdown table
    md_table = "| " + " | ".join(header) + " |\n"
    md_table += "|" + "|".join(["-" * 8 for _ in header]) + "|\n"
    
    for row in rows:
        # Truncate URL for readability
        loc = row.get('loc', '')
        if len(loc) > 55:
            loc = loc[:52] + "..."
        
        lastmod = row.get('lastmod', '')
        if lastmod:
            lastmod = lastmod[:10]  # Just the date part
        
        cells = [
            row.get('source', ''),
            loc,
            lastmod,
            row.get('priority', '')
        ]
        md_table += "| " + " | ".join(cells) + " |\n"
    
    # Count remaining rows
    total_rows = sum(1 for _ in open(tsv_path, encoding='utf-8'))
    remaining = total_rows - 1 - max_rows  # -1 for header
    
    if remaining > 0:
        md_table += f"| ... | _(~{remaining} more rows)_ | | |\n"
    
    return md_table


def update_readme(readme_path: str, preview_table: str) -> bool:
    """Update README.md with new preview table between markers."""
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern: between <!-- tsv_preview_start --> and <!-- tsv_preview_end -->
    pattern = r'(<!-- tsv_preview_start -->)\n.*?\n(<!-- tsv_preview_end -->)'
    
    replacement = f"\\1\n{preview_table}\n\\2"
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content == content:
        print("⚠ No preview markers found; skipping README update", file=sys.stderr)
        return False
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ Updated README.md preview table", file=sys.stderr)
    return True


def main() -> int:
    tsv_path = "data/sitemaps/en.tsv"
    readme_path = "README.md"
    
    try:
        preview_table = generate_preview_table(tsv_path, max_rows=15)
        if not preview_table:
            print("✗ Failed to generate preview table", file=sys.stderr)
            return 1
        
        update_readme(readme_path, preview_table)
        return 0
    except Exception as e:
        print(f"✗ Error updating README: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
