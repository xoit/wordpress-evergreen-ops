#!/usr/bin/env python3
"""
wordpress-evergreen-ops: Standalone CLI
======================================
Automates:
0. Bidirectional sync between WordPress online content and local Obsidian notes (Phase 0)
1. Fetching published posts and metadata (Phase 0)
2. Incremental updating of posts with SEO tags & callout blocks (Phase 3)
3. Fetching traffic metrics (Independent Analytics / GSC / GA4) (Phase 4)
"""

import os
import re
import sys
import json
import base64
import argparse
import urllib.request
import urllib.parse
from datetime import datetime, timezone

# -------------------------------------------------------------
# Configuration & Credentials Ingestion
# Searches standard locations for .env
# -------------------------------------------------------------
env_search_paths = [
    "/Users/xoit/Documents/icsteve-wordpress/.env",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../assets/.env"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
]

wp_url = "https://www.icsteve.com"
wp_user = ""
wp_pass = ""
obsidian_voice_dir = "/Users/xoit/Documents/SteveNote/MyWork/Voice"

for env_path in env_search_paths:
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k == "WP_SITE_URL":
                        wp_url = v
                    elif k == "WP_USERNAME":
                        wp_user = v
                    elif k == "WP_APP_PASSWORD":
                        wp_pass = v
        if wp_user and wp_pass:
            break

auth = base64.b64encode(f"{wp_user}:{wp_pass}".encode()).decode()
headers = {
    "Authorization": f"Basic {auth}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

def api_request(endpoint, method="GET", data=None):
    url = f"{wp_url}/wp-json{endpoint}"
    req_data = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"❌ API Error ({e.code}): {err_msg}", file=sys.stderr)
        raise

# -------------------------------------------------------------
# Phase 0: Bidirectional Sync & Merge
# -------------------------------------------------------------
def parse_frontmatter(content):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not m:
        return {}, content
    yaml_text = m.group(1)
    body = m.group(2)
    meta = {}
    for line in yaml_text.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            meta[k] = v
    return meta, body

