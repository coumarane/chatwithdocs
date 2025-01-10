from typing import List
from fastapi import APIRouter
from app.domain.post import Post

router = APIRouter()

@router.get("/posts", response_model=List[Post])
async def get_posts():
    return [
        {"id": 1, "title": "First Post", "body": "This is the body of the first post"},
        {"id": 2, "title": "Second Post", "body": "This is the body of the second post"},
        {"id": 3, "title": "Third Post", "body": "This is the body of the third post"},
        # Add more posts as needed
    ]
