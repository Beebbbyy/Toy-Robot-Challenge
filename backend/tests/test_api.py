"""
Comprehensive API integration tests for the Toy Robot Simulator.

This module tests all REST API endpoints with valid inputs, invalid inputs,
error responses, and CORS headers.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.robot_service import RobotService


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_robot():
    """Reset robot state before and after each test."""
    RobotService.reset_singleton()
    yield
    RobotService.reset_singleton()


class TestHealthEndpoints:
    """Tests for health check and root endpoints."""

    def test_root_endpoint(self, client):
        """Test root endpoint returns API information."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Toy Robot Simulator API"
        assert data["version"] == "1.0.0"
        assert data["status"] == "running"
        assert data["docs"] == "/docs"
        assert data["table_size"] == "5x5"

    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestPlaceEndpoint:
    """Tests for POST /api/robot/place endpoint."""

    # Valid Input Tests

    def test_place_valid_position_north(self, client):
        """Test placing robot at valid position facing NORTH."""
        response = client.post(
            "/api/robot/place",
            json={"x": 0, "y": 0, "facing": "NORTH"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["x"] == 0
        assert data["y"] == 0
        assert data["facing"] == "NORTH"
        assert data["is_placed"] is True
        assert "placed at (0, 0)" in data["message"].lower()

    def test_place_valid_position_south(self, client):
        """Test placing robot facing SOUTH."""
        response = client.post(
            "/api/robot/place",
            json={"x": 2, "y": 3, "facing": "SOUTH"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["facing"] == "SOUTH"

    def test_place_valid_position_east(self, client):
        """Test placing robot facing EAST."""
        response = client.post(
            "/api/robot/place",
            json={"x": 4, "y": 4, "facing": "EAST"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["facing"] == "EAST"

    def test_place_valid_position_west(self, client):
        """Test placing robot facing WEST."""
        response = client.post(
            "/api/robot/place",
            json={"x": 1, "y": 2, "facing": "WEST"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["facing"] == "WEST"

    def test_place_at_all_corners(self, client):
        """Test placing robot at all four corners of the table."""
        corners = [
            (0, 0), (0, 4), (4, 0), (4, 4)
        ]
        for x, y in corners:
            response = client.post(
                "/api/robot/place",
                json={"x": x, "y": y, "facing": "NORTH"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["x"] == x
            assert data["y"] == y

    def test_place_replaces_previous_position(self, client):
        """Test that placing robot again updates its position."""
        # Place first time
        client.post("/api/robot/place", json={"x": 0, "y": 0, "facing": "NORTH"})
        # Place second time
        response = client.post(
            "/api/robot/place",
            json={"x": 3, "y": 3, "facing": "SOUTH"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["x"] == 3
        assert data["y"] == 3
        assert data["facing"] == "SOUTH"

    # Invalid Input Tests

    def test_place_invalid_x_negative(self, client):
        """Test placing robot with negative x coordinate."""
        response = client.post(
            "/api/robot/place",
            json={"x": -1, "y": 0, "facing": "NORTH"}
        )
        assert response.status_code == 422
        data = response.json()
        assert "error" in data
        assert data["details"]["error_type"] == "validation_error"

    def test_place_invalid_x_too_large(self, client):
        """Test placing robot with x coordinate beyond table."""
        response = client.post(
            "/api/robot/place",
            json={"x": 5, "y": 0, "facing": "NORTH"}
        )
        assert response.status_code == 422
        data = response.json()
        assert "error" in data

    def test_place_invalid_y_negative(self, client):
        """Test placing robot with negative y coordinate."""
        response = client.post(
            "/api/robot/place",
            json={"x": 0, "y": -1, "facing": "NORTH"}
        )
        assert response.status_code == 422

    def test_place_invalid_y_too_large(self, client):
        """Test placing robot with y coordinate beyond table."""
        response = client.post(
            "/api/robot/place",
            json={"x": 0, "y": 5, "facing": "NORTH"}
        )
        assert response.status_code == 422

    def test_place_invalid_direction(self, client):
        """Test placing robot with invalid direction."""
        response = client.post(
            "/api/robot/place",
            json={"x": 0, "y": 0, "facing": "NORTHWEST"}
        )
        assert response.status_code == 422
        data = response.json()
        assert "error" in data

    def test_place_missing_x(self, client):
        """Test placing robot without x coordinate."""
        response = client.post(
            "/api/robot/place",
            json={"y": 0, "facing": "NORTH"}
        )
        assert response.status_code == 422

    def test_place_missing_y(self, client):
        """Test placing robot without y coordinate."""
        response = client.post(
            "/api/robot/place",
            json={"x": 0, "facing": "NORTH"}
        )
        assert response.status_code == 422

    def test_place_missing_facing(self, client):
        """Test placing robot without facing direction."""
        response = client.post(
            "/api/robot/place",
            json={"x": 0, "y": 0}
        )
        assert response.status_code == 422

    def test_place_invalid_data_type_x(self, client):
        """Test placing robot with string x coordinate."""
        response = client.post(
            "/api/robot/place",
            json={"x": "zero", "y": 0, "facing": "NORTH"}
        )
        assert response.status_code == 422

    def test_place_empty_body(self, client):
        """Test placing robot with empty request body."""
        response = client.post("/api/robot/place", json={})
        assert response.status_code == 422


class TestCommandEndpoint:
    """Tests for POST /api/robot/command endpoint."""

    # Valid Input Tests

    def test_command_move_valid(self, client):
        """Test MOVE command after placing robot."""
        client.post("/api/robot/place", json={"x": 0, "y": 0, "facing": "NORTH"})
        response = client.post(
            "/api/robot/command",
            json={"command": "MOVE"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["x"] == 0
        assert data["y"] == 1
        assert "moved to (0, 1)" in data["message"].lower()

    def test_command_left_valid(self, client):
        """Test LEFT command after placing robot."""
        client.post("/api/robot/place", json={"x": 0, "y": 0, "facing": "NORTH"})
        response = client.post(
            "/api/robot/command",
            json={"command": "LEFT"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["facing"] == "WEST"
        assert "rotated left" in data["message"].lower()

    def test_command_right_valid(self, client):
        """Test RIGHT command after placing robot."""
        client.post("/api/robot/place", json={"x": 0, "y": 0, "facing": "NORTH"})
        response = client.post(
            "/api/robot/command",
            json={"command": "RIGHT"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["facing"] == "EAST"
        assert "rotated right" in data["message"].lower()

    def test_command_report_valid(self, client):
        """Test REPORT command after placing robot."""
        client.post("/api/robot/place", json={"x": 2, "y": 3, "facing": "SOUTH"})
        response = client.post(
            "/api/robot/command",
            json={"command": "REPORT"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["x"] == 2
        assert data["y"] == 3
        assert data["facing"] == "SOUTH"
        assert "2,3,SOUTH" in data["message"]

    def test_command_report_not_placed(self, client):
        """Test REPORT command when robot is not placed."""
        response = client.post(
            "/api/robot/command",
            json={"command": "REPORT"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_placed"] is False
        assert "not been placed" in data["message"].lower()

    def test_command_sequence(self, client):
        """Test a sequence of commands."""
        client.post("/api/robot/place", json={"x": 1, "y": 2, "facing": "EAST"})

        # MOVE
        response = client.post("/api/robot/command", json={"command": "MOVE"})
        assert response.status_code == 200
        assert response.json()["x"] == 2

        # MOVE again
        response = client.post("/api/robot/command", json={"command": "MOVE"})
        assert response.status_code == 200
        assert response.json()["x"] == 3

        # LEFT
        response = client.post("/api/robot/command", json={"command": "LEFT"})
        assert response.status_code == 200
        assert response.json()["facing"] == "NORTH"

        # MOVE
        response = client.post("/api/robot/command", json={"command": "MOVE"})
        assert response.status_code == 200
        data = response.json()
        assert data["x"] == 3
        assert data["y"] == 3

    # Invalid Input Tests - Robot Not Placed

    def test_command_move_not_placed(self, client):
        """Test MOVE command when robot is not placed."""
        response = client.post(
            "/api/robot/command",
            json={"command": "MOVE"}
        )
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "not been placed" in data["error"].lower()
        assert data["details"]["error_type"] == "robot_not_placed"

    def test_command_left_not_placed(self, client):
        """Test LEFT command when robot is not placed."""
        response = client.post(
            "/api/robot/command",
            json={"command": "LEFT"}
        )
        assert response.status_code == 400
        data = response.json()
        assert "not been placed" in data["error"].lower()

    def test_command_right_not_placed(self, client):
        """Test RIGHT command when robot is not placed."""
        response = client.post(
            "/api/robot/command",
            json={"command": "RIGHT"}
        )
        assert response.status_code == 400

    # Invalid Input Tests - Invalid Commands

    def test_command_invalid_command(self, client):
        """Test invalid command string."""
        response = client.post(
            "/api/robot/command",
            json={"command": "JUMP"}
        )
        assert response.status_code == 422
        data = response.json()
        assert "error" in data

    def test_command_missing_command(self, client):
        """Test request without command field."""
        response = client.post("/api/robot/command", json={})
        assert response.status_code == 422

    def test_command_empty_command(self, client):
        """Test request with empty command."""
        response = client.post(
            "/api/robot/command",
            json={"command": ""}
        )
        assert response.status_code == 422

    def test_command_invalid_data_type(self, client):
        """Test command with invalid data type."""
        response = client.post(
            "/api/robot/command",
            json={"command": 123}
        )
        assert response.status_code == 422


class TestStateEndpoint:
    """Tests for GET /api/robot/state endpoint."""

    def test_state_when_placed(self, client):
        """Test getting state when robot is placed."""
        client.post("/api/robot/place", json={"x": 2, "y": 3, "facing": "EAST"})
        response = client.get("/api/robot/state")
        assert response.status_code == 200
        data = response.json()
        assert data["x"] == 2
        assert data["y"] == 3
        assert data["facing"] == "EAST"
        assert data["is_placed"] is True
        assert "at (2, 3)" in data["message"].lower()

    def test_state_when_not_placed(self, client):
        """Test getting state when robot is not placed."""
        response = client.get("/api/robot/state")
        assert response.status_code == 200
        data = response.json()
        assert data["x"] is None
        assert data["y"] is None
        assert data["facing"] is None
        assert data["is_placed"] is False
        assert "not been placed" in data["message"].lower()

    def test_state_after_movement(self, client):
        """Test state reflects changes after movement."""
        client.post("/api/robot/place", json={"x": 0, "y": 0, "facing": "NORTH"})
        client.post("/api/robot/command", json={"command": "MOVE"})
        client.post("/api/robot/command", json={"command": "RIGHT"})

        response = client.get("/api/robot/state")
        assert response.status_code == 200
        data = response.json()
        assert data["x"] == 0
        assert data["y"] == 1
        assert data["facing"] == "EAST"


class TestResetEndpoint:
    """Tests for POST /api/robot/reset endpoint."""

    def test_reset_when_placed(self, client):
        """Test resetting robot when it is placed."""
        client.post("/api/robot/place", json={"x": 2, "y": 3, "facing": "NORTH"})
        response = client.post("/api/robot/reset")
        assert response.status_code == 200
        data = response.json()
        assert data["x"] is None
        assert data["y"] is None
        assert data["facing"] is None
        assert data["is_placed"] is False
        assert "reset" in data["message"].lower()

    def test_reset_when_not_placed(self, client):
        """Test resetting robot when it is not placed."""
        response = client.post("/api/robot/reset")
        assert response.status_code == 200
        data = response.json()
        assert data["is_placed"] is False

    def test_reset_clears_state(self, client):
        """Test that reset properly clears robot state."""
        client.post("/api/robot/place", json={"x": 2, "y": 3, "facing": "NORTH"})
        client.post("/api/robot/reset")

        # Try to move without placing again should fail
        response = client.post("/api/robot/command", json={"command": "MOVE"})
        assert response.status_code == 400
        assert "not been placed" in response.json()["error"].lower()

    def test_reset_allows_new_placement(self, client):
        """Test that robot can be placed again after reset."""
        client.post("/api/robot/place", json={"x": 0, "y": 0, "facing": "NORTH"})
        client.post("/api/robot/reset")

        response = client.post("/api/robot/place", json={"x": 4, "y": 4, "facing": "SOUTH"})
        assert response.status_code == 200
        data = response.json()
        assert data["x"] == 4
        assert data["y"] == 4


class TestCORSHeaders:
    """Tests for CORS headers."""

    def test_cors_headers_on_place(self, client):
        """Test CORS headers are present on place endpoint."""
        response = client.post(
            "/api/robot/place",
            json={"x": 0, "y": 0, "facing": "NORTH"},
            headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-credentials" in response.headers

    def test_cors_headers_on_command(self, client):
        """Test CORS headers are present on command endpoint."""
        response = client.options(
            "/api/robot/command",
            headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-origin" in response.headers

    def test_cors_headers_on_state(self, client):
        """Test CORS headers are present on state endpoint."""
        response = client.options(
            "/api/robot/state",
            headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-origin" in response.headers

    def test_cors_headers_on_reset(self, client):
        """Test CORS headers are present on reset endpoint."""
        response = client.options(
            "/api/robot/reset",
            headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-origin" in response.headers

    def test_cors_allows_credentials(self, client):
        """Test CORS allows credentials."""
        response = client.get(
            "/api/robot/state",
            headers={"Origin": "http://localhost:3000"}
        )
        assert response.headers.get("access-control-allow-credentials") == "true"

    def test_cors_allowed_origin(self, client):
        """Test CORS accepts allowed origins."""
        response = client.get(
            "/api/robot/state",
            headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-origin" in response.headers


class TestErrorResponses:
    """Tests for error response formats."""

    def test_validation_error_format(self, client):
        """Test validation error response format."""
        response = client.post(
            "/api/robot/place",
            json={"x": -1, "y": 0, "facing": "NORTH"}
        )
        assert response.status_code == 422
        data = response.json()
        assert "error" in data
        assert "details" in data
        assert "path" in data
        assert data["path"] == "/api/robot/place"

    def test_robot_exception_error_format(self, client):
        """Test robot exception error format."""
        response = client.post(
            "/api/robot/command",
            json={"command": "MOVE"}
        )
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "details" in data
        assert "path" in data
        assert data["details"]["error_type"] == "robot_not_placed"

    def test_invalid_placement_error_format(self, client):
        """Test invalid placement error includes coordinates."""
        # This would require a scenario where place returns False
        # Currently Pydantic validation catches these first
        # But we can test the path is correct
        response = client.post(
            "/api/robot/place",
            json={"x": 5, "y": 5, "facing": "NORTH"}
        )
        assert response.status_code == 422
        data = response.json()
        assert "error" in data
        assert data["path"] == "/api/robot/place"


class TestComplexScenarios:
    """Tests for complex multi-step scenarios."""

    def test_example_a_via_api(self, client):
        """Test Example A: PLACE 0,0,NORTH -> MOVE -> REPORT."""
        client.post("/api/robot/place", json={"x": 0, "y": 0, "facing": "NORTH"})
        client.post("/api/robot/command", json={"command": "MOVE"})
        response = client.post("/api/robot/command", json={"command": "REPORT"})

        assert response.status_code == 200
        data = response.json()
        assert data["x"] == 0
        assert data["y"] == 1
        assert data["facing"] == "NORTH"
        assert "0,1,NORTH" in data["message"]

    def test_example_b_via_api(self, client):
        """Test Example B: PLACE 0,0,NORTH -> LEFT -> REPORT."""
        client.post("/api/robot/place", json={"x": 0, "y": 0, "facing": "NORTH"})
        client.post("/api/robot/command", json={"command": "LEFT"})
        response = client.post("/api/robot/command", json={"command": "REPORT"})

        assert response.status_code == 200
        data = response.json()
        assert data["x"] == 0
        assert data["y"] == 0
        assert data["facing"] == "WEST"
        assert "0,0,WEST" in data["message"]

    def test_example_c_via_api(self, client):
        """Test Example C: PLACE 1,2,EAST -> MOVE -> MOVE -> LEFT -> MOVE -> REPORT."""
        client.post("/api/robot/place", json={"x": 1, "y": 2, "facing": "EAST"})
        client.post("/api/robot/command", json={"command": "MOVE"})
        client.post("/api/robot/command", json={"command": "MOVE"})
        client.post("/api/robot/command", json={"command": "LEFT"})
        client.post("/api/robot/command", json={"command": "MOVE"})
        response = client.post("/api/robot/command", json={"command": "REPORT"})

        assert response.status_code == 200
        data = response.json()
        assert data["x"] == 3
        assert data["y"] == 3
        assert data["facing"] == "NORTH"
        assert "3,3,NORTH" in data["message"]

    def test_boundary_protection(self, client):
        """Test that robot doesn't fall off table."""
        # Try to walk off north edge
        client.post("/api/robot/place", json={"x": 0, "y": 4, "facing": "NORTH"})
        client.post("/api/robot/command", json={"command": "MOVE"})
        response = client.get("/api/robot/state")
        data = response.json()
        assert data["y"] == 4  # Should not change

        # Try to walk off east edge
        client.post("/api/robot/place", json={"x": 4, "y": 0, "facing": "EAST"})
        client.post("/api/robot/command", json={"command": "MOVE"})
        response = client.get("/api/robot/state")
        data = response.json()
        assert data["x"] == 4  # Should not change

    def test_full_rotation(self, client):
        """Test full 360 degree rotation."""
        client.post("/api/robot/place", json={"x": 2, "y": 2, "facing": "NORTH"})

        # Four right turns
        for _ in range(4):
            client.post("/api/robot/command", json={"command": "RIGHT"})

        response = client.get("/api/robot/state")
        data = response.json()
        assert data["facing"] == "NORTH"  # Should be back to NORTH
        assert data["x"] == 2  # Position unchanged
        assert data["y"] == 2

    def test_stateful_operations(self, client):
        """Test that robot state is maintained across requests."""
        # Place robot
        client.post("/api/robot/place", json={"x": 0, "y": 0, "facing": "NORTH"})

        # Move multiple times
        for _ in range(3):
            client.post("/api/robot/command", json={"command": "MOVE"})

        # Check state
        response = client.get("/api/robot/state")
        assert response.json()["y"] == 3

        # Rotate and move
        client.post("/api/robot/command", json={"command": "RIGHT"})
        client.post("/api/robot/command", json={"command": "MOVE"})

        # Final state check
        response = client.get("/api/robot/state")
        data = response.json()
        assert data["x"] == 1
        assert data["y"] == 3
        assert data["facing"] == "EAST"


class TestEdgeCases:
    """Tests for edge cases and corner scenarios."""

    def test_place_at_same_position_twice(self, client):
        """Test placing robot at same position twice."""
        payload = {"x": 2, "y": 2, "facing": "NORTH"}
        response1 = client.post("/api/robot/place", json=payload)
        response2 = client.post("/api/robot/place", json=payload)

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response1.json()["x"] == response2.json()["x"]

    def test_multiple_reports(self, client):
        """Test multiple REPORT commands return consistent results."""
        client.post("/api/robot/place", json={"x": 1, "y": 1, "facing": "SOUTH"})

        response1 = client.post("/api/robot/command", json={"command": "REPORT"})
        response2 = client.post("/api/robot/command", json={"command": "REPORT"})

        assert response1.json() == response2.json()

    def test_move_at_all_edges(self, client):
        """Test moving at all four edges of the table."""
        edges = [
            (0, 2, "WEST"),   # West edge
            (4, 2, "EAST"),   # East edge
            (2, 0, "SOUTH"),  # South edge
            (2, 4, "NORTH"),  # North edge
        ]

        for x, y, facing in edges:
            client.post("/api/robot/reset")
            client.post("/api/robot/place", json={"x": x, "y": y, "facing": facing})
            client.post("/api/robot/command", json={"command": "MOVE"})

            response = client.get("/api/robot/state")
            data = response.json()
            # Position should not change when trying to move off edge
            assert data["x"] == x
            assert data["y"] == y

    def test_rapid_rotation(self, client):
        """Test rapid rotation doesn't affect position."""
        client.post("/api/robot/place", json={"x": 2, "y": 2, "facing": "NORTH"})

        # Rotate many times
        for _ in range(10):
            client.post("/api/robot/command", json={"command": "LEFT"})

        response = client.get("/api/robot/state")
        data = response.json()
        # Position should remain unchanged
        assert data["x"] == 2
        assert data["y"] == 2
        # After 10 left turns from NORTH: 10 % 4 = 2 left turns = SOUTH
        assert data["facing"] == "SOUTH"
