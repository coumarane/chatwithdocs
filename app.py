import os
import sys
from typing import Union
from fastapi import FastAPI, Request, BackgroundTasks, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager


DEBUG = os.environ.get("DEBUG", "").strip().lower() in {
    "1", "true", "on", "yes"}

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

resource = {}


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    print("init lifespan")
    resource["msg"] = "Hello World!"
    yield
    resource.clear()
    print("clean up lifespan")

app = FastAPI(
    debug=DEBUG,
    title="ChatWithDocs Web Service",
    description="This project is a production ready ChatWithDocs Web Service"
    "<br /><br />"
    "Author - [***Coumarane COUPPANE***](https://www.linkedin.com/https://www.linkedin.com/in/coumarane-couppane-712a2415/)",
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/swagger/",
    lifespan=app_lifespan,
)

templates = Jinja2Templates(directory="src/templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/test")
def get_test():
    return {"Hello": "World"}


print("completed app init.")
