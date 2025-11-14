"""
Middleware components for the Toy Robot Simulator API.

This module provides logging and request tracking middleware.
"""
import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("robot_api")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP requests and responses.

    Logs request details, response status, and execution time.
    """

    def __init__(self, app: ASGIApp):
        """
        Initialize the middleware.

        Args:
            app: The ASGI application
        """
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and log details.

        Args:
            request: The incoming request
            call_next: The next middleware or route handler

        Returns:
            The response from the application
        """
        # Record start time
        start_time = time.time()

        # Extract request details
        method = request.method
        url = str(request.url)
        client_host = request.client.host if request.client else "unknown"

        # Log incoming request
        logger.info(
            f"Incoming request: {method} {url} from {client_host}",
            extra={
                "method": method,
                "url": url,
                "client": client_host,
                "headers": dict(request.headers),
            },
        )

        # Process request
        try:
            response = await call_next(request)

            # Calculate execution time
            execution_time = time.time() - start_time

            # Log response
            logger.info(
                f"Request completed: {method} {url} - Status: {response.status_code} - Time: {execution_time:.3f}s",
                extra={
                    "method": method,
                    "url": url,
                    "status_code": response.status_code,
                    "execution_time": execution_time,
                },
            )

            # Add custom headers for debugging
            response.headers["X-Process-Time"] = str(execution_time)

            return response

        except Exception as e:
            # Log errors
            execution_time = time.time() - start_time
            logger.error(
                f"Request failed: {method} {url} - Error: {str(e)} - Time: {execution_time:.3f}s",
                extra={
                    "method": method,
                    "url": url,
                    "error": str(e),
                    "execution_time": execution_time,
                },
                exc_info=True,
            )
            raise


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware for adding unique request IDs to each request.

    Useful for tracking requests across logs and debugging.
    """

    def __init__(self, app: ASGIApp):
        """
        Initialize the middleware.

        Args:
            app: The ASGI application
        """
        super().__init__(app)
        self._request_counter = 0

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Add request ID to the request and response.

        Args:
            request: The incoming request
            call_next: The next middleware or route handler

        Returns:
            The response with added request ID header
        """
        # Generate request ID
        self._request_counter += 1
        request_id = f"{int(time.time())}-{self._request_counter}"

        # Add to request state for access in routes
        request.state.request_id = request_id

        # Process request
        response = await call_next(request)

        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id

        return response
