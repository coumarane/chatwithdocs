from sqlalchemy.orm import declarative_base
from .user import User
from .post import Post

# Base object for all models
Base = declarative_base()

# Export models and metadata for Alembic
__all__ = ["Base", "User", "Post"]