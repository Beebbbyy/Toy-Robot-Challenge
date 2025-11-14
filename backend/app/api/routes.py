"""
API routes for the Toy Robot Simulator.

This module defines all REST API endpoints for controlling the robot.
"""
from fastapi import APIRouter, HTTPException, status
from typing import Optional

from ..models.requests import PlaceRequest, CommandRequest, RobotStateResponse
from ..services.robot_service import RobotService
from ..exceptions import (
    RobotNotPlacedException,
    InvalidPlacementException,
    InvalidCommandException,
)

# Create API router
router = APIRouter(prefix="/robot", tags=["robot"])

# Get singleton robot service instance
robot_service = RobotService.get_instance()


@router.post(
    "/place",
    response_model=RobotStateResponse,
    status_code=status.HTTP_200_OK,
    summary="Place the robot on the table",
    description="Place the robot at specific coordinates (0-4, 0-4) facing a direction (NORTH, SOUTH, EAST, WEST)",
)
async def place_robot(request: PlaceRequest) -> RobotStateResponse:
    """
    Place the robot on the tabletop at the specified position.

    Args:
        request: PlaceRequest containing x, y coordinates and facing direction

    Returns:
        RobotStateResponse with the robot's current state

    Raises:
        InvalidPlacementException: If the placement coordinates are invalid
    """
    success = robot_service.place(request.x, request.y, request.facing)

    if not success:
        raise InvalidPlacementException(
            message=f"Cannot place robot at position ({request.x}, {request.y}) facing {request.facing}",
            x=request.x,
            y=request.y,
        )

    state = robot_service.get_state()
    return RobotStateResponse(
        x=state["x"],
        y=state["y"],
        facing=state["facing"],
        is_placed=state["is_placed"],
        message=f"Robot placed at ({request.x}, {request.y}) facing {request.facing}",
    )


@router.post(
    "/command",
    response_model=RobotStateResponse,
    status_code=status.HTTP_200_OK,
    summary="Execute a robot command",
    description="Execute a command: MOVE (forward one unit), LEFT (rotate 90° left), RIGHT (rotate 90° right), or REPORT (get position)",
)
async def execute_command(request: CommandRequest) -> RobotStateResponse:
    """
    Execute a robot command (MOVE, LEFT, RIGHT, REPORT).

    Args:
        request: CommandRequest containing the command to execute

    Returns:
        RobotStateResponse with the robot's current state

    Raises:
        RobotNotPlacedException: If robot hasn't been placed yet
        InvalidCommandException: If command is invalid
    """
    # Check if robot is placed (except for REPORT which can return "not placed" state)
    if request.command != "REPORT" and not robot_service.is_placed():
        raise RobotNotPlacedException()

    try:
        # Execute the command
        report_output = robot_service.execute_command(request.command)

        # Get current state
        state = robot_service.get_state()

        # Build response message
        if request.command == "REPORT":
            if report_output:
                message = f"Report: {report_output}"
            else:
                message = "Robot has not been placed on the table"
        elif request.command == "MOVE":
            message = f"Robot moved to ({state['x']}, {state['y']})"
        elif request.command in ["LEFT", "RIGHT"]:
            message = f"Robot rotated {request.command.lower()}, now facing {state['facing']}"
        else:
            message = f"Command {request.command} executed"

        return RobotStateResponse(
            x=state["x"],
            y=state["y"],
            facing=state["facing"],
            is_placed=state["is_placed"],
            message=message,
        )

    except ValueError as e:
        raise InvalidCommandException(
            command=request.command,
            message=str(e),
        )


@router.get(
    "/state",
    response_model=RobotStateResponse,
    status_code=status.HTTP_200_OK,
    summary="Get robot state",
    description="Get the current state of the robot (position, facing direction, placement status)",
)
async def get_robot_state() -> RobotStateResponse:
    """
    Get the current state of the robot.

    Returns:
        RobotStateResponse with the robot's current state
    """
    state = robot_service.get_state()

    if state["is_placed"]:
        message = f"Robot is at ({state['x']}, {state['y']}) facing {state['facing']}"
    else:
        message = "Robot has not been placed on the table"

    return RobotStateResponse(
        x=state["x"],
        y=state["y"],
        facing=state["facing"],
        is_placed=state["is_placed"],
        message=message,
    )


@router.post(
    "/reset",
    response_model=RobotStateResponse,
    status_code=status.HTTP_200_OK,
    summary="Reset the robot",
    description="Reset the robot to its initial state (removes it from the table)",
)
async def reset_robot() -> RobotStateResponse:
    """
    Reset the robot to its initial state.

    Removes the robot from the tabletop and clears its position and direction.

    Returns:
        RobotStateResponse with the reset state
    """
    robot_service.reset()
    state = robot_service.get_state()

    return RobotStateResponse(
        x=state["x"],
        y=state["y"],
        facing=state["facing"],
        is_placed=state["is_placed"],
        message="Robot has been reset",
    )
