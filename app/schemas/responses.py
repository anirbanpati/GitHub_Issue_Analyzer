"""Response schemas for API endpoints."""

from pydantic import BaseModel
from typing import Optional


class ScanResponse(BaseModel):
    """Response body for POST /scan endpoint."""
    repo: str
    issues_fetched: int
    cached_successfully: bool


class AnalyzeResponse(BaseModel):
    """Response body for POST /analyze endpoint."""
    analysis: str


class HealthResponse(BaseModel):
    """Response body for GET /health endpoint."""
    status: str
    service: str
    version: str


class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str
