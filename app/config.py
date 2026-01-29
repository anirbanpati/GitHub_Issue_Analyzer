"""Configuration management for the application."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "./data/issues.db")
    
    # LLM settings
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    MAX_ISSUES_PER_CHUNK: int = int(os.getenv("MAX_ISSUES_PER_CHUNK", "20"))


settings = Settings()
