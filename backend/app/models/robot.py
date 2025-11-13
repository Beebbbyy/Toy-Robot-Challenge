"""
Robot model for the Toy Robot Simulator.
"""
from typing import Optional, Literal


Direction = Literal['NORTH', 'SOUTH', 'EAST', 'WEST']


class Robot:
    """
    Represents a toy robot on a 5x5 tabletop.

    The robot can be placed at any position with a facing direction,
    and can move, rotate, and report its position.
    """

    def __init__(self):
        """Initialize a robot with no position."""
        self.x: Optional[int] = None
        self.y: Optional[int] = None
        self.facing: Optional[Direction] = None

    def place(self, x: int, y: int, facing: Direction) -> bool:
        """
        Place the robot on the tabletop.

        Args:
            x: X coordinate (0-4)
            y: Y coordinate (0-4)
            facing: Direction the robot should face

        Returns:
            True if placement successful, False otherwise
        """
        if 0 <= x <= 4 and 0 <= y <= 4 and facing in ('NORTH', 'SOUTH', 'EAST', 'WEST'):
            self.x = x
            self.y = y
            self.facing = facing
            return True
        return False

    def is_placed(self) -> bool:
        """
        Check if the robot has been placed on the tabletop.

        Returns:
            True if robot is placed, False otherwise
        """
        return self.x is not None and self.y is not None and self.facing is not None

    def move(self) -> None:
        """
        Move the robot one unit forward in the direction it's facing.

        The robot will not move if it would fall off the table.
        """
        if not self.is_placed():
            return

        if self.facing == 'NORTH':
            self.y = min(self.y + 1, 4)
        elif self.facing == 'SOUTH':
            self.y = max(self.y - 1, 0)
        elif self.facing == 'EAST':
            self.x = min(self.x + 1, 4)
        elif self.facing == 'WEST':
            self.x = max(self.x - 1, 0)

    def left(self) -> None:
        """Rotate the robot 90 degrees to the left (counter-clockwise)."""
        if not self.is_placed():
            return

        directions = ['NORTH', 'EAST', 'SOUTH', 'WEST']
        self.facing = directions[(directions.index(self.facing) - 1) % 4]

    def right(self) -> None:
        """Rotate the robot 90 degrees to the right (clockwise)."""
        if not self.is_placed():
            return

        directions = ['NORTH', 'EAST', 'SOUTH', 'WEST']
        self.facing = directions[(directions.index(self.facing) + 1) % 4]

    def report(self) -> Optional[str]:
        """
        Get the current position and facing direction.

        Returns:
            String in format "X,Y,FACING" if placed, None otherwise
        """
        if self.is_placed():
            return f"{self.x},{self.y},{self.facing}"
        return None

    def to_dict(self) -> dict:
        """
        Convert robot state to dictionary for JSON serialization.

        Returns:
            Dictionary containing robot's position and facing direction
        """
        return {
            "x": self.x,
            "y": self.y,
            "facing": self.facing,
            "is_placed": self.is_placed()
        }
