"""Health check routes."""

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to GitHub Issue Analyzer API", "docs": "/docs"}


@router.get("/health")
async def health_check():
    """Health check endpoint for Docker and monitoring."""
    return {
        "status": "healthy",
        "service": "GitHub Issue Analyzer",
        "version": "1.0.0"
    }
