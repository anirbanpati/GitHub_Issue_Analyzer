"""Issue routes - /scan and /analyze endpoints."""

import logging
from fastapi import APIRouter, HTTPException

from app.schemas import (
    ScanRequest, ScanResponse,
    AnalyzeRequest, AnalyzeResponse,
    ErrorResponse
)
from app.services import scan_service, analyze_service
from app.exceptions import GitHubClientError, LLMError, RepositoryNotFoundError, NoIssuesFoundError

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Issues"])


@router.post("/scan", response_model=ScanResponse, responses={
    400: {"model": ErrorResponse},
    429: {"model": ErrorResponse},
    502: {"model": ErrorResponse}
})
async def scan_repository(request: ScanRequest):
    """
    Fetch all open GitHub issues for a repository and cache them locally.
    
    - Fetches all open issues using GitHub REST API
    - Handles pagination automatically
    - Filters out pull requests
    - Caches issues in SQLite database
    """
    try:
        result = await scan_service.scan_repository(request.repo)
        return ScanResponse(
            repo=result.repo,
            issues_fetched=result.issues_fetched,
            cached_successfully=result.cached_successfully
        )
    except GitHubClientError as e:
        logger.error(f"GitHub API error: {e.message}")
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.post("/analyze", response_model=AnalyzeResponse, responses={
    400: {"model": ErrorResponse},
    404: {"model": ErrorResponse},
    500: {"model": ErrorResponse}
})
async def analyze_issues(request: AnalyzeRequest):
    """
    Analyze cached GitHub issues using a natural-language prompt and LLM.
    
    - Retrieves cached issues for the repository
    - Combines user prompt with issue data
    - Sends to LLM for analysis
    - Returns natural-language analysis
    """
    try:
        analysis = await analyze_service.analyze_issues(
            repo=request.repo,
            prompt=request.prompt,
            mode=request.mode.value
        )
        return AnalyzeResponse(analysis=analysis)
    
    except RepositoryNotFoundError as e:
        logger.error(f"Repository not found: {e.message}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except NoIssuesFoundError as e:
        logger.error(f"No issues found: {e.message}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except LLMError as e:
        logger.error(f"LLM error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
