---
name: wordpress-evergreen-ops
description: Automates trend-driven evergreen content retrofitting, bidirectional sync, SEO enhancement, publishing, and traffic analytics feedback for icsteve.com.
version: "1.2.0"
author: Steve (icsteve.com)
tags: [wordpress, seo, evergreen-content, newsjacking, analytics, bidirectional-sync]
dependencies:
  runtime:
    - python3 (>= 3.8, standard library only, zero pip dependencies)
    - bash / zsh
  credentials:
    - path: /Users/xoit/Documents/icsteve-wordpress/.env
      required_vars: [WP_SITE_URL, WP_USERNAME, WP_APP_PASSWORD]
  skills_and_capabilities:
    - capability: wordpress-publishing
      description: Capability to read and publish posts to WordPress via REST API.
      fallback: Run bundled python script `scripts/content_ops.py` or execute curl commands.
    - capability: web-trend-radar
      description: Access to live trending searches and news (Google Trends, Twitter/X, HN, Weibo).
      fallback: User provides recent topic keywords directly in prompt.
    - capability: obsidian-filesystem-access
      description: Read and write access to local vault path `/Users/xoit/Documents/SteveNote`.
      fallback: Agent outputs updated Markdown content directly in chat for manual saving.
    - capability: traffic-analytics
      description: Access to WordPress Independent Analytics REST API or Google Search Console API.
      fallback: Manual review via WordPress Admin Dashboard Analytics tab.
---

# WordPress Evergreen Content Retrofit & Analytics Ops (Skill)

A self-contained, robust agent skill for discovering real-world trends, syncing and retrofitting published articles on `icsteve.com`, performing SEO enhancement, publishing updates, and closing the loop with traffic analytics.

---

## 🚨 ABSOLUTE HARD RULES & EDITORIAL INTEGRITY

1. **ZERO NEW POST CREATION:** Under NO circumstances may the agent create a new WordPress post. Calling `POST /wp-json/wp/v2/posts` without a specific post ID is strictly prohibited.
2. **STRICTLY IN-PLACE UPDATE:** All modifications MUST target existing published posts via `POST /wp-json/wp/v2/posts/{id}` using the verified `postId`.
3. **PRESERVE ORIGINAL ATTRIBUTES:** Keep the original publication date (`date`), author, category, and canonical permalink slug 100% unchanged. Only inject the callout card, append relevant SEO tags, and update the title suffix.
4. **BILINGUAL SYMMETRY:** Whenever an article is updated, BOTH Chinese and English editions MUST be updated together to maintain parity.
5. **OBSIDIAN BIDIRECTIONAL SYNC:** Every update pushed to WordPress MUST be synchronized back to the corresponding local Markdown file in `/Users/xoit/Documents/SteveNote/MyWork/Voice/` preserving frontmatter.
6. **FULL TREND RADAR PRINTOUT (破除信息茧房):** The agent MUST print out ALL identified external trends from the radar (background, facts, and significance) directly to the user as an informational guide and horizon-scanning tool.
7. **READER-FACING UPDATE TRANSPARENCY (读者更新透明度规范):**
   - Readers MUST be clearly informed of what parts are newly added.
   - The injected update block MUST clearly structure and label:
     * **📌 更新提示与时间戳 (Update Notice & Timestamp):** e.g., "2026/09 动态追踪与增量手记"
     * **🌐 新增时事背景 (New Context):** The external event, data point, or trend triggering this update.
     * **💡 新的感悟与思考 (New Insights & Takeaways):** The author's latest reflection or evolved understanding.
     * **🔚 原文起始分界线 (Boundary Demarcation):** An unmistakable visual separator (e.g. `--- 以下为初版正文 / Original Post Continues Below ---`) so readers can clearly distinguish between fresh additions and original writing.

---

## 1. Quick Start / Agent Kickoff

When an AI agent (Claude, Cursor, Copilot, Gemini) loads this skill, execute the following 5 phases in order:

```
[Phase 0: Sync] -> [Phase 1: Radar & Full Printout] -> [Phase 2: Fit Analysis] -> [Phase 3: In-Place Update & Sync] -> [Phase 4: Feedback]
```

### Kickoff Command
```bash
# 1. Verify credentials and sync online & local baselines
python3 scripts/content_ops.py sync

# 2. If online has newer edits, pull into local Obsidian
python3 scripts/content_ops.py sync --pull
```

---

## 2. Dependencies & Fallback Matrix

Before running, check the agent's environment against the dependency matrix. If any native capability is missing, apply the corresponding fallback:

