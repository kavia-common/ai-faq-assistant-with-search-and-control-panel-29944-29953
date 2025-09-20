from functools import lru_cache
from typing import List
import os
from pydantic import BaseModel, Field


class Settings(BaseModel):
    # PUBLIC_INTERFACE
    environment: str = Field(default=os.getenv("ENVIRONMENT", "development"), description="Runtime environment.")
    cors_allow_origins: List[str] = Field(
        default_factory=lambda: os.getenv("CORS_ALLOW_ORIGINS", "*").split(","),
        description="Comma-separated list of allowed CORS origins."
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    PUBLIC_INTERFACE
    Returns cached Settings loaded from environment variables.
    """
    return Settings()
