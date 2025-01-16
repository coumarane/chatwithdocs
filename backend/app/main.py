from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import DEBUG, tags_metadata
from app.core.lifecycle import app_lifespan
from app.api.routes.posts_route import router as posts_router
from app.api.routes.general_route import router as general_router
from app.api.routes.users_route import router as user_router
from app.api.routes.auth_route import router as auth_router
from dotenv import load_dotenv

from app.core.middleware.login_middleware import LoggingMiddleware

# Load environment variables from a .env file
load_dotenv()


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

# Add the logging middleware
app.add_middleware(LoggingMiddleware)

# Include API routes
app.include_router(general_router)
app.include_router(posts_router, prefix="/api")
app.include_router(user_router, prefix="/api", tags=["users"])
app.include_router(auth_router, prefix="/api")

# Instrument the app for Prometheus
Instrumentator().instrument(app).expose(app)

print("completed app init.")
