import os
from pydantic_settings import BaseSettings
from pydantic import Field

DEBUG = os.environ.get("DEBUG", "").strip().lower() in {"1", "true", "on", "yes"}


tags_metadata = [
    {
        "name": "Build",
        "description": "Use this API to check project build number."
    },
    {
        "name": "Chat With Docs",
        "description": "ChatWithDocs Service APIs"
    },
]


class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(15, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(1440, env="REFRESH_TOKEN_EXPIRE_MINUTES")
    REDIS_HOST: str = Field(default=None, env="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT")  # Default value for optional integer
    REDIS_URL: str = Field(default=None, env="REDIS_URL")
    MAIL_USERNAME: str = Field(default=None, env="MAIL_USERNAME")
    MAIL_PASSWORD: str = Field(default=None, env="MAIL_PASSWORD")
    MAIL_SERVER: str = Field(default=None, env="MAIL_SERVER")
    MAIL_PORT: int = Field(default=587, env="MAIL_PORT")  # Default value for optional integer
    MAIL_FROM: str = Field(default=None, env="MAIL_FROM")
    MAIL_FROM_NAME: str = Field(default=None, env="MAIL_FROM_NAME")
    DOMAIN: str = Field(default="localhost", env="DOMAIN")  # Default string value
    APP_VERSION: str = Field(default="1.0.0", env="APP_VERSION")

settings = Settings()
