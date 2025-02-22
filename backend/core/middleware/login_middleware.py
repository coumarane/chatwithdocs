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
        # Skip logging for excluded paths
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)

        # Extract request details safely
        client_ip = request.client.host if request.client else "-"
        method = request.method
        path = request.url.path
        http_version = request.scope.get("http_version", "1.1")

        # Process the request and get the response
        response = await call_next(request)

        # Log with the actual status code
        self.logger.info(
            '%s - "%s %s HTTP/%s" %s',
            client_ip,
            method,
            path,
            http_version,
            response.status_code
        )

        return response
