from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "taskmanager"
    JWT_SECRET: str = "change-this-secret-in-production"
    JWT_EXPIRY_MINUTES: int = 1440  # 24 hours

    class Config:
        env_file = ".env"


settings = Settings()
