"""Custom exceptions for the application."""


class AppException(Exception):
    """Base exception for the application."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class GitHubClientError(AppException):
    """Exception for GitHub API errors."""
    pass


class LLMError(AppException):
    """Exception for LLM-related errors."""
    def __init__(self, message: str):
        super().__init__(message, status_code=500)


class RepositoryNotFoundError(AppException):
    """Exception when repository is not found in cache."""
    def __init__(self, repo: str):
        super().__init__(
            f"Repository '{repo}' has not been scanned. Please call /scan first.",
            status_code=404
        )


class NoIssuesFoundError(AppException):
    """Exception when no issues are found for a repository."""
    def __init__(self, repo: str):
        super().__init__(
            f"No issues found for repository '{repo}'. The repository may have no open issues.",
            status_code=400
        )
