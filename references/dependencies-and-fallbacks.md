# Dependencies, Prerequisites, and Fallback Matrix

This document defines the exact dependency chain required to run the `wordpress-evergreen-ops` workflow, and specifies how an agent must degrade gracefully if a tool, skill, or environment capability is missing.

---

## 1. System & Runtime Dependencies

| Component | Minimum Version | Purpose | Is Mandatory? | Fallback if Missing |
|---|---|---|---|---|
| **Python** | 3.8+ | Running `scripts/content_ops.py` | Highly Recommended | Execute equivalent `curl` commands directly in bash/terminal. |
| **Python Stdlib** | Standard | `urllib`, `json`, `base64`, `os`, `re`, `argparse` | Yes | Zero pip packages needed. Runs out-of-the-box on macOS. |
| **Bash / Zsh** | Any | Command execution | Recommended | Agent performs HTTP requests via its native API calling tools. |

---

## 2. Credentials & Environment (`.env`)

The skill searches for `.env` at:
1. `/Users/xoit/Documents/icsteve-wordpress/.env`
2. `skills/wordpress-evergreen-ops/assets/.env`
3. Current working directory `.env`

### Required Variables:
```ini
WP_SITE_URL=https://www.icsteve.com
WP_USERNAME=***********
WP_APP_PASSWORD="***********"
```

> **How to Generate a WordPress Application Password:**
> 1. Log in to `https://www.icsteve.com/wp-admin/profile.php`.
> 2. Scroll down to **Application Passwords**.
> 3. Enter a name (e.g. `Gemini-Agent`) and click **Add New Application Password**.
> 4. Copy the generated 24-character string with spaces into `.env`.

---

## 3. Skill & Capability Fallback Matrix

### Dependency A: WordPress Publishing & Sync Capability
- **Ideal Scenario:** The agent has a native WordPress tool/MCP or uses `user:wordpress-evergreen-ops`.
- **Fallback 1 (Bundled Script):** Execute the bundled python script:
  ```bash
  python3 "/Users/xoit/Documents/SteveNote/MyWork/AI-Agent Tooling/skills/wordpress-evergreen-ops/scripts/content_ops.py" sync --pull
  ```
- **Fallback 2 (Pure Curl - No Python needed):**
  - **Fetch post:**
    ```bash
    curl -s -u "$WP_USERNAME:$WP_APP_PASSWORD" \
      "https://www.icsteve.com/wp-json/wp/v2/posts/{post_id}?context=edit"
    ```
  - **Update post:**
    ```bash
    curl -X POST -u "$WP_USERNAME:$WP_APP_PASSWORD" \
      -H "Content-Type: application/json" \
      -d '{"content": "<updated_html>", "title": "<new_title>"}' \
      "https://www.icsteve.com/wp-json/wp/v2/posts/{post_id}"
    ```
- **Fallback 3 (Manual Admin Fallback):**
  The agent outputs the updated HTML and new tags in the chat; the user manually copies and pastes it into Gutenberg editor.

---

### Dependency B: Trend Radar / Web Search Capability
- **Ideal Scenario:** Agent has live web search (Google Search, Twitter/X API, Hacker News API).
- **Fallback 1 (User-Assisted Input):**
  If the agent has no web access or network is sandboxed, the agent prompts:
  *"Please paste 2-3 current trending headlines or topics you want to explore today."*
- **Fallback 2 (Topic Seed Vault):**
  Read previously harvested backlog topics from `/Users/xoit/Documents/SteveNote/MyWork/Voice/topic-and-idea-seed-vault.md`.

---

### Dependency C: Local Obsidian Filesystem Access
- **Ideal Scenario:** Agent has read/write permissions to `/Users/xoit/Documents/SteveNote`.
- **Fallback:**
  If the agent is running in a cloud/sandboxed container without Mac filesystem access:
  The agent outputs the exact Markdown content with frontmatter in a code block, specifying:
  *"Save this file to: SteveNote/MyWork/Voice/<filename>.md"*.

---

### Dependency D: Traffic Analytics Access
- **Ideal Scenario:**
  1. WordPress plugin **Independent Analytics** installed on `icsteve.com`.
     - Endpoint: `GET /wp-json/independent-analytics/v1/pages`
     - Uses the same basic auth as WordPress posts.
  2. Or Google Search Console Service Account JSON placed at `/Users/xoit/Documents/icsteve-wordpress/gsc_service_account.json`.
- **Fallback:**
  Agent outputs a checklist of URL slugs and instructions for the user to check in WP Admin -> Analytics tab, and inputs the numbers back into chat.
