from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
from typing import Optional, List


class Settings(BaseSettings):
    # App
    app_name: str = "VampireVTT"
    debug: bool = True
    ENVIRONMENT: str = "development"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"

    # Database (SQLite for development, PostgreSQL for production)
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./vampire_vtt.db",
        alias="DATABASE_URL"
    )

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # Discord OAuth
    DISCORD_CLIENT_ID: Optional[str] = None
    DISCORD_CLIENT_SECRET: Optional[str] = None
    DISCORD_REDIRECT_URI: str = "http://localhost:8000/api/auth/discord/callback"

    # JWT
    JWT_SECRET: str = "your-jwt-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # CORS
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # Frontend URL
    FRONTEND_URL: str = "http://localhost:5173"

    # Aliases for compatibility
    @property
    def database_url(self) -> str:
        return self.DATABASE_URL

    @property
    def redis_url(self) -> str:
        return self.REDIS_URL

    @property
    def discord_client_id(self) -> Optional[str]:
        return self.DISCORD_CLIENT_ID

    @property
    def discord_client_secret(self) -> Optional[str]:
        return self.DISCORD_CLIENT_SECRET

    @property
    def discord_redirect_uri(self) -> str:
        return self.DISCORD_REDIRECT_URI

    @property
    def secret_key(self) -> str:
        return self.SECRET_KEY

    @property
    def frontend_url(self) -> str:
        return self.FRONTEND_URL

    @property
    def jwt_secret(self) -> str:
        return self.JWT_SECRET

    @property
    def jwt_algorithm(self) -> str:
        return self.JWT_ALGORITHM

    @property
    def jwt_expire_minutes(self) -> int:
        return self.JWT_EXPIRE_MINUTES

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        populate_by_name = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
