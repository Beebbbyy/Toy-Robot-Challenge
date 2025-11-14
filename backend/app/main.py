"""
Toy Robot Simulator - FastAPI Application

Main application entry point for the Toy Robot Simulator REST API.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from app.config import settings
from app.api import routes
from app.middleware import RequestLoggingMiddleware, RequestIDMiddleware
from app.exceptions import (
    RobotException,
    robot_exception_handler,
    validation_exception_handler,
    general_exception_handler,
)


# Create FastAPI application instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)


# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware for logging and request tracking
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RequestIDMiddleware)


# Register exception handlers
app.add_exception_handler(RobotException, robot_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


@app.get("/")
async def root():
    """
    Root endpoint - API health check and information
    """
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "running",
        "docs": "/docs",
        "table_size": f"{settings.TABLE_WIDTH}x{settings.TABLE_HEIGHT}",
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {"status": "healthy"}


# Include API routes
app.include_router(routes.router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
