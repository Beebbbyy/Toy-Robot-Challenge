"""
RobotService - Business logic layer for robot operations.

This service implements the singleton pattern to maintain a single robot instance
throughout the application lifecycle.
"""
from typing import Optional
from ..models.robot import Robot, Direction


class RobotService:
    """
    Service class for managing robot operations.

    Implements the singleton pattern to ensure only one robot instance exists.
    Provides methods for command execution, state retrieval, and reset functionality.
    """

    _instance: Optional['RobotService'] = None
    _robot: Optional[Robot] = None

    def __new__(cls) -> 'RobotService':
        """
        Implement singleton pattern.

        Returns:
            The single RobotService instance
        """
        if cls._instance is None:
            cls._instance = super(RobotService, cls).__new__(cls)
            cls._robot = Robot()
        return cls._instance

    def __init__(self):
        """Initialize the service (no-op for singleton)."""
        pass

    # Command Execution Methods

    def place(self, x: int, y: int, facing: Direction) -> bool:
        """
        Place the robot on the tabletop at the specified position.

        Args:
            x: X coordinate (0-4)
            y: Y coordinate (0-4)
            facing: Direction the robot should face (NORTH, SOUTH, EAST, WEST)

        Returns:
            True if placement was successful, False otherwise
        """
        return self._robot.place(x, y, facing)

    def move(self) -> None:
        """
        Move the robot one unit forward in the direction it's facing.

        The robot will not move if it would fall off the table or if not placed.
        """
        self._robot.move()

    def left(self) -> None:
        """
        Rotate the robot 90 degrees to the left (counter-clockwise).

        Only executes if the robot has been placed.
        """
        self._robot.left()

    def right(self) -> None:
        """
        Rotate the robot 90 degrees to the right (clockwise).

        Only executes if the robot has been placed.
        """
        self._robot.right()

    def execute_command(self, command: str) -> Optional[str]:
        """
        Execute a robot command by name.

        Args:
            command: Command string (MOVE, LEFT, RIGHT, REPORT)

        Returns:
            Report string if command is REPORT, None otherwise

        Raises:
            ValueError: If command is not recognized
        """
        command = command.upper()

        if command == 'MOVE':
            self.move()
            return None
        elif command == 'LEFT':
            self.left()
            return None
        elif command == 'RIGHT':
            self.right()
            return None
        elif command == 'REPORT':
            return self.report()
        else:
            raise ValueError(f"Unknown command: {command}")

    # State Retrieval Methods

    def report(self) -> Optional[str]:
        """
        Get the current position and facing direction of the robot.

        Returns:
            String in format "X,Y,FACING" if robot is placed, None otherwise
        """
        return self._robot.report()

    def get_state(self) -> dict:
        """
        Get the complete state of the robot as a dictionary.

        Returns:
            Dictionary containing x, y, facing, and is_placed status
        """
        return self._robot.to_dict()

    def is_placed(self) -> bool:
        """
        Check if the robot has been placed on the tabletop.

        Returns:
            True if robot is placed, False otherwise
        """
        return self._robot.is_placed()

    def get_position(self) -> Optional[tuple[int, int]]:
        """
        Get the current position coordinates.

        Returns:
            Tuple of (x, y) coordinates if placed, None otherwise
        """
        if self._robot.is_placed():
            return (self._robot.x, self._robot.y)
        return None

    def get_facing(self) -> Optional[Direction]:
        """
        Get the current facing direction.

        Returns:
            Direction string if placed, None otherwise
        """
        return self._robot.facing

    # Reset Functionality

    def reset(self) -> None:
        """
        Reset the robot to its initial state (not placed).

        This removes the robot from the tabletop and clears its position and direction.
        """
        self._robot.x = None
        self._robot.y = None
        self._robot.facing = None

    @classmethod
    def reset_singleton(cls) -> None:
        """
        Reset the singleton instance (primarily for testing).

        This creates a new robot instance, clearing all state.
        """
        if cls._instance is not None:
            cls._robot = Robot()

    @classmethod
    def get_instance(cls) -> 'RobotService':
        """
        Get the singleton instance of RobotService.

        Returns:
            The RobotService instance
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
