"""
Comprehensive unit tests for Robot model and RobotService.

This module tests the core robot functionality including placement, movement,
rotation, and state management.
"""
import pytest
from app.models.robot import Robot, Direction
from app.services.robot_service import RobotService


class TestRobotModel:
    """Unit tests for the Robot model."""

    def setup_method(self):
        """Set up a fresh robot instance for each test."""
        self.robot = Robot()

    # Placement Tests

    def test_robot_initial_state(self):
        """Test robot starts with no position."""
        assert self.robot.x is None
        assert self.robot.y is None
        assert self.robot.facing is None
        assert not self.robot.is_placed()

    def test_place_valid_position_north(self):
        """Test placing robot at valid position facing NORTH."""
        result = self.robot.place(0, 0, "NORTH")
        assert result is True
        assert self.robot.x == 0
        assert self.robot.y == 0
        assert self.robot.facing == "NORTH"
        assert self.robot.is_placed()

    def test_place_valid_position_south(self):
        """Test placing robot at valid position facing SOUTH."""
        result = self.robot.place(2, 3, "SOUTH")
        assert result is True
        assert self.robot.x == 2
        assert self.robot.y == 3
        assert self.robot.facing == "SOUTH"

    def test_place_valid_position_east(self):
        """Test placing robot at valid position facing EAST."""
        result = self.robot.place(4, 4, "EAST")
        assert result is True
        assert self.robot.x == 4
        assert self.robot.y == 4
        assert self.robot.facing == "EAST"

    def test_place_valid_position_west(self):
        """Test placing robot at valid position facing WEST."""
        result = self.robot.place(1, 2, "WEST")
        assert result is True
        assert self.robot.x == 1
        assert self.robot.y == 2
        assert self.robot.facing == "WEST"

    def test_place_invalid_x_negative(self):
        """Test placing robot with negative x coordinate."""
        result = self.robot.place(-1, 0, "NORTH")
        assert result is False
        assert not self.robot.is_placed()

    def test_place_invalid_x_too_large(self):
        """Test placing robot with x coordinate beyond table."""
        result = self.robot.place(5, 0, "NORTH")
        assert result is False
        assert not self.robot.is_placed()

    def test_place_invalid_y_negative(self):
        """Test placing robot with negative y coordinate."""
        result = self.robot.place(0, -1, "NORTH")
        assert result is False
        assert not self.robot.is_placed()

    def test_place_invalid_y_too_large(self):
        """Test placing robot with y coordinate beyond table."""
        result = self.robot.place(0, 5, "NORTH")
        assert result is False
        assert not self.robot.is_placed()

    def test_place_invalid_direction(self):
        """Test placing robot with invalid direction."""
        result = self.robot.place(0, 0, "NORTHWEST")
        assert result is False
        assert not self.robot.is_placed()

    def test_place_replaces_previous_position(self):
        """Test that placing robot again updates its position."""
        self.robot.place(0, 0, "NORTH")
        self.robot.place(3, 3, "SOUTH")
        assert self.robot.x == 3
        assert self.robot.y == 3
        assert self.robot.facing == "SOUTH"

    # Movement Tests

    def test_move_north_from_center(self):
        """Test moving north from center of table."""
        self.robot.place(2, 2, "NORTH")
        self.robot.move()
        assert self.robot.x == 2
        assert self.robot.y == 3

    def test_move_south_from_center(self):
        """Test moving south from center of table."""
        self.robot.place(2, 2, "SOUTH")
        self.robot.move()
        assert self.robot.x == 2
        assert self.robot.y == 1

    def test_move_east_from_center(self):
        """Test moving east from center of table."""
        self.robot.place(2, 2, "EAST")
        self.robot.move()
        assert self.robot.x == 3
        assert self.robot.y == 2

    def test_move_west_from_center(self):
        """Test moving west from center of table."""
        self.robot.place(2, 2, "WEST")
        self.robot.move()
        assert self.robot.x == 1
        assert self.robot.y == 2

    def test_move_north_at_edge(self):
        """Test moving north when at north edge (should not move)."""
        self.robot.place(2, 4, "NORTH")
        self.robot.move()
        assert self.robot.x == 2
        assert self.robot.y == 4  # Should not change

    def test_move_south_at_edge(self):
        """Test moving south when at south edge (should not move)."""
        self.robot.place(2, 0, "SOUTH")
        self.robot.move()
        assert self.robot.x == 2
        assert self.robot.y == 0  # Should not change

    def test_move_east_at_edge(self):
        """Test moving east when at east edge (should not move)."""
        self.robot.place(4, 2, "EAST")
        self.robot.move()
        assert self.robot.x == 4  # Should not change
        assert self.robot.y == 2

    def test_move_west_at_edge(self):
        """Test moving west when at west edge (should not move)."""
        self.robot.place(0, 2, "WEST")
        self.robot.move()
        assert self.robot.x == 0  # Should not change
        assert self.robot.y == 2

    def test_move_when_not_placed(self):
        """Test that move does nothing when robot is not placed."""
        self.robot.move()
        assert not self.robot.is_placed()

    def test_multiple_moves(self):
        """Test multiple consecutive moves."""
        self.robot.place(0, 0, "NORTH")
        self.robot.move()
        self.robot.move()
        self.robot.move()
        assert self.robot.x == 0
        assert self.robot.y == 3

    # Rotation Tests - LEFT

    def test_left_from_north(self):
        """Test rotating left from NORTH."""
        self.robot.place(0, 0, "NORTH")
        self.robot.left()
        assert self.robot.facing == "WEST"

    def test_left_from_west(self):
        """Test rotating left from WEST."""
        self.robot.place(0, 0, "WEST")
        self.robot.left()
        assert self.robot.facing == "SOUTH"

    def test_left_from_south(self):
        """Test rotating left from SOUTH."""
        self.robot.place(0, 0, "SOUTH")
        self.robot.left()
        assert self.robot.facing == "EAST"

    def test_left_from_east(self):
        """Test rotating left from EAST."""
        self.robot.place(0, 0, "EAST")
        self.robot.left()
        assert self.robot.facing == "NORTH"

    def test_left_full_rotation(self):
        """Test that four left rotations return to original direction."""
        self.robot.place(0, 0, "NORTH")
        self.robot.left()
        self.robot.left()
        self.robot.left()
        self.robot.left()
        assert self.robot.facing == "NORTH"

    def test_left_when_not_placed(self):
        """Test that left does nothing when robot is not placed."""
        self.robot.left()
        assert not self.robot.is_placed()

    # Rotation Tests - RIGHT

    def test_right_from_north(self):
        """Test rotating right from NORTH."""
        self.robot.place(0, 0, "NORTH")
        self.robot.right()
        assert self.robot.facing == "EAST"

    def test_right_from_east(self):
        """Test rotating right from EAST."""
        self.robot.place(0, 0, "EAST")
        self.robot.right()
        assert self.robot.facing == "SOUTH"

    def test_right_from_south(self):
        """Test rotating right from SOUTH."""
        self.robot.place(0, 0, "SOUTH")
        self.robot.right()
        assert self.robot.facing == "WEST"

    def test_right_from_west(self):
        """Test rotating right from WEST."""
        self.robot.place(0, 0, "WEST")
        self.robot.right()
        assert self.robot.facing == "NORTH"

    def test_right_full_rotation(self):
        """Test that four right rotations return to original direction."""
        self.robot.place(0, 0, "NORTH")
        self.robot.right()
        self.robot.right()
        self.robot.right()
        self.robot.right()
        assert self.robot.facing == "NORTH"

    def test_right_when_not_placed(self):
        """Test that right does nothing when robot is not placed."""
        self.robot.right()
        assert not self.robot.is_placed()

    # Report Tests

    def test_report_when_placed(self):
        """Test report returns correct format when robot is placed."""
        self.robot.place(1, 2, "EAST")
        report = self.robot.report()
        assert report == "1,2,EAST"

    def test_report_when_not_placed(self):
        """Test report returns None when robot is not placed."""
        report = self.robot.report()
        assert report is None

    def test_report_after_movement(self):
        """Test report reflects position after movement."""
        self.robot.place(0, 0, "NORTH")
        self.robot.move()
        self.robot.right()
        self.robot.move()
        report = self.robot.report()
        assert report == "1,1,EAST"

    # to_dict Tests

    def test_to_dict_when_placed(self):
        """Test to_dict returns correct dictionary when placed."""
        self.robot.place(2, 3, "SOUTH")
        state = self.robot.to_dict()
        assert state == {
            "x": 2,
            "y": 3,
            "facing": "SOUTH",
            "is_placed": True
        }

    def test_to_dict_when_not_placed(self):
        """Test to_dict returns correct dictionary when not placed."""
        state = self.robot.to_dict()
        assert state == {
            "x": None,
            "y": None,
            "facing": None,
            "is_placed": False
        }

    # Complex Scenario Tests

    def test_example_a(self):
        """Test Example A from requirements: PLACE 0,0,NORTH -> MOVE -> REPORT."""
        self.robot.place(0, 0, "NORTH")
        self.robot.move()
        assert self.robot.report() == "0,1,NORTH"

    def test_example_b(self):
        """Test Example B: PLACE 0,0,NORTH -> LEFT -> REPORT."""
        self.robot.place(0, 0, "NORTH")
        self.robot.left()
        assert self.robot.report() == "0,0,WEST"

    def test_example_c(self):
        """Test Example C: PLACE 1,2,EAST -> MOVE -> MOVE -> LEFT -> MOVE -> REPORT."""
        self.robot.place(1, 2, "EAST")
        self.robot.move()
        self.robot.move()
        self.robot.left()
        self.robot.move()
        assert self.robot.report() == "3,3,NORTH"

    def test_corner_to_corner_navigation(self):
        """Test navigating from one corner to another."""
        self.robot.place(0, 0, "EAST")
        # Move to east edge
        for _ in range(4):
            self.robot.move()
        self.robot.left()  # Now facing NORTH
        # Move to north edge
        for _ in range(4):
            self.robot.move()
        assert self.robot.report() == "4,4,NORTH"


