# 📋 GitHub Issue Analyzer - TODO List

> A comprehensive task breakdown for implementing the GitHub Issue Analyzer with Local Caching + LLM Processing

---

## 🏗️ Phase 1: Project Setup & Architecture

### 1.1 Initialize Project
- [x] Create project directory structure
- [x] Initialize Python project with FastAPI
- [x] Install core dependencies:
  - [x] FastAPI (framework)
  - [x] httpx (HTTP client)
  - [x] python-dotenv (environment configuration)
  - [x] SQLite (built-in Python)
  - [x] LangChain + LangChain-OpenAI (LLM integration)
- [x] Set up `.gitignore` file
- [x] Create `.env.example` template

### 1.2 Environment Configuration
- [x] Create `.env` file with required variables:
  - [x] `GITHUB_TOKEN`
  - [x] `OPENAI_API_KEY`
  - [x] `DATABASE_PATH`
- [x] Set up configuration loader module (`app/config.py`)
- [x] Validate environment variables on startup

### 1.3 Server Skeleton
- [x] Create main server entry file (`app/main.py`)
- [x] Set up FastAPI app instance
- [x] Configure JSON body parser (built-in)
- [x] Add basic request logging middleware
- [x] Define server port configuration
- [x] Add graceful shutdown handling (lifespan)

---

## 🗄️ Phase 2: Storage Layer (SQLite)

### 2.1 Database Setup
- [x] Create database initialization module (`app/database.py`)
- [x] Define schema for `issues` table:
  - [x] `id` (INTEGER - GitHub issue ID)
  - [x] `repo` (TEXT - owner/repo)
  - [x] `title` (TEXT)
  - [x] `body` (TEXT)
  - [x] `html_url` (TEXT)
  - [x] `created_at` (TEXT - ISO timestamp)
- [x] Create index on `repo` column for fast lookup
- [x] Implement auto-migration on startup

### 2.2 Repository Layer
- [x] Create database functions module
- [x] Implement `save_issues(repo, issues)` method
  - [x] Clear existing issues for repo before insert
  - [x] Bulk insert new issues
- [x] Implement `get_issues_by_repo(repo)` method
- [x] Implement `has_repo(repo)` method (cache check)

---

## 🔌 Phase 3: GitHub API Integration

### 3.1 GitHub Client Module
- [x] Create `GitHubClient` class (`app/github_client.py`)
- [x] Configure authentication header with `GITHUB_TOKEN`
- [x] Set base URL for GitHub REST API
- [x] Add request timeout configuration

### 3.2 Fetch Issues Implementation
- [x] Implement `fetch_open_issues(owner, repo)` method
- [x] Handle pagination:
  - [x] Use `page` and `per_page` query parameters
  - [x] Loop until response is empty or 422
  - [x] Default `per_page=100` for efficiency
- [x] Filter out pull requests:
  - [x] Check for `pull_request` field presence
  - [x] Exclude items with `pull_request` field
- [x] Normalize response to extract required fields:
  - [x] `id`, `title`, `body`, `html_url`, `created_at`

### 3.3 Error Handling
- [x] Handle HTTP 403 (rate limit exceeded)
  - [x] Parse `X-RateLimit-*` headers
  - [x] Return appropriate error message
- [x] Handle HTTP 404 (repository not found)
- [x] Handle network errors / timeouts
- [x] Handle HTTP 422 (pagination limit)

---

## 📡 Phase 4: POST /scan Endpoint

### 4.1 Request Validation
- [x] Validate request body exists (Pydantic)
- [x] Validate `repo` field is present
- [x] Validate `repo` format matches `owner/repository-name`
  - [x] Regex: `^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$`
- [x] Return `400 Bad Request` for invalid input

### 4.2 Core Logic
- [x] Parse `owner` and `repo` from request
- [x] Call GitHub client to fetch all open issues
- [x] Store fetched issues in SQLite cache
- [x] Build success response with count

### 4.3 Response Handling
- [x] Return success response:
  ```json
  {
    "repo": "owner/repository-name",
    "issues_fetched": 42,
    "cached_successfully": true
  }
  ```
- [x] Handle error scenarios:
  - [x] `400` - Invalid repo format
  - [x] `502` - GitHub API failure
  - [x] `429` - Rate limit exceeded

---

## 🤖 Phase 5: LLM Integration (LangChain)

### 5.1 LLM Adapter Setup
- [x] Create `LLMAdapter` class (`app/llm_adapter.py`)
- [x] Configure LangChain with ChatOpenAI
- [x] Set up authentication with `OPENAI_API_KEY`
- [x] Configure model selection (gpt-3.5-turbo)
- [x] Set temperature and max tokens parameters

### 5.2 Prompt Construction
- [x] Create prompt template with:
  - [x] System message (open-source maintainer persona)
  - [x] User-provided prompt/instruction
  - [x] Formatted issue data (title + body)
- [x] Implement issue data formatting function
- [x] Convert issues to LangChain Documents

