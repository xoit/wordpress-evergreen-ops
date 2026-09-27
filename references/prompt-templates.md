# Prompt Templates for Other AI Agents

Use these ready-to-run prompt templates when initiating conversations with Claude, Cursor, Copilot, or another Gemini instance.

---

## 1. Full-Cycle Retrofit & Sync Prompt (Default)

```text
Please read the skill instructions at:
/Users/xoit/Documents/SteveNote/MyWork/AI-Agent Tooling/skills/wordpress-evergreen-ops/SKILL.md

Execute the workflow:
1. Phase 0: Run `python3 "/Users/xoit/Documents/SteveNote/MyWork/AI-Agent Tooling/skills/wordpress-evergreen-ops/scripts/content_ops.py" sync` to verify sync status between WordPress and local Obsidian notes. Pull any remote edits if needed.
2. Phase 1: Perform a dual-layer trend scan (mass public topics + deep tech).
3. Phase 2: Calculate fit against my published posts in `SteveNote/MyWork/Voice/`. Deduplicate, draft retrofit callout blocks for high-fit posts, and record low-fit topics to `topic-and-idea-seed-vault.md`.
4. Present the plan to me and wait for my confirmation before publishing.
```

---

## 2. Targeted Retrofit on a Specific Article

```text
Please refer to the skill at:
/Users/xoit/Documents/SteveNote/MyWork/AI-Agent Tooling/skills/wordpress-evergreen-ops/SKILL.md

I want to update my article: [Article Title, e.g. Behind the Gavel] using the trending topic [Topic, e.g. 2026 US Midterms Debate].
1. First sync and verify the latest baseline for this article.
2. Draft a reality check callout block and proposed SEO tags.
3. Show me the diff and wait for my approval to push to icsteve.com.
```

---

## 3. Pure Sync & Maintenance Mode

```text
Please run Phase 0 of the skill at:
/Users/xoit/Documents/SteveNote/MyWork/AI-Agent Tooling/skills/wordpress-evergreen-ops/SKILL.md

Run `python3 "/Users/xoit/Documents/SteveNote/MyWork/AI-Agent Tooling/skills/wordpress-evergreen-ops/scripts/content_ops.py" sync --pull` to reconcile all changes between icsteve.com and my local Obsidian vault.
```

---

## 4. Traffic & Performance Analytics Query

```text
Please refer to Phase 4 of:
/Users/xoit/Documents/SteveNote/MyWork/AI-Agent Tooling/skills/wordpress-evergreen-ops/SKILL.md

Run `python3 "/Users/xoit/Documents/SteveNote/MyWork/AI-Agent Tooling/skills/wordpress-evergreen-ops/scripts/content_ops.py" stats --days 30` to analyze recent traffic trends for my modified posts.
```