| Dependency / Capability | Ideal Native Tool | Fallback Mechanism (Zero-Tooling Safe) |
|---|---|---|
| **WordPress Publishing** | Specialized WordPress Agent / MCP | Run bundled script: `python3 scripts/content_ops.py update <post_id>` or direct `curl` |
| **Bidirectional Sync** | Automated Background Sync | Run: `python3 scripts/content_ops.py sync --pull` |
| **Trend Ingestion** | Live Search / Browser / News APIs | User provides top news keywords, or agent uses latest training cutoff events |
| **Local File Access** | Local Filesystem MCP / View / Write | Output formatted Markdown blocks in chat; user copies to Obsidian |
| **Traffic Analytics** | GSC API / GA4 Data API | Query WordPress plugin endpoint `GET /wp-json/independent-analytics/v1/pages` |

---

## 3. Core Workflow Phases

### Phase 0: Bidirectional Sync & Baseline Merge (Critical)
*Never modify on an out-of-sync baseline!*
1. Fetch remote post data (`GET /wp-json/wp/v2/posts/{id}?context=edit`).
2. Compare remote `modified_gmt` with local Markdown `mtime`:
   - **Remote Newer:** Pull remote changes to local Obsidian Markdown file.
   - **Local Newer:** Local draft is the baseline to be pushed later.
   - **Both Modified:** Diff & merge changes. Retain local draft sections and absorb remote formatting/typo fixes.

### Phase 1: Dual-Layer Trend Radar & Full Printout (破除信息茧房)
- **Layer 1 (Mass Public & Culture):** Zero constraints. Monitor top-of-funnel public traffic: 2026 Midterm elections, macroeconomic shifts, utility bills/energy costs, sports, pop culture, and viral social phenomena.
- **Layer 2 (Deep Tech & Specialist):** Monitor Hacker News, GitHub Trending, semiconductor packaging, AI systems, chiplet substrates, CPO, and grid infrastructure.
- **Informational Printout:** Print out ALL scanned trends with background facts, relevance, and societal/technological significance for the user's strategic reading.

### Phase 2: Three-Tier Fit Analysis & Deduplication
1. **Deduplication Check:** Check if the target post already covers the entity in depth. If so, **SKIP** or pivot to net-new developments.
2. **T1: High Fit (>= 80/100) -> Immediate Evergreen Retrofit:** Candidates for immediate in-place update on both Chinese and English posts.
3. **T2: Medium Fit (30-79/100) -> Crossover Retrofit:** Candidates for cross-domain perspective callouts or follow-up notes on both Chinese and English posts.
4. **T3: Low Fit (1-29/100) -> Topic Seed Vault:** Save to `MyWork/Voice/topic-and-idea-seed-vault.md` for future topic incubation. Never discard.
5. **SEO Enhancement:** Inject relevant tags (`/wp-json/wp/v2/tags`), update Title suffix, and refine Meta Description without altering permalinks.

### Phase 3: Publishing to icsteve.com (STRICT IN-PLACE UPDATE ONLY)
- **HARD RULE:** Target existing published posts via `POST /wp-json/wp/v2/posts/{id}`. **NEVER** create a new post.
- **Preserve Original Attributes:** Keep original publication date (`date`), author, category, and URL slug 100% unchanged. Only inject the transparent callout card, append new tags, and add title suffix.
- **Transparency Structure:** Must label New Context, New Insight, and Demarcate Original Text.
- Verify `post_modified_gmt` refreshed (triggers Google QDF freshness signal).
- Update BOTH Chinese and English paired posts to maintain bilingual symmetry.
- Sync updated content back to the local Obsidian Markdown files.
- **Safety Rule:** Strictly do not upload local private photos; use public copyright-free Unsplash images only.

### Phase 4: Analytics Feedback Loop
1. Query traffic endpoints (`python3 scripts/content_ops.py stats --days 30`).
2. Compare 14-day pre-update vs 14-day post-update metrics (Impressions, Clicks, Pageviews).
3. Record findings to refine future keyword targeting.

---

## 4. Bundled Resources

- `scripts/content_ops.py`: Standalone Python CLI for sync, list, update, and analytics.
- `references/dependencies-and-fallbacks.md`: Full dependency breakdown and zero-dependency curl recipes.
- `references/operational-guidelines.md`: The complete master SOP and matching criteria.
- `references/prompt-templates.md`: Copy-paste prompt templates for initiating work across different AI agents.
- `assets/env.example`: Configuration template for WordPress REST API credentials.
- `assets/callout-template.html`: HTML template for the reality check callout box.
