# 🛠️ Technical Documentation
## GitHub Issue Analyzer with Local Caching + LLM Processing

---

## 1. Purpose of This Document

This document provides **technical implementation details** for the GitHub Issue Analyzer. It is intended for:
- Reviewers evaluating engineering depth
- Developers maintaining or extending the system
- Interview panels conducting live demos

It complements the **PRD** by explaining *how* the system is built rather than *what* it does.

---

## 2. Technology Stack

### Backend
| Layer | Technology |
|---|---|
| Runtime | Node.js (LTS) / Python 3.10+ |
| Framework | Express.js / FastAPI |
| HTTP Client | Axios / Fetch / Requests |
| Environment Config | dotenv |

### External Services
| Service | Purpose |
|---|---|
| GitHub REST API | Fetch open issues |
| LLM Provider | Issue analysis & summarization |

### Storage (Example Choice)
| Option | Selected |
|---|---|
| In-memory | ❌ |
| JSON File | ❌ |
| SQLite | ✅ |

> **Reasoning:** SQLite provides durability, structured querying, and easy inspection without external dependencies.

---

## 3. High-Level Architecture

```
Client
  │
  ▼
REST API Server
  │
  ├── GitHub API Client
  │
  ├── Local Cache (SQLite)
  │
  └── LLM Adapter
```

### Key Design Principles
- Stateless HTTP endpoints
- Deterministic caching behavior
- LLM isolated behind a service layer
- Fail-fast error handling

---

## 4. API Layer

### POST /scan

**Responsibility:**
- Fetch open GitHub issues
- Normalize and persist data

**Flow:**
1. Validate `owner/repo` format
2. Call GitHub Issues API with pagination
3. Filter out pull requests
4. Normalize issue fields
5. Store issues in local cache
6. Return scan summary

---

### POST /analyze

**Responsibility:**
- Analyze cached issues using LLM

**Flow:**
1. Validate request payload
2. Check repository cache existence
3. Load cached issues
4. Build LLM prompt context
5. Chunk issues if needed
6. Call LLM provider
7. Aggregate and return analysis

---

## 5. Data Model

### Issues Table (SQLite Example)

| Column | Type | Description |
|---|---|---|
| id | INTEGER | GitHub issue ID |
| repo | TEXT | owner/repo |
| title | TEXT | Issue title |
| body | TEXT | Issue description |
| html_url | TEXT | GitHub issue URL |
| created_at | TEXT | ISO timestamp |

**Indexes:**
- `(repo)` for fast lookup

---

## 6. GitHub API Integration

### Endpoint Used
```
GET /repos/{owner}/{repo}/issues?state=open
```

### Pagination Strategy
- Use `page` and `per_page` parameters
- Continue until empty response

### Pull Request Filtering
- GitHub issues API returns PRs
- Filter by checking presence of `pull_request` field

### Rate Limits
- Handle HTTP `403` with rate-limit headers
- Fail gracefully with meaningful error

---

## 7. LLM Integration

### LLM Abstraction Layer

Responsibilities:
- Accept structured issue data
- Build prompt safely
- Handle retries and failures

### Prompt Construction Strategy

```
System:
You are an experienced open-source maintainer.

User Prompt:
<user-provided instruction>

Issues:
- Title: ...
  Body: ...
```

### Chunking Strategy
- Max N issues per request
- Summarize chunks individually
- Combine summaries into final analysis

---

## 8. Error Handling Strategy

| Layer | Strategy |
|---|---|
| Input Validation | 400 errors |
| External APIs | 502 / 429 |
| Cache Miss | 404 |
| LLM Failure | 500 with message |

All errors return structured JSON responses.

---

## 9. Configuration & Environment Variables

```env
GITHUB_TOKEN=xxxxx
LLM_API_KEY=xxxxx
DATABASE_PATH=./data/issues.db
```

- No secrets stored in code
- `.env` excluded from version control

---

## 10. Testing Strategy

### Manual Testing
- curl / Postman for endpoint validation

### Test Cases
- Valid repo with issues
- Repo with zero issues
- Analyze before scan
- Large issue sets
- Invalid inputs

---

## 11. Observability & Logging

- Log incoming requests
- Log GitHub API failures
- Log LLM request/response metadata (no content)

---

## 12. Deployment Notes

- Designed for local execution
- Single-process server
- No background jobs required

---

## 13. Extensibility

Future enhancements:
- Webhook-based incremental updates
- Multiple repo support per request
- Issue labeling and clustering
- Streaming LLM responses

---

## 14. Summary

This technical design prioritizes:
- Simplicity
- Reliability
- Clear separation of concerns
- Interview-ready clarity

The system is production-inspired while remaining lightweight and easy to reason about.

---

✅ **Status:** Ready for implementation and live demo

