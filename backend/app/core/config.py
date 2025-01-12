import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

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

# Load environment variables from a .env file
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()