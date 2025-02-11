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

        # Process the request and get the response
        response = await call_next(request)

        # If status code is 422, log the response body
        if response.status_code == 422:
            response_body = b"".join([chunk async for chunk in response.body_iterator])
            self.logger.info(f"Response Body: {response_body.decode('utf-8')}")

            # We need to restore the response body iterator
            response.body_iterator = iter([response_body])  # Restore response body iterator

        # Log response status
        self.logger.info(f"Response status: {response.status_code}")

        return response

