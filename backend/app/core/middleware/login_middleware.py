import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, log_level: int = logging.INFO, exclude_paths: list = None):
        super().__init__(app)
        self.logger = logging.getLogger("uvicorn.access")
        self.logger.setLevel(log_level)
        self.exclude_paths = exclude_paths or []

    async def dispatch(self, request: Request, call_next):
        # Log request details
        self.logger.info(f"Request: {request.method} {request.url}")
        self.logger.info(f"Headers: {dict(request.headers)}")
        body = await request.body()
        if body:
            self.logger.info(f"Body: {body.decode('utf-8')}")

        # Process the request
        response = await call_next(request)

        # Log response details
        self.logger.info(f"Response status: {response.status_code}")
        if response.status_code == 422:  # Log additional details for 422 errors
            response_body = b"".join([chunk async for chunk in response.body_iterator])
            self.logger.info(f"Response Body: {response_body.decode('utf-8')}")
            response.body_iterator = iter([response_body])  # Restore response body iterator

        return response

