# 📄 Product Requirements Document (PRD)
## GitHub Issue Analyzer with Local Caching + LLM Processing

---

## 1. Overview

### Product Name
**GitHub Issue Analyzer**

### Objective
Build a backend-only service that:
1. Fetches and locally caches open GitHub issues for a repository
2. Analyzes cached issues using a natural-language prompt powered by an LLM

The system demonstrates backend engineering skills, third-party API integration, local data storage, and practical LLM usage.

### Target Audience
- Engineering hiring panel / interviewers  
- Developers evaluating backend + AI integration skills

### Non-Goals
- No frontend or UI
- No authentication or user accounts
- No real-time GitHub webhooks

---

## 2. Functional Requirements

### 2.1 Endpoint: `POST /scan`

#### Purpose
Fetch all **open issues** from a GitHub repository and cache them locally.

#### Request
```json
{
  "repo": "owner/repository-name"
}
```

#### Functional Behavior
- Validate repository format (`owner/repo`)
- Call GitHub REST API to fetch **all open issues**
- Handle pagination (GitHub returns 30 issues per page by default)
- Filter out pull requests (GitHub issues API includes PRs)
- Extract and store the following fields:
  - `id`
  - `title`
  - `body`
  - `html_url`
  - `created_at`
- Store issues using **one local storage mechanism**
- Overwrite or refresh existing cached issues for the same repo

#### Success Response
```json
{
  "repo": "owner/repository-name",
  "issues_fetched": 42,
  "cached_successfully": true
}
```

#### Error Scenarios
| Case | Behavior |
|---|---|
| Invalid repo format | Return `400 Bad Request` |
| GitHub API failure | Return `502 Bad Gateway` |
| Rate limit exceeded | Return `429 Too Many Requests` |

---

### 2.2 Endpoint: `POST /analyze`

#### Purpose
Analyze cached GitHub issues using a natural-language prompt and an LLM.

#### Request
```json
{
  "repo": "owner/repository-name",
  "prompt": "Find themes across recent issues and recommend what to fix first"
}
```

#### Functional Behavior
- Validate request body
- Check if the repository has been scanned
- Load cached issues from local storage
- Combine:
  - User-provided prompt
  - Structured issue data
- Send combined context to an LLM
- Return a **fully natural-language analysis**
- Support chunking if issue count exceeds LLM context window

#### Success Response
```json
{
  "analysis": "The majority of recent issues point to authentication failures..."
}
```

#### Error Scenarios
| Case | Behavior |
|---|---|
| Repo not scanned | Return `404 Not Found` |
| No cached issues | Return `400 Bad Request` |
| LLM failure | Return `500 Internal Server Error` |

---

## 3. Non-Functional Requirements

### Performance
- `/scan` should complete within reasonable time for repositories with ≤500 issues
- `/analyze` should respond within LLM latency constraints

### Reliability
- Graceful handling of API failures
- No server crashes due to malformed inputs

### Scalability
- Designed for **single-user / demo usage**
- No horizontal scaling required

### Security
- GitHub tokens stored via environment variables
- No secrets hardcoded
- No user data persistence beyond issues

---

## 4. Storage Design

### Supported Options
One of the following must be chosen and documented:
- In-memory storage
- JSON file storage
- SQLite database

### Storage Responsibilities
- Persist issues per repository
- Enable efficient retrieval for analysis
- Allow overwrite on re-scan

---

## 5. LLM Integration

### Requirements
- Any LLM provider or local model allowed
- Prompt must include:
  - User intent
  - Issue summaries (title + body)
- Must generate **free-form natural language output**
- Handle token limits using chunking or summarization

### Example LLM Context (Conceptual)
```
User Prompt:
"Identify recurring problems and suggest priorities"

Issues:
1. Title: Login fails on Safari
   Body: Users report...
2. Title: Memory leak in worker
   Body: After long runs...
```

---

## 6. API Design Summary

| Endpoint | Method | Purpose |
|---|---|---|
| `/scan` | POST | Fetch & cache GitHub issues |
| `/analyze` | POST | Analyze cached issues with LLM |

---

## 7. Edge Cases & Handling

- Repository scanned multiple times → overwrite cache
- Empty issue list → return informative error
- Large issue sets → chunk before LLM call
- Partial LLM failures → return meaningful error message

---

## 8. Deliverables

### Required
- Public GitHub repository
- Fully working backend server
- Both endpoints implemented

### README.md Must Include
1. Setup & run instructions
2. Storage choice + reasoning
3. Prompt history:
   - AI coding prompts
   - Architecture design prompts
   - Final `/analyze` LLM prompt

---

## 9. Success Criteria

- Server runs locally without errors
- `/scan` correctly caches GitHub issues
- `/analyze` returns coherent, meaningful insights
- Code is readable, modular, and documented
- Ready for live demo and testing

---

## 10. Timeline

| Task | Time |
|---|---|
| Architecture & setup | 0.5 day |
| GitHub API + caching | 0.5 day |
| LLM integration | 0.5 day |
| Testing & README | 0.5 day |

---

✅ **Outcome:** A realistic backend system demonstrating API design, persistence, and applied LLM reasoning.
