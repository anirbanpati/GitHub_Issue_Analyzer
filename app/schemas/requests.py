"""Request schemas for API endpoints."""

from pydantic import BaseModel, Field, field_validator
from enum import Enum
import re


class ScanRequest(BaseModel):
    """Request body for POST /scan endpoint."""
    repo: str = Field(..., description="GitHub repository in format 'owner/repo'")
    
    @field_validator("repo")
    @classmethod
    def validate_repo_format(cls, v: str) -> str:
        """Validate repository format as owner/repo."""
        pattern = r'^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$'
        if not re.match(pattern, v):
            raise ValueError("Invalid repository format. Expected 'owner/repo'")
        return v


class AnalysisMode(str, Enum):
    """Analysis mode for controlling speed vs comprehensiveness."""
    fast = "fast"      # Analyze 50 most recent issues (faster)
    default = "default"  # Analyze all cached issues (comprehensive)


class AnalyzeRequest(BaseModel):
    """Request body for POST /analyze endpoint."""
    repo: str = Field(..., description="GitHub repository in format 'owner/repo'")
    prompt: str = Field(..., min_length=1, description="Analysis prompt for the LLM")
    mode: AnalysisMode = Field(
        default=AnalysisMode.fast, 
        description="'fast' (50 issues) or 'default' (all issues)"
    )
    
    @field_validator("repo")
    @classmethod
    def validate_repo_format(cls, v: str) -> str:
        """Validate repository format as owner/repo."""
        pattern = r'^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$'
        if not re.match(pattern, v):
            raise ValueError("Invalid repository format. Expected 'owner/repo'")
        return v
