import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    database_url: str = os.getenv("DATABASE_URL", "")
    better_auth_secret: str = os.getenv("BETTER_AUTH_SECRET", "")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"  # This will ignore extra fields that aren't defined in the model
    )


# Create a single instance of settings
settings = Settings()