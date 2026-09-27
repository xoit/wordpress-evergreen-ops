# 🔄 WordPress Evergreen Content Retrofit & Analytics Ops

> **An autonomous, production-tested AI Agent Skill for revitalizing published articles on WordPress and Obsidian.**  
> Built for the post-spam AI era: zero disposable new posts, strictly in-place updates, real-world trend jacking, and full reader transparency.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Runtime: Python 3.8+](https://img.shields.io/badge/Python-3.8%2B%20(Zero--Pip)-green.svg)](#dependencies)
[![Local-First: Obsidian](https://img.shields.io/badge/Vault-Obsidian%20Compatible-purple.svg)](#architecture)
[![Integration: WordPress REST API](https://img.shields.io/badge/CMS-WordPress%20REST-orange.svg)](#architecture)

---

## 💡 The Core Problem: Why "More Posts" Is Killing Blogs in 2026

In the age of generative AI, the internet has been flooded with disposable, one-shot articles that decay into digital ghost towns within weeks. Search engines (Google's Core Updates & QDF algorithms) and AI engines (Perplexity, ChatGPT, Gemini Search) increasingly penalize generic content churn and heavily favor **living, verified, continuously updated primary sources**.

Most content creators and engineers make a fatal mistake: **they write a new post for every new thought, leaving their existing high-ranking evergreen articles to rot.**

`wordpress-evergreen-ops` automates the reverse philosophy: **Continuous In-Place Retrofitting.** It scans real-world trends, identifies matching existing assets, injects structured reality checks and transparent insights, refreshes SEO timestamps, and syncs everything bidirectionally back to your local Obsidian vault.

---

## ⚡ Key Capabilities

### 1. 🚨 Zero New Post Creation (Strict In-Place Update)
- **Hard Red Line:** Strictly calls `POST /wp-json/wp/v2/posts/{id}`. Never pollutes your sitemap or creates redundant slug URLs.
- **Preserved Identity:** Keeps original publication dates, authors, categories, and canonical permalinks 100% intact.
- **Freshness Signals:** Updates `modified_gmt` to alert search engines and indexers of genuine, net-new technical or cultural updates (Google QDF).

### 2. 📡 Dual-Layer Trend Radar (Anti-Echo-Chamber)
- **Layer 1 (Mass Public & Culture):** Zero-constraint scanning of high-velocity top-of-funnel topics (e.g. U.S. Midterms, pop culture, consumer retail phenomena, major sports).
- **Layer 2 (Deep Tech & Engineering):** Specialized intelligence across AI agent architectures, context drift, semiconductor packaging (Glass Substrates, ABF warpage), and datacenter power grids.
- **Three-Tier Fit Scoring:** Automatically routes trends into High Fit (T1, immediate retrofit), Medium Fit (T2, cross-domain notes), or Low Fit (T3, permanently preserved in `topic-and-idea-seed-vault.md` to break information bubbles).

### 3. 📌 Reader-Facing Update Transparency
Every modified article clearly presents:
- 📌 **Update Notice & Timestamp**
- 🌐 **New Real-World Context** (What recent event triggered this revisit)
- 💡 **New Reflections & Evolved Insights** (The author's fresh takeaways after time has elapsed)
- 🔚 **Original Post Boundary** (`👇 Original Post Begins Below`)

### 4. 🌐 Bilingual Parity & Obsidian Local-First Sync
- Seamlessly pairs translated posts via Polylang REST endpoints.
- Synchronizes updated content and YAML frontmatter (`postId`, `modified_gmt`, new SEO tags) back to local `.md` notes.

---

## 🏗️ Architecture & Workflow

```
                                ┌─────────────────────────┐
                                │   Phase 1: Trend Radar  │
                                │ (Mass Culture + Tech)   │
                                └────────────┬────────────┘
                                             │
                                             ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│  Phase 0: Baseline Sync │ ──> │ Phase 2: Fit Analysis   │
│ (Obsidian <-> WordPress)│     │ & Deduplication         │
└─────────────────────────┘     └────────────┬────────────┘
                                             │
                                             ▼
                                ┌─────────────────────────┐
                                │ Phase 3: In-Place Update│
                                │ (Transparent Callout)   │
                                └────────────┬────────────┘
                                             │
                                             ▼
                                ┌─────────────────────────┐
                                │   Phase 4: Analytics    │
                                │ (Pre/Post Trajectory)   │
                                └─────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Installation
Clone this repository into your AI Agent's skill folder or Obsidian scripts directory:

```bash
git clone https://github.com/xoit/wordpress-evergreen-ops.git
cd wordpress-evergreen-ops
```

### 2. Configuration
Copy the configuration template and populate your WordPress credentials:

```bash
cp assets/env.example .env
```

Edit `.env`:
```ini
WP_SITE_URL=https://your-domain.com
WP_USERNAME=your_username
WP_APP_PASSWORD="your-24-char-application-password"
```

> **Security Note:** The `.env` file is permanently ignored by `.gitignore`. No credentials will ever be tracked or pushed to Git.

### 3. Standalone CLI Usage (Zero External Dependencies)
All operations use Python's standard library (`urllib`, `json`, `base64`, `os`). Zero `pip install` required.

```bash
# Bi-directional sync check between local Obsidian notes and WordPress
python3 scripts/content_ops.py sync

# If remote WordPress has newer edits, pull into local Markdown files
python3 scripts/content_ops.py sync --pull

# List all published posts, slugs, and modified dates
python3 scripts/content_ops.py list

# Query traffic analytics trajectory
python3 scripts/content_ops.py stats --days 30
```

---

## 🤖 Using with AI Agents (Claude, Cursor, Copilot, Gemini)

When working with an autonomous coding agent, simply paste this kickoff prompt:

```text
Please read the skill definition at:
skills/wordpress-evergreen-ops/SKILL.md

Execute the workflow:
1. Verify sync status between my WordPress site and local Obsidian notes using content_ops.py.
2. Run the dual-layer trend radar across mass culture and deep tech.
3. Calculate fit against my published posts, print the radar findings, and show proposed in-place update blocks with full reader transparency.
4. Wait for my confirmation before updating posts in-place.
```

---

## 📂 Project Structure

```text
wordpress-evergreen-ops/
├── SKILL.md                              # Complete agent master instructions & rules
├── README.md                             # Documentation & quick start guide
├── .gitignore                            # Secrets & local artifacts exclusion
├── scripts/
│   └── content_ops.py                    # Standalone zero-pip Python CLI
├── references/
│   ├── dependencies-and-fallbacks.md     # Graceful degradation matrix & curl recipes
│   ├── operational-guidelines.md         # QDF algorithm & reconciliation logic
│   └── prompt-templates.md               # Ready-to-use prompt templates for agents
└── assets/
    ├── callout-template.html             # Transparent update block HTML template
    └── env.example                       # Sanitized credentials template
```

---

## 📄 License

MIT License. Designed and maintained by [Steve](https://www.icsteve.com). Contributions and feedback are welcome!
