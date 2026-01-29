"""Issue repository for database operations."""

import sqlite3
from typing import List, Optional
from pathlib import Path
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class IssueRepository:
    """Repository for managing issues in SQLite database."""
    
    def __init__(self):
        self.db_path = settings.DATABASE_PATH
    
    def init_db(self) -> None:
        """Initialize the database and create tables if they don't exist."""
        # Ensure the directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS issues (
                id INTEGER PRIMARY KEY,
                repo TEXT NOT NULL,
                title TEXT NOT NULL,
                body TEXT,
                html_url TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        
        # Create index on repo for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_issues_repo ON issues(repo)
        ''')
        
        conn.commit()
        conn.close()
        logger.info(f"Database initialized at {self.db_path}")
    
    def save_issues(self, repo: str, issues: List[dict]) -> int:
        """
        Save issues to the database.
        Clears existing issues for the repo before inserting new ones.
        Returns the number of issues saved.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete existing issues for this repo
        cursor.execute('DELETE FROM issues WHERE repo = ?', (repo,))
        
        # Insert new issues
        for issue in issues:
            cursor.execute('''
                INSERT INTO issues (id, repo, title, body, html_url, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                issue.id if hasattr(issue, 'id') else issue['id'],
                repo,
                issue.title if hasattr(issue, 'title') else issue['title'],
                issue.body if hasattr(issue, 'body') else issue.get('body', ''),
                issue.html_url if hasattr(issue, 'html_url') else issue['html_url'],
                issue.created_at if hasattr(issue, 'created_at') else issue['created_at']
            ))
        
        conn.commit()
        conn.close()
        
        return len(issues)
    
    def get_issues_by_repo(self, repo: str) -> List[dict]:
        """Retrieve all issues for a given repository."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, repo, title, body, html_url, created_at
            FROM issues
            WHERE repo = ?
            ORDER BY created_at DESC
        ''', (repo,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def has_repo(self, repo: str) -> bool:
        """Check if a repository has been scanned (exists in database)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM issues WHERE repo = ?', (repo,))
        count = cursor.fetchone()[0]
        conn.close()
        
        return count > 0
    
    def get_issue_count(self, repo: str) -> int:
        """Get the number of cached issues for a repository."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM issues WHERE repo = ?', (repo,))
        count = cursor.fetchone()[0]
        conn.close()
        
        return count


# Singleton instance
issue_repository = IssueRepository()
