#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import hashlib
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

import yaml


def fetch_bytes(url: str, retries: int = 3) -> bytes:
    """
    Fetch URL with retry logic for transient network failures.
    """
    last_error = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "claude-docs-sitemap-bot/1.0 (+GitHub Actions)",
                    "Accept": "text/markdown,text/plain,*/*",
                },
                method="GET",
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read()
        except Exception as e:
            last_error = e
            if attempt < retries - 1:
                import time
                wait = 2 ** attempt
                print(f"⚠ Attempt {attempt + 1} failed for {url}: {e}. Retrying in {wait}s...", file=sys.stderr)
                time.sleep(wait)
            else:
                print(f"✗ All {retries} attempts failed for {url}", file=sys.stderr)
    raise last_error


def url_to_local_path(url: str, content_base: str) -> str:
    """
    Map URL to local file path.
    
    Note: url should NOT include .md extension (it's added during fetch_bytes call).
    
    Example:
      https://platform.claude.com/docs/en/agent-sdk/overview
      → content/claude-docs/platform.claude.com/docs/en/agent-sdk/overview.md
    """
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc
    path = parsed.path or "/"
    
    # Remove .md suffix if present (from fetch_bytes call)
    if path.endswith(".md"):
        path = path[:-3]
    
    # Normalize path: remove trailing slash for consistency (we'll use .md)
    if path.endswith("/") and path != "/":
        path = path.rstrip("/")
    
    # Build local path: base/host/path + .md
    local_rel = os.path.join("content/claude-docs", host, path.lstrip("/"))
    local_path = os.path.join(content_base, local_rel) + ".md"
    
    return local_path


def compute_sha256(data: bytes) -> str:
    """Compute SHA256 hash of content."""
    return hashlib.sha256(data).hexdigest()


def add_frontmatter(content: bytes, url: str, source: str, fetched_at: str) -> str:
    """
    Add YAML frontmatter to markdown content.
    """
    sha256 = compute_sha256(content)
    text = content.decode("utf-8", errors="replace")
    
    frontmatter = {
        "source": source,
        "url": url,
        "fetched_at": fetched_at,
        "sha256": sha256,
    }
    
    # Build frontmatter block
    fm_lines = ["---"]
    for key, value in frontmatter.items():
        fm_lines.append(f"{key}: {value}")
    fm_lines.append("---")
    
    return "\n".join(fm_lines) + "\n\n" + text


def main(sitemap_path: str = "data/sitemaps/en.yaml", content_base: str = ".") -> int:
    """
    Fetch markdown content from all URLs in sitemap and save locally.
    """
    # Load sitemap
    if not os.path.exists(sitemap_path):
        print(f"✗ Sitemap not found: {sitemap_path}", file=sys.stderr)
        return 1
    
    with open(sitemap_path, "r", encoding="utf-8") as f:
        sitemap_items = yaml.safe_load(f) or []
    
    if not sitemap_items:
        print(f"✗ No items in sitemap: {sitemap_path}", file=sys.stderr)
        return 1
    
    now = datetime.utcnow().isoformat() + "Z"
    manifest = []
    fetched_count = 0
    error_count = 0
    
    for i, item in enumerate(sitemap_items, start=1):
        url = item.get("loc", "")
        if not url:
            continue
        
        source = item.get("source", "unknown")
        
        try:
            # Fetch content
            content = fetch_bytes(url + ".md")
            
            # Determine local path
            local_path = url_to_local_path(url + ".md", content_base)
            local_dir = os.path.dirname(local_path)
            
            # Create directory
            os.makedirs(local_dir, exist_ok=True)
            
            # Add frontmatter and write
            text_with_fm = add_frontmatter(content, url, source, now)
            with open(local_path, "w", encoding="utf-8") as f:
                f.write(text_with_fm)
            
            # Record in manifest
            sha256 = compute_sha256(content)
            manifest.append({
                "source": source,
                "url": url,
                "local_path": os.path.relpath(local_path, content_base),
                "fetched_at": now,
                "sha256": sha256,
            })
            
            fetched_count += 1
            if fetched_count % 50 == 0:
                print(f"⋯ Fetched {fetched_count}/{len(sitemap_items)} documents", file=sys.stderr)
        
        except Exception as e:
            error_count += 1
            print(f"✗ Failed to fetch {url}: {e}", file=sys.stderr)
            continue
    
    # Write manifest
    manifest_dir = os.path.join(content_base, "data/manifests")
    os.makedirs(manifest_dir, exist_ok=True)
    
    manifest_path = os.path.join(manifest_dir, "docs.en.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Fetched {fetched_count}/{len(sitemap_items)} documents", file=sys.stderr)
    print(f"✓ Generated manifest: {manifest_path} ({len(manifest)} entries)", file=sys.stderr)
    if error_count > 0:
        print(f"⚠ {error_count} errors during fetch", file=sys.stderr)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
