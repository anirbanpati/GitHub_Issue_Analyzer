"""GitHub API client for fetching issues."""

import httpx
from typing import List
from dataclasses import dataclass

from app.config import settings
from app.exceptions import GitHubClientError


@dataclass
class Issue:
    """GitHub issue data model."""
    id: int
    title: str
    body: str
    html_url: str
    created_at: str


class GitHubClient:
    """Client for interacting with GitHub REST API."""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self):
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Issue-Analyzer"
        }
        if settings.GITHUB_TOKEN:
            self.headers["Authorization"] = f"token {settings.GITHUB_TOKEN}"
    
    async def fetch_open_issues(self, owner: str, repo: str) -> List[Issue]:
        """
        Fetch all open issues for a repository.
        Handles pagination and filters out pull requests.
        """
        issues: List[Issue] = []
        page = 1
        per_page = 100  # Maximum allowed by GitHub
        
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            while True:
                url = f"{self.BASE_URL}/repos/{owner}/{repo}/issues"
                params = {
                    "state": "open",
                    "page": page,
                    "per_page": per_page
                }
                
                try:
                    response = await client.get(url, headers=self.headers, params=params)
                except httpx.TimeoutException:
                    raise GitHubClientError("GitHub API request timed out", 504)
                except httpx.RequestError as e:
                    raise GitHubClientError(f"Network error: {str(e)}", 502)
                
                # Handle rate limiting
                if response.status_code == 403:
                    remaining = response.headers.get("X-RateLimit-Remaining", "0")
                    if remaining == "0":
                        raise GitHubClientError(
                            "GitHub API rate limit exceeded. Please try again later.",
                            429
                        )
                    raise GitHubClientError("GitHub API access forbidden", 403)
                
                # Handle not found
                if response.status_code == 404:
                    raise GitHubClientError(
                        f"Repository '{owner}/{repo}' not found",
                        404
                    )
                
                # Handle 422 - pagination limit reached
                if response.status_code == 422:
                    break
                
                # Handle other errors
                if response.status_code != 200:
                    raise GitHubClientError(
                        f"GitHub API error: {response.status_code}",
                        502
                    )
                
                data = response.json()
                
                # Empty response means no more pages
                if not data:
                    break
                
                # Filter out pull requests and extract required fields
                for item in data:
                    # Skip pull requests (they have a 'pull_request' field)
                    if "pull_request" in item:
                        continue
                    
                    issue = Issue(
                        id=item["id"],
                        title=item["title"],
                        body=item.get("body") or "",
                        html_url=item["html_url"],
                        created_at=item["created_at"]
                    )
                    issues.append(issue)
                
                # If we got fewer items than per_page, we've reached the end
                if len(data) < per_page:
                    break
                
                page += 1
        
        return issues


# Singleton instance
github_client = GitHubClient()
