# 🔍 GitHub Issue Analyzer

A backend service built with **FastAPI** that fetches, caches, and analyzes GitHub issues using LLM.

## ✨ Features

- **POST /scan** - Fetch and cache all open GitHub issues for a repository
- **POST /analyze** - Analyze cached issues using natural language prompts with LLM

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- GitHub Personal Access Token
- OpenAI API Key

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd GitHub_Issue_Analyzer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
GITHUB_TOKEN=your_github_token_here
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_PATH=./data/issues.db
```

### Run the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Using Docker directly

```bash
# Build image
docker build -t github-issue-analyzer .

# Run container
docker run -d \
  -p 8000:8000 \
  -e GITHUB_TOKEN=your_token \
  -e OPENAI_API_KEY=your_key \
  -v $(pwd)/data:/app/data \
  --name github-issue-analyzer \
  github-issue-analyzer
```

---

## 📡 API Endpoints

### POST /scan

Fetch and cache all open issues for a GitHub repository.

**Request:**
```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"repo": "facebook/react"}'
```

**Response:**
```json
{
  "repo": "facebook/react",
  "issues_fetched": 42,
  "cached_successfully": true
}
```

### POST /analyze

Analyze cached issues using a natural language prompt.

**Request:**
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "repo": "facebook/react",
    "prompt": "Find themes across recent issues",
    "mode": "fast"
  }'
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `repo` | string | required | Repository in `owner/repo` format |
| `prompt` | string | required | Natural language analysis prompt |
| `mode` | string | `fast` | `"fast"` (50 issues, ~20s) or `"default"` (all issues) |

**Response:**
```json
{
  "analysis": "Based on the analysis of recent issues..."
}
```

---

## 🗄️ Storage Choice: SQLite

**Why SQLite?**

1. **Durability** - Data persists across server restarts
2. **Structured Querying** - Efficient lookups by repository
3. **Zero Configuration** - No external database server needed
4. **Easy Inspection** - Can open with any SQLite client
5. **Lightweight** - Perfect for demo/interview scenarios

---

## 🏗️ Project Structure

```
GitHub_Issue_Analyzer/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application & endpoints
│   ├── config.py         # Environment configuration
│   ├── database.py       # SQLite storage layer
│   ├── models.py         # Pydantic request/response models
│   ├── github_client.py  # GitHub API integration
│   └── llm_adapter.py    # LLM integration with chunking
├── data/                 # SQLite database (auto-created)
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 📝 Prompt History

### AI Coding Prompts Used

1. "Create a FastAPI backend with /scan and /analyze endpoints for GitHub issue analysis"
2. "Implement pagination for GitHub API with PR filtering"
3. "Add chunking strategy for large issue sets to handle LLM context limits"

### Architecture Design Prompts

1. "Design SQLite schema for caching GitHub issues with efficient repo lookups"
2. "Structure FastAPI project with separation of concerns"

### Final /analyze LLM Prompt

```
System: You are an experienced open-source maintainer and software engineer.
You are analyzing GitHub issues for a repository. Provide clear, actionable 
insights based on the issues provided. Be specific about patterns, priorities, 
and recommendations.

User: [User's prompt]

Issues:
1. **[Issue Title]**
   Created: [timestamp]
   URL: [url]
   Description: [body]
...
```

---

## 🧪 Testing

### Test Scan Endpoint
```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"repo": "octocat/Hello-World"}'
```

### Test Analyze Endpoint
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"repo": "octocat/Hello-World", "prompt": "Summarize the main issues"}'
```

### API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI.

---

## ⚠️ Error Handling

| Scenario | Status Code | Message |
|----------|-------------|---------|
| Invalid repo format | 400 | Invalid repository format |
| Repo not found | 404 | Repository not found |
| Rate limit exceeded | 429 | Rate limit exceeded |
| GitHub API error | 502 | GitHub API error |
| Repo not scanned | 404 | Repository has not been scanned |
| LLM failure | 500 | LLM analysis failed |

---

## 📄 License

MIT
