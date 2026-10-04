"""Application settings and AI client configuration."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI


@dataclass(frozen=True)
class Settings:
    """Configuration loaded from environment variables."""

    ai_base_url: str
    ai_api_key: str
    ai_model: str


def load_settings() -> Settings:
    """Load application settings from the environment and `.env`."""
    load_dotenv()

    return Settings(
        ai_base_url=os.getenv(
            "AI_BASE_URL",
            "http://localhost:20128/v1",
        ),
        ai_api_key=os.getenv(
            "AI_API_KEY",
            "local",
        ),
        ai_model=os.getenv("AI_MODEL", ""),
    )


settings = load_settings()

client = OpenAI(
    base_url=settings.ai_base_url,
    api_key=settings.ai_api_key,
)
