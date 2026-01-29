"""Main FastAPI application - App factory and configuration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.routes import router
from app.repositories import issue_repository

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    logger.info("Initializing database...")
    issue_repository.init_db()
    logger.info("Database initialized successfully")
    yield


# API Tags for documentation
tags_metadata = [
    {
        "name": "Health",
        "description": "Health check and status endpoints"
    },
    {
        "name": "Issues",
        "description": "Endpoints for fetching and analyzing GitHub issues"
    }
]

app = FastAPI(
    title="GitHub Issue Analyzer",
    description="""
## 🔍 GitHub Issue Analyzer API

A backend service that fetches, caches, and analyzes GitHub issues using LLM.

### Features:
- **Scan repositories** - Fetch and cache all open issues from any public GitHub repository
- **Analyze issues** - Use natural language prompts to analyze cached issues with AI
- **Two analysis modes** - Fast mode (50 issues) or Default mode (all issues)

### Quick Start:
1. Call `/scan` with a repository name to fetch issues
2. Call `/analyze` with a prompt to get AI-powered insights

### Authentication:
- Requires `GITHUB_TOKEN` for GitHub API access
- Requires `OPENAI_API_KEY` for LLM analysis
    """,
    version="1.0.0",
    contact={
        "name": "GitHub Issue Analyzer",
        "url": "https://github.com/your-repo/github-issue-analyzer"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    openapi_tags=tags_metadata,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routes
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
