import os

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
