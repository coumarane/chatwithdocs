from contextlib import asynccontextmanager

resource = {}

@asynccontextmanager
async def app_lifespan(app):
    print("init lifespan")
    resource["msg"] = "Hello World!"
    yield
    resource.clear()
    print("clean up lifespan")
