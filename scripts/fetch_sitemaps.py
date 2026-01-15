#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

try:
    import yaml
except ImportError:
    print("✗ PyYAML not found. Installing...", file=sys.stderr)
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pyyaml"])
    import yaml

CODE_SITEMAP_URL = "https://code.claude.com/docs/sitemap.xml"
PLATFORM_SITEMAP_URL = "https://platform.claude.com/sitemap.xml"

# 要求：code.claude.com 采集英文版本 `/docs/en/`
CODE_EN_PATH_MARKER = "/docs/en/"

# platform.claude.com：题目要求"英文版本"
# 实务上可能出现：
# - 默认即英文（无 /en/）
# - 或英文在 /en/ 下
# - 或 query: ?lang=en
# 这里提供"保守排除 + 显式包含"的规则：
NON_EN_LANG_SEGMENTS = ("zh", "ja", "ko", "fr", "de", "es", "pt", "it", "ru")
NON_EN_SEGMENT_RE = re.compile(r"^/(" + "|".join(NON_EN_LANG_SEGMENTS) + r")(/|$)", re.IGNORECASE)


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
                    "Accept": "application/xml,text/xml,*/*",
                },
                method="GET",
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read()
        except Exception as e:
            last_error = e
            if attempt < retries - 1:
                import time
                wait = 2 ** attempt  # exponential backoff: 1, 2, 4 seconds
                print(f"⚠ Attempt {attempt + 1} failed for {url}: {e}. Retrying in {wait}s...", file=sys.stderr)
                time.sleep(wait)
            else:
                print(f"✗ All {retries} attempts failed for {url}", file=sys.stderr)
    raise last_error


def parse_sitemap(xml_bytes: bytes):
    """
    支持标准 sitemap urlset：
      <url><loc>...</loc><lastmod>...</lastmod><priority>...</priority><changefreq>...</changefreq></url>
    注意 namespace：用通配匹配 { * }loc 等。
    保留所有XML中出现的子元素。
    """
    root = ET.fromstring(xml_bytes)
    urls = []
    for url_node in root.findall(".//{*}url"):
        loc = url_node.findtext("{*}loc")
        if not loc:
            continue
        
        # 收集该 <url> 元素的所有子元素
        entry = {}
        for child in url_node:
            # 去掉namespace前缀
            tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
            text = child.text.strip() if child.text else None
            if text:
                entry[tag] = text
        
        urls.append(entry)
    return urls


def is_code_en(url: str) -> bool:
    # 严格按题目要求：必须包含 /docs/en/
    return url.startswith("https://code.claude.com/") and (CODE_EN_PATH_MARKER in url)


def is_platform_en(url: str) -> bool:
    """
    英文判定规则：
    1) 若 path 中第一个路径段是非英文语言 => 排除
    2) 若 query 有 lang=xx 且 xx != en => 排除；若 lang=en => 包含
    3) 若 path 中任何地方包含 /en/ => 包含
    4) 若 path 后半段包含语言代码（如 /zh-TW/）=> 排除
    5) 其他情况默认包含（常见：默认语言即英文）
    
    实例：
    - /docs => EN (默认) ✓
    - /docs/en/... => EN ✓
    - /docs/zh-TW/... => 非EN ✗
    - /de/... => 非EN ✗
    """
    if not url.startswith("https://platform.claude.com/"):
        return False

    parsed = urllib.parse.urlparse(url)
    path = parsed.path or "/"

    # 排除明显的非英文语言路径（语言在path开头）
    if NON_EN_SEGMENT_RE.match(path):
        return False

    qs = urllib.parse.parse_qs(parsed.query or "")
    if "lang" in qs:
        # lang 可能多值，取任意一个
        langs = [v.lower() for v in qs.get("lang", []) if v]
        if any(l == "en" for l in langs):
            return True
        # 指定了 lang 但不是 en，则排除
        return False

    # 显式包含 /en/
    if "/en/" in path.lower() or path.lower().endswith("/en"):
        return True

    # 排除其他语言标记（如 zh-TW, zh-CN, ja-JP, pt-BR, etc）
    # 这些通常出现在path中间如 /docs/zh-TW/...
    # 支持两字母或地区变体如 pt, pt-BR, zh, zh-TW 等
    if re.search(r"/(zh(-[A-Z]{2})?|ja|ko|fr|de|es|pt(-[A-Z]{2})?|it|ru)(?:/|$)", path, re.IGNORECASE):
        return False

    return True


def main(output_dir: str = "data/sitemaps") -> int:
    # 抓取并解析
    code_xml = fetch_bytes(CODE_SITEMAP_URL)
    platform_xml = fetch_bytes(PLATFORM_SITEMAP_URL)

    code_items = parse_sitemap(code_xml)
    platform_items = parse_sitemap(platform_xml)

    os.makedirs(output_dir, exist_ok=True)

    # 存档源XML
    with open(os.path.join(output_dir, "code.xml"), "wb") as f:
        f.write(code_xml)
    with open(os.path.join(output_dir, "platform.xml"), "wb") as f:
        f.write(platform_xml)

    rows = []

    # code：保留所有XML字段
    for it in code_items:
        loc = it.get("loc", "")
        if not is_code_en(loc):
            continue
        entry = {"source": "code"}
        entry.update(it)
        rows.append(entry)

    # platform：保留所有XML字段
    for it in platform_items:
        loc = it.get("loc", "")
        if not is_platform_en(loc):
            continue
        entry = {"source": "platform"}
        entry.update(it)
        rows.append(entry)

    # 稳定排序：避免无意义 diff
    rows.sort(key=lambda r: (r["source"], r.get("loc", "")))

    # 输出YAML
    yaml_path = os.path.join(output_dir, "en.yaml")
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(
            rows,
            f,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            explicit_start=True,
        )

    print(f"✓ Generated {yaml_path} ({len(rows)} URLs)", file=sys.stderr)
    print(f"✓ Archived {os.path.join(output_dir, 'code.xml')} ({len(code_items)} URLs)", file=sys.stderr)
    print(f"✓ Archived {os.path.join(output_dir, 'platform.xml')} ({len(platform_items)} URLs)", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
