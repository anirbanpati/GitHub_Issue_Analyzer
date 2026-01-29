"""Routes package - HTTP route handlers."""

from fastapi import APIRouter
from app.routes import health, issues

# Main router that includes all sub-routers
router = APIRouter()
router.include_router(health.router)
router.include_router(issues.router)

__all__ = ["router"]
