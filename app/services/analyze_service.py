"""Analyze service - Business logic for analyzing issues."""

import logging
from typing import List

from app.clients.llm_client import llm_client
from app.repositories.issue_repository import issue_repository
from app.exceptions import RepositoryNotFoundError, NoIssuesFoundError, LLMError

logger = logging.getLogger(__name__)


class AnalyzeService:
    """Service for analyzing GitHub issues."""
    
    async def analyze_issues(
        self, 
        repo: str, 
        prompt: str, 
        mode: str = "fast"
    ) -> str:
        """
        Analyze cached issues for a repository using LLM.
        
        Args:
            repo: Repository in 'owner/repo' format
            prompt: Analysis prompt
            mode: 'fast' (50 issues) or 'default' (all issues)
            
        Returns:
            Analysis result from LLM
            
        Raises:
            RepositoryNotFoundError: If repo hasn't been scanned
            NoIssuesFoundError: If no issues found
            LLMError: If LLM analysis fails
        """
        logger.info(f"Analyzing repository: {repo}")
        
        # Check if repository has been scanned
        if not issue_repository.has_repo(repo):
            raise RepositoryNotFoundError(repo)
        
        # Get cached issues
        issues = issue_repository.get_issues_by_repo(repo)
        
        if not issues:
            raise NoIssuesFoundError(repo)
        
        logger.info(f"Found {len(issues)} cached issues for analysis")
        
        # Apply mode: fast (50 issues) or default (all)
        if mode == "fast" and len(issues) > 50:
            logger.info("Fast mode: Limiting to 50 most recent issues")
            issues = issues[:50]
        else:
            logger.info(f"Default mode: Analyzing all {len(issues)} issues")
        
        # Analyze with LLM
        analysis = await llm_client.analyze(prompt, issues)
        logger.info("LLM analysis completed successfully")
        
        return analysis


# Singleton instance
analyze_service = AnalyzeService()
