from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import DEBUG, tags_metadata
from app.core.lifecycle import app_lifespan
from app.api.routes.posts import router as posts_router
from app.api.routes.general import router as general_router

app = FastAPI(
    debug=DEBUG,
    title="ChatWithDocs Web Service",
    description=(
        "This project is a production ready ChatWithDocs Web Service"
        "<br /><br />"
        "Author - [***Coumarane COUPPANE***](https://www.linkedin.com/https://www.linkedin.com/in/coumarane-couppane-712a2415/)"
    ),
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/swagger/",
    lifespan=app_lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to your frontend's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(general_router)
app.include_router(posts_router, prefix="/api")

print("completed app init.")
