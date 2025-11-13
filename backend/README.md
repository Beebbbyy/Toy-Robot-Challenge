# Toy Robot Simulator - Backend API

FastAPI-based REST API for the Toy Robot Simulator.

## Overview

This backend provides a RESTful API for controlling a toy robot on a 5x5 grid table. It maintains the core business logic from the original CLI application while exposing it through HTTP endpoints.

## Technology Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - ASGI server for running FastAPI applications
- **Pydantic** - Data validation using Python type annotations
- **pytest** - Testing framework

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration settings
│   ├── models/
│   │   ├── __init__.py
│   │   ├── robot.py            # Robot class (core business logic)
│   │   └── requests.py         # Pydantic request/response models
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # API endpoint definitions
│   └── services/
│       ├── __init__.py
│       └── robot_service.py    # Business logic layer
├── tests/
│   ├── __init__.py
│   ├── test_robot.py           # Unit tests for Robot class
│   └── test_api.py             # API integration tests
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

### Development Mode

Run the server with auto-reload enabled:

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at: `http://localhost:8000`

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:

- **Swagger UI** (interactive docs): http://localhost:8000/docs
- **ReDoc** (alternative docs): http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### POST /api/robot/place
Place the robot on the table at specified coordinates.

**Request:**
```json
{
  "x": 0,
  "y": 0,
  "facing": "NORTH"
}
```

### POST /api/robot/command
Execute a robot command (MOVE, LEFT, RIGHT, REPORT).

**Request:**
```json
{
  "command": "MOVE"
}
```

### GET /api/robot/state
Get the current robot state without executing a command.

### POST /api/robot/reset
Reset the robot (remove from table).

## Testing

Run all tests:
```bash
pytest tests/ -v
```

Run tests with coverage:
```bash
pytest tests/ -v --cov=app --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_robot.py -v
pytest tests/test_api.py -v
```

## Development

### Adding New Endpoints

1. Define the endpoint in `app/api/routes.py`
2. Add any new Pydantic models to `app/models/requests.py`
3. Implement business logic in `app/services/robot_service.py`
4. Write tests in `tests/test_api.py`

### Code Quality

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write docstrings for public methods
- Maintain test coverage above 90%

## CORS Configuration

By default, CORS is configured for development to allow requests from `http://localhost:3000` (frontend). Update `app/main.py` for production deployment.

## Environment Variables

- `ALLOWED_ORIGINS` - Comma-separated list of allowed CORS origins
- `PORT` - Server port (default: 8000)

## Troubleshooting

### ImportError: No module named 'app'
Make sure you're running uvicorn from the `backend/` directory.

### CORS Errors
Check that the frontend origin is included in the CORS configuration in `app/main.py`.

## License

See main project README.
