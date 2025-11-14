"""
Configuration settings for the Toy Robot Simulator API
"""
import os
from typing import List


class Settings:
    """Application settings and configuration"""

    # API Settings
    API_V1_PREFIX: str = "/api"
    PROJECT_NAME: str = "Toy Robot Simulator API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = """
    REST API for the Toy Robot Simulator.

    Control a toy robot on a 5x5 grid table using simple commands:
    - PLACE: Position the robot at specific coordinates
    - MOVE: Move the robot one unit forward
    - LEFT: Rotate the robot 90 degrees left
    - RIGHT: Rotate the robot 90 degrees right
    - REPORT: Get the current position and facing direction
    """

    # CORS Settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5500",  # VS Code Live Server
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5500",  # VS Code Live Server
        "http://127.0.0.1:8080",
    ]

    # Table Settings
    TABLE_WIDTH: int = 5
    TABLE_HEIGHT: int = 5

    # Development Settings
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    @classmethod
    def get_allowed_origins(cls) -> List[str]:
        """
        Get allowed CORS origins from environment variable or use defaults.

        Checks the ALLOWED_ORIGINS environment variable for a comma-separated
        list of origins. If not set, returns the default allowed origins.

        Returns:
            List of allowed origin URLs for CORS
        """
        env_origins = os.getenv("ALLOWED_ORIGINS")
        if env_origins:
            return [origin.strip() for origin in env_origins.split(",")]
        return cls.ALLOWED_ORIGINS


settings = Settings()
