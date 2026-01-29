# GitHub Issue Analyzer with Local Caching + LLM Processing

## Overview
Build a small backend service with **two HTTP endpoints** that can:

1. Fetch and **locally cache GitHub issues** from a repository
2. **Analyze cached issues** using a **natural-language prompt** and an **LLM**

⏳ **Time limit:** 2 days  
🤖 You are encouraged to use AI coding tools (Cursor, Claude Code, ChatGPT, etc.).

---

## Expectations
- The assignment **must be in a working state**
- There will be a **live demo and testing** in the first round
- After completion, submit details here:
  👉 https://forms.gle/u4QtfALtdSgQhoZc6

---

## What You Need to Build

You will build a **server** (any language or framework) that exposes the following endpoints.

---

## 1️⃣ Endpoint: `POST /scan`

### Purpose
Fetch all **open GitHub issues** for a given repository and **cache them locally**.

### Request Format
```json
{
  "repo": "owner/repository-name"
}
```

### Expected Behavior
- Fetch **all open issues** using the GitHub REST API
- Extract and store **at minimum**:
  - `id`
  - `title`
  - `body`
  - `html_url`
  - `created_at`
- Cache issues locally using **one** of the following storage options

### Allowed Storage Options (Choose One)

| Option | Description |
|------|------------|
| In-memory | Fast, simple, clears on server restart |
| JSON file | Easy to inspect, slower for large datasets |
| SQLite | Most durable, slightly more setup |

📌 **Important:** Document your chosen storage option and reasoning in the README.

### Response Format
```json
{
  "repo": "owner/repository-name",
  "issues_fetched": 42,
  "cached_successfully": true
}
```

---

## 2️⃣ Endpoint: `POST /analyze`

### Purpose
Analyze cached issues for a repository using a **natural-language prompt** and an **LLM**.

### Request Format
```json
{
  "repo": "owner/repository-name",
  "prompt": "Find themes across recent issues and recommend what the maintainers should fix first"
}
```

### Expected Behavior
- Retrieve cached issues for the given repository
- Combine:
  - User prompt
  - Cached issues data
- Send the combined context to an **LLM**
- Return a **fully natural-language analysis** (no keyword-only classification)

### Requirements
- Any LLM provider or local model may be used
- Be mindful of **context size** (chunking is allowed)
- Handle edge cases:
  - Repository not scanned yet
  - No issues cached
  - LLM failures or errors

### Response Format
```json
{
  "analysis": "<LLM-generated text here>"
}
```

---

## ❌ Out of Scope
- No frontend or UI required
- Backend-only implementation

---

## 📦 Deliverables

Submit via:  
👉 https://forms.gle/u4QtfALtdSgQhoZc6

Your submission must include a **public GitHub repository** containing:

### 1. Source Code
- Fully working server
- Both endpoints implemented

### 2. README.md
Include:
- How to run the server
- Why you chose your local storage option

### 3. Prompt History (Add to README)
Provide a list of prompts used during development, including:
- Prompts sent to AI coding tools
- Prompts used to design architecture or fix bugs
- Prompts used to construct the final LLM request in `/analyze`

_(They don’t need to be perfect—this is to understand your workflow.)_

---

✅ **Goal:** Demonstrate backend design, API integration, local storage, LLM usage, and real-world problem-solving.