### 5.3 Chunking Strategy (Map-Reduce)
- [x] Define maximum issues per LLM request (15)
- [x] Implement issue chunking logic
- [x] Create per-chunk analysis handler (map phase)
- [x] Implement hierarchical summary aggregation (reduce phase)
- [x] Handle single-chunk optimization (direct analysis)

### 5.4 LLM Request Handling
- [x] Implement `analyze(prompt, issues)` method
- [x] Use LCEL chains (prompt | llm | parser)
- [x] Implement map-reduce for large issue sets
- [x] Log request metadata for observability

---

## 📊 Phase 6: POST /analyze Endpoint

### 6.1 Request Validation
- [x] Validate request body exists (Pydantic)
- [x] Validate `repo` field is present and valid format
- [x] Validate `prompt` field is present and non-empty
- [x] Return `400 Bad Request` for invalid input

### 6.2 Cache Verification
- [x] Check if repository has been scanned
- [x] Return `404 Not Found` if repo not cached
- [x] Check if cached issues exist
- [x] Return `400 Bad Request` if no issues cached

### 6.3 Core Logic
- [x] Load cached issues from SQLite
- [x] Build combined LLM context:
  - [x] User prompt
  - [x] Issue summaries
- [x] Apply chunking if needed
- [x] Call LLM adapter for analysis
- [x] Aggregate chunked responses if applicable

### 6.4 Response Handling
- [x] Return success response:
  ```json
  {
    "analysis": "<LLM-generated text here>"
  }
  ```
- [x] Handle error scenarios:
  - [x] `404` - Repo not scanned
  - [x] `400` - No cached issues
  - [x] `500` - LLM failure

---

## 🧪 Phase 7: Testing & Validation

### 7.1 Manual Testing Cases
- [x] Test `/scan` with valid repository (has issues)
- [ ] Test `/scan` with valid repository (zero issues)
- [ ] Test `/scan` with invalid repo format
- [ ] Test `/scan` with non-existent repository
- [ ] Test `/scan` re-scan (cache overwrite)
- [/] Test `/analyze` after successful scan
- [ ] Test `/analyze` before any scan (404)
- [ ] Test `/analyze` with empty prompt
- [/] Test `/analyze` with large issue set (chunking)

### 7.2 Edge Case Testing
- [ ] Test rate limit handling
- [ ] Test network timeout handling
- [ ] Test LLM failure handling
- [ ] Test malformed JSON request body
- [x] Test very long issue bodies (truncation)

### 7.3 Testing Tools
- [x] Create sample curl commands for both endpoints
- [ ] Set up Postman collection (optional)
- [ ] Document expected responses for each test case

---

## 📚 Phase 8: Documentation

### 8.1 README.md
- [x] Add project title and description
- [x] Add prerequisites section
- [x] Write setup instructions:
  - [x] Clone repository
  - [x] Install dependencies
  - [x] Configure environment variables
- [x] Write run instructions
- [x] Document API endpoints with examples
- [x] Explain storage choice (SQLite) + reasoning
- [x] Add prompt history section:
  - [x] AI coding tool prompts
  - [x] Architecture design prompts
  - [x] Final `/analyze` LLM prompt

### 8.2 Code Documentation
- [x] Add docstrings to all functions
- [x] Document module purposes
- [x] Add inline comments for complex logic

---

## 🚀 Phase 9: Final Polish

### 9.1 Code Quality
- [x] Review and refactor code for readability
- [x] Ensure consistent code style
- [x] Remove debug logs and unused code
- [x] Check for security issues (no hardcoded secrets)

### 9.2 Error Messages
- [x] Ensure all error responses are user-friendly
- [x] Verify structured JSON format for all errors
- [x] Add helpful suggestions in error messages

### 9.3 Demo Readiness
- [x] Verify server starts without errors
- [/] Test both endpoints end-to-end
- [ ] Prepare demo script/walkthrough
- [x] Verify all deliverables are complete

---

## 📦 Deliverables Checklist

- [ ] Public GitHub repository created
- [x] Fully working backend server
- [x] `POST /scan` endpoint implemented
- [x] `POST /analyze` endpoint implemented
- [x] README.md with:
  - [x] Setup & run instructions
  - [x] Storage choice + reasoning
  - [x] Prompt history
- [x] Code is readable, modular, and documented
- [/] Ready for live demo and testing

---

## 🗓️ Timeline Reference

| Phase | Estimated Time | Status |
|-------|----------------|--------|
| Setup & Architecture | 0.5 day | ✅ Done |
| Storage Layer | 0.25 day | ✅ Done |
| GitHub API Integration | 0.25 day | ✅ Done |
| POST /scan Endpoint | 0.25 day | ✅ Done |
| LLM Integration | 0.5 day | ✅ Done |
| POST /analyze Endpoint | 0.25 day | ✅ Done |
| Testing & Validation | 0.25 day | 🔄 In Progress |
| Documentation | 0.25 day | ✅ Done |
| Final Polish | Remaining | 🔄 In Progress |

---

✅ **Goal:** Build a production-inspired backend demonstrating API design, local caching, and LLM integration.
