"""
Custom exceptions for the Toy Robot Simulator API.
"""
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from typing import Any, Dict, Optional


class RobotException(Exception):
    """Base exception for robot-related errors."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize robot exception.

        Args:
            message: Error message
            status_code: HTTP status code
            details: Additional error details
        """
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class RobotNotPlacedException(RobotException):
    """Exception raised when attempting to command an unplaced robot."""

    def __init__(self, message: str = "Robot has not been placed on the table yet"):
        """
        Initialize RobotNotPlacedException.

        Args:
            message: Custom error message
        """
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"error_type": "robot_not_placed"},
        )


class InvalidPlacementException(RobotException):
    """Exception raised when placement coordinates are invalid."""

    def __init__(
        self,
        message: str = "Invalid placement coordinates",
        x: Optional[int] = None,
        y: Optional[int] = None,
    ):
        """
        Initialize InvalidPlacementException.

        Args:
            message: Custom error message
            x: X coordinate that failed
            y: Y coordinate that failed
        """
        details = {"error_type": "invalid_placement"}
        if x is not None:
            details["x"] = x
        if y is not None:
            details["y"] = y

        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details,
        )


class InvalidCommandException(RobotException):
    """Exception raised when command is invalid or unknown."""

    def __init__(self, command: str, message: Optional[str] = None):
        """
        Initialize InvalidCommandException.

        Args:
            command: The invalid command
            message: Custom error message
        """
        if message is None:
            message = f"Invalid or unknown command: {command}"

        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"error_type": "invalid_command", "command": command},
        )


# Exception handlers


async def robot_exception_handler(request: Request, exc: RobotException) -> JSONResponse:
    """
    Handle RobotException and its subclasses.

    Args:
        request: The request that caused the exception
        exc: The exception instance

    Returns:
        JSON response with error details
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "details": exc.details,
            "path": str(request.url.path),
        },
    )


async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle validation errors from Pydantic.

    Args:
        request: The request that caused the exception
        exc: The exception instance

    Returns:
        JSON response with validation error details
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation error",
            "details": {"error_type": "validation_error", "message": str(exc)},
            "path": str(request.url.path),
        },
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle unexpected errors.

    Args:
        request: The request that caused the exception
        exc: The exception instance

    Returns:
        JSON response with generic error message
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "details": {
                "error_type": "internal_error",
                "message": "An unexpected error occurred",
            },
            "path": str(request.url.path),
        },
    )
