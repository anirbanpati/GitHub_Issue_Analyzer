"""Scan service - Business logic for scanning repositories."""

import logging
from dataclasses import dataclass
from typing import List

from app.clients.github_client import github_client
from app.repositories.issue_repository import issue_repository
from app.exceptions import GitHubClientError

logger = logging.getLogger(__name__)


@dataclass
class ScanResult:
    """Result of a repository scan."""
    repo: str
    issues_fetched: int
    cached_successfully: bool


class ScanService:
    """Service for scanning GitHub repositories."""
    
    async def scan_repository(self, repo: str) -> ScanResult:
        """
        Fetch all open issues from a GitHub repository and cache them.
        
        Args:
            repo: Repository in 'owner/repo' format
            
        Returns:
            ScanResult with scan details
            
        Raises:
            GitHubClientError: If GitHub API fails
        """
        logger.info(f"Scanning repository: {repo}")
        
        # Parse owner and repo
        owner, repo_name = repo.split("/")
        
        # Fetch issues from GitHub
        issues = await github_client.fetch_open_issues(owner, repo_name)
        logger.info(f"Fetched {len(issues)} issues from GitHub")
        
        # Convert Issue objects to dicts for storage
        issues_data = [
            {
                "id": issue.id,
                "title": issue.title,
                "body": issue.body,
                "html_url": issue.html_url,
                "created_at": issue.created_at
            }
            for issue in issues
        ]
        
        # Save to database
        count = issue_repository.save_issues(repo, issues_data)
        logger.info(f"Cached {count} issues successfully")
        
        return ScanResult(
            repo=repo,
            issues_fetched=count,
            cached_successfully=True
        )


# Singleton instance
scan_service = ScanService()