def sync_articles(pull_all=False):
    print(f"🔄 Starting bidirectional sync check ({obsidian_voice_dir} <-> {wp_url})...\n")
    if not os.path.exists(obsidian_voice_dir):
        print(f"❌ Cannot find Obsidian voice directory: {obsidian_voice_dir}")
        return

    local_posts = {}
    for fname in os.listdir(obsidian_voice_dir):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(obsidian_voice_dir, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            meta, body = parse_frontmatter(content)
            post_id = meta.get("postId")
            if post_id:
                mtime = os.path.getmtime(fpath)
                local_posts[str(post_id)] = {
                    "filename": fname,
                    "filepath": fpath,
                    "mtime": mtime,
                    "meta": meta,
                    "body": body,
                    "full_content": content
                }
        except Exception:
            continue

    print(f"📁 Detected {len(local_posts)} local notes with postId.\n")
    print(f"{'PostID':<7} | {'Status':<25} | {'Note File'}")
    print("-" * 80)

    for pid, ldata in local_posts.items():
        try:
            remote = api_request(f"/wp/v2/posts/{pid}?context=edit")
            remote_title = remote.get("title", {}).get("raw", "") or remote.get("title", {}).get("rendered", "")
            remote_mod_str = remote.get("modified_gmt", "")
            remote_dt = datetime.strptime(remote_mod_str, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
            local_dt = datetime.fromtimestamp(ldata["mtime"], tz=timezone.utc)

            time_diff_sec = (remote_dt - local_dt).total_seconds()
            
            if time_diff_sec > 300:
                status = "⚠️ Remote Newer (Pull needed)"
                print(f"{pid:<7} | {status:<25} | {ldata['filename']}")
                print(f"        └─ Remote: {remote_mod_str} | Local: {local_dt.strftime('%Y-%m-%d %H:%M:%S')}")
                if pull_all:
                    remote_raw_content = remote.get("content", {}).get("raw", "")
                    new_md = f"""---
profileName: icsteve
postId: "{pid}"
postType: post
categories:
  - {remote.get('categories', [''])[0]}
tags: {json.dumps(remote.get('tags', []))}
title: "{remote_title}"
date: "{remote.get('date', '')[:10]}"
type: wp-post
lang: {remote.get('lang', 'zh')}
wp-status: publish
modified_gmt: "{remote_mod_str}"
---

# {remote_title}

## 正文

{remote_raw_content}
"""
                    with open(ldata["filepath"], "w", encoding="utf-8") as f:
                        f.write(new_md)
                    print(f"        ✅ [Synced to Local] Updated {ldata['filename']}")

            elif time_diff_sec < -300:
                status = "📝 Local Newer (Pending push)"
                print(f"{pid:<7} | {status:<25} | {ldata['filename']}")
                print(f"        └─ Local: {local_dt.strftime('%Y-%m-%d %H:%M:%S')} | Remote: {remote_mod_str}")
            else:
                status = "✅ Synced"
                print(f"{pid:<7} | {status:<25} | {ldata['filename']}")

        except Exception as e:
            print(f"{pid:<7} | ❌ Fetch Error           | {ldata['filename']} ({e})")

# -------------------------------------------------------------
# Phase 0: Asset Ingestion
# -------------------------------------------------------------
def list_posts(per_page=50):
    print(f"📡 Fetching published posts from {wp_url}...")
    endpoint = f"/wp/v2/posts?status=publish&per_page={per_page}&_fields=id,date,modified,slug,title,categories,tags,link"
    posts = api_request(endpoint)
    print(f"✅ Retrieved {len(posts)} published posts:\n")
    print(f"{'ID':<6} | {'Slug':<35} | {'Modified':<20} | {'Title'}")
    print("-" * 90)
    for p in posts:
        pid = p.get("id")
        slug = p.get("slug")[:33]
        mod = p.get("modified", "")[:19]
        title = p.get("title", {}).get("rendered", "")[:40]
        print(f"{pid:<6} | {slug:<35} | {mod:<20} | {title}")
    return posts

# -------------------------------------------------------------
# Phase 3: Tag Management & Incremental Update
# -------------------------------------------------------------
def get_or_create_tag(tag_name):
    query = urllib.parse.quote(tag_name)
    tags = api_request(f"/wp/v2/tags?search={query}")
    for t in tags:
        if t.get("name", "").lower() == tag_name.lower():
            return t.get("id")
    new_tag = api_request("/wp/v2/tags", method="POST", data={"name": tag_name})
    return new_tag.get("id")

def update_post(post_id, new_title=None, callout_html=None, excerpt=None, add_tags=None):
    print(f"📡 Fetching post ID: {post_id}...")
    post = api_request(f"/wp/v2/posts/{post_id}?context=edit")
    
    current_content = post.get("content", {}).get("raw", "") or post.get("content", {}).get("rendered", "")
    current_tags = post.get("tags", [])
    
    payload = {}
    if new_title:
        payload["title"] = new_title
        
    if callout_html:
        payload["content"] = callout_html + "\n\n" + current_content
        
    if excerpt:
        payload["excerpt"] = excerpt
        
    if add_tags:
        for t_name in add_tags:
            tid = get_or_create_tag(t_name)
            if tid not in current_tags:
                current_tags.append(tid)
        payload["tags"] = current_tags

    print(f"🚀 Pushing update to WordPress...")
    res = api_request(f"/wp/v2/posts/{post_id}", method="POST", data=payload)
    print(f"✅ Update successful! Link: {res.get('link')}")
    print(f"🕒 Modified GMT: {res.get('modified_gmt')}")
    return res

# -------------------------------------------------------------
# Phase 4: Analytics
# -------------------------------------------------------------
def fetch_traffic_metrics(days=30):
    print(f"📊 Checking traffic metrics endpoints (Period: Last {days} days)...")
    try:
        ia_data = api_request(f"/independent-analytics/v1/pages?period=last-{days}-days")
        print("✅ Connected to Independent Analytics REST API successfully!")
        return ia_data
    except Exception:
        print("ℹ️ Independent Analytics endpoint not responding.")
        print("💡 Tip: Install the free 'Independent Analytics' plugin in WP Admin to enable direct REST API queries.")
        print("   Or place Google Search Console credentials in /Users/xoit/Documents/icsteve-wordpress/gsc_service_account.json")

def main():
    parser = argparse.ArgumentParser(description="wordpress-evergreen-ops CLI")
    subparsers = parser.add_subparsers(dest="command")
    
    sync_p = subparsers.add_parser("sync", help="Bidirectional sync check")
    sync_p.add_argument("--pull", action="store_true", help="Auto-pull remote changes into local notes")
    
    subparsers.add_parser("list", help="List published posts")
    
    stats_p = subparsers.add_parser("stats", help="Fetch analytics data")
    stats_p.add_argument("--days", type=int, default=30, help="Days to analyze")
    
    args = parser.parse_args()
    if args.command == "sync":
        sync_articles(pull_all=args.pull)
    elif args.command == "list":
        list_posts()
    elif args.command == "stats":
        fetch_traffic_metrics(days=args.days)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
