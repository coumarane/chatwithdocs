from fastapi import FastAPI
import logging
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.middleware.cors import CORSMiddleware
from api.routes.general_route import router as general_router
from api.routes.users_route import router as user_router
from api.routes.auth_route import router as auth_router
from api.routes.document_router import router as document_router
from dotenv import load_dotenv
from core.config.config import DEBUG, tags_metadata
from core.lifecycle import app_lifespan
from core.middleware.login_middleware import LoggingMiddleware
from fastapi_pagination import add_pagination

# Load environment variables from a .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        # logging.FileHandler("app.log"),  # Logs to a file named `app.log`
        logging.StreamHandler()  # Logs to console
    ],
)

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

# Add pagination to the app
add_pagination(app)

# Include API routes
app.include_router(general_router)
app.include_router(user_router, prefix="/api", tags=["users"])
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(document_router, prefix="/api", tags=["document"])

# Instrument the app for Prometheus
Instrumentator().instrument(app).expose(app)

print("completed app init.")
