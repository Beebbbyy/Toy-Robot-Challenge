"""
Pydantic models for API requests and responses.
"""
from typing import Optional, Literal
from pydantic import BaseModel, Field, validator


Direction = Literal['NORTH', 'SOUTH', 'EAST', 'WEST']
Command = Literal['MOVE', 'LEFT', 'RIGHT', 'REPORT']


class PlaceRequest(BaseModel):
    """Request model for placing the robot on the tabletop."""

    x: int = Field(..., ge=0, le=4, description="X coordinate on the 5x5 grid (0-4)")
    y: int = Field(..., ge=0, le=4, description="Y coordinate on the 5x5 grid (0-4)")
    facing: Direction = Field(..., description="Direction the robot should face")

    class Config:
        json_schema_extra = {
            "example": {
                "x": 0,
                "y": 0,
                "facing": "NORTH"
            }
        }


class CommandRequest(BaseModel):
    """Request model for robot commands (MOVE, LEFT, RIGHT, REPORT)."""

    command: Command = Field(..., description="Command to execute")

    class Config:
        json_schema_extra = {
            "example": {
                "command": "MOVE"
            }
        }


class RobotStateResponse(BaseModel):
    """Response model for robot state."""

    x: Optional[int] = Field(None, description="Current X coordinate (null if not placed)")
    y: Optional[int] = Field(None, description="Current Y coordinate (null if not placed)")
    facing: Optional[Direction] = Field(None, description="Current facing direction (null if not placed)")
    is_placed: bool = Field(..., description="Whether the robot has been placed on the table")
    message: Optional[str] = Field(None, description="Optional message about the operation")

    class Config:
        json_schema_extra = {
            "example": {
                "x": 2,
                "y": 3,
                "facing": "NORTH",
                "is_placed": True,
                "message": "Robot placed successfully"
            }
        }