class TestRobotService:
    """Unit tests for the RobotService singleton."""

    def setup_method(self):
        """Reset the singleton before each test."""
        RobotService.reset_singleton()
        self.service = RobotService()

    def teardown_method(self):
        """Clean up after each test."""
        RobotService.reset_singleton()

    # Singleton Tests

    def test_singleton_pattern(self):
        """Test that RobotService implements singleton pattern."""
        service1 = RobotService()
        service2 = RobotService()
        assert service1 is service2

    def test_get_instance(self):
        """Test get_instance returns the singleton instance."""
        instance = RobotService.get_instance()
        assert instance is self.service

    # Place Tests

    def test_service_place_valid(self):
        """Test placing robot through service."""
        result = self.service.place(1, 2, "NORTH")
        assert result is True
        assert self.service.is_placed()

    def test_service_place_invalid(self):
        """Test placing robot at invalid position through service."""
        result = self.service.place(5, 5, "NORTH")
        assert result is False
        assert not self.service.is_placed()

    # Movement Command Tests

    def test_service_move(self):
        """Test move command through service."""
        self.service.place(0, 0, "NORTH")
        self.service.move()
        state = self.service.get_state()
        assert state["x"] == 0
        assert state["y"] == 1

    def test_service_left(self):
        """Test left rotation through service."""
        self.service.place(0, 0, "NORTH")
        self.service.left()
        state = self.service.get_state()
        assert state["facing"] == "WEST"

    def test_service_right(self):
        """Test right rotation through service."""
        self.service.place(0, 0, "NORTH")
        self.service.right()
        state = self.service.get_state()
        assert state["facing"] == "EAST"

    # Execute Command Tests

    def test_execute_command_move(self):
        """Test executing MOVE command."""
        self.service.place(0, 0, "NORTH")
        result = self.service.execute_command("MOVE")
        assert result is None
        assert self.service.get_position() == (0, 1)

    def test_execute_command_left(self):
        """Test executing LEFT command."""
        self.service.place(0, 0, "NORTH")
        result = self.service.execute_command("LEFT")
        assert result is None
        assert self.service.get_facing() == "WEST"

    def test_execute_command_right(self):
        """Test executing RIGHT command."""
        self.service.place(0, 0, "NORTH")
        result = self.service.execute_command("RIGHT")
        assert result is None
        assert self.service.get_facing() == "EAST"

    def test_execute_command_report(self):
        """Test executing REPORT command."""
        self.service.place(2, 3, "SOUTH")
        result = self.service.execute_command("REPORT")
        assert result == "2,3,SOUTH"

    def test_execute_command_case_insensitive(self):
        """Test that commands are case insensitive."""
        self.service.place(0, 0, "NORTH")
        result = self.service.execute_command("move")
        assert result is None
        assert self.service.get_position() == (0, 1)

    def test_execute_command_invalid(self):
        """Test executing invalid command raises ValueError."""
        self.service.place(0, 0, "NORTH")
        with pytest.raises(ValueError, match="Unknown command"):
            self.service.execute_command("JUMP")

    # State Retrieval Tests

    def test_get_state_when_placed(self):
        """Test get_state returns correct state when placed."""
        self.service.place(2, 3, "EAST")
        state = self.service.get_state()
        assert state == {
            "x": 2,
            "y": 3,
            "facing": "EAST",
            "is_placed": True
        }

    def test_get_state_when_not_placed(self):
        """Test get_state returns correct state when not placed."""
        state = self.service.get_state()
        assert state == {
            "x": None,
            "y": None,
            "facing": None,
            "is_placed": False
        }

    def test_report_when_placed(self):
        """Test report through service when placed."""
        self.service.place(1, 2, "WEST")
        report = self.service.report()
        assert report == "1,2,WEST"

    def test_report_when_not_placed(self):
        """Test report through service when not placed."""
        report = self.service.report()
        assert report is None

    def test_is_placed(self):
        """Test is_placed method."""
        assert not self.service.is_placed()
        self.service.place(0, 0, "NORTH")
        assert self.service.is_placed()

    def test_get_position_when_placed(self):
        """Test get_position returns tuple when placed."""
        self.service.place(3, 4, "SOUTH")
        position = self.service.get_position()
        assert position == (3, 4)

    def test_get_position_when_not_placed(self):
        """Test get_position returns None when not placed."""
        position = self.service.get_position()
        assert position is None

    def test_get_facing_when_placed(self):
        """Test get_facing returns direction when placed."""
        self.service.place(0, 0, "WEST")
        facing = self.service.get_facing()
        assert facing == "WEST"

    def test_get_facing_when_not_placed(self):
        """Test get_facing returns None when not placed."""
        facing = self.service.get_facing()
        assert facing is None

    # Reset Tests

    def test_reset(self):
        """Test reset removes robot from table."""
        self.service.place(2, 2, "NORTH")
        assert self.service.is_placed()
        self.service.reset()
        assert not self.service.is_placed()
        state = self.service.get_state()
        assert state["x"] is None
        assert state["y"] is None
        assert state["facing"] is None

    def test_reset_singleton(self):
        """Test reset_singleton creates new robot instance."""
        self.service.place(2, 2, "NORTH")
        RobotService.reset_singleton()
        # Should have new robot instance
        state = self.service.get_state()
        assert not state["is_placed"]

    # Complex Scenario Tests

    def test_service_example_a(self):
        """Test service with Example A scenario."""
        self.service.place(0, 0, "NORTH")
        self.service.execute_command("MOVE")
        report = self.service.execute_command("REPORT")
        assert report == "0,1,NORTH"

    def test_service_example_b(self):
        """Test service with Example B scenario."""
        self.service.place(0, 0, "NORTH")
        self.service.execute_command("LEFT")
        report = self.service.execute_command("REPORT")
        assert report == "0,0,WEST"

    def test_service_example_c(self):
        """Test service with Example C scenario."""
        self.service.place(1, 2, "EAST")
        self.service.execute_command("MOVE")
        self.service.execute_command("MOVE")
        self.service.execute_command("LEFT")
        self.service.execute_command("MOVE")
        report = self.service.execute_command("REPORT")
        assert report == "3,3,NORTH"

    def test_state_persistence_across_operations(self):
        """Test that state persists correctly across multiple operations."""
        self.service.place(0, 0, "NORTH")
        self.service.move()
        state1 = self.service.get_state()
        self.service.right()
        state2 = self.service.get_state()
        # Position should remain same
        assert state2["x"] == state1["x"]
        assert state2["y"] == state1["y"]
        # Direction should change
        assert state2["facing"] == "EAST"
