# Toy Robot Challenge - Architecture Design Document

## Phase 1: Architecture & Design

**Date:** 2025-11-12
**Version:** 1.0
**Backend Choice:** Option A - REST API with FastAPI
**Frontend Choice:** Option A - Vanilla JavaScript + HTML/CSS

---

## 1. Overview

This document outlines the architecture for transforming the Toy Robot CLI simulator into a full-stack web application. The application will maintain the core robot simulation logic while providing a modern web interface for user interaction.

### 1.1 Project Goals
- Create an interactive web-based UI for the Toy Robot Simulator
- Provide a RESTful API backend for robot commands
- Maintain existing business logic and test coverage
- Enable real-time visual feedback of robot position on a 5x5 grid
- Support all existing commands: PLACE, MOVE, LEFT, RIGHT, REPORT

---

## 2. Technology Stack

### 2.1 Backend
- **Framework:** FastAPI (Python 3.8+)
- **ASGI Server:** Uvicorn
- **CORS:** FastAPI CORS middleware
- **Testing:** pytest, pytest-asyncio
- **Validation:** Pydantic models

**Rationale for FastAPI:**
- Built-in async support for scalability
- Automatic API documentation (Swagger/OpenAPI)
- Fast performance with minimal overhead
- Native Pydantic integration for data validation
- Excellent developer experience with type hints

### 2.2 Frontend
- **Core:** Vanilla JavaScript (ES6+)
- **Styling:** CSS3 with CSS Grid/Flexbox
- **HTTP Client:** Fetch API
- **Build:** No build step required (pure vanilla)

**Rationale for Vanilla JS:**
- Zero dependencies and build complexity
- Lightweight and fast load times
- Direct DOM manipulation for simple UI
- Educational clarity
- No framework overhead

### 2.3 Development Tools
- **Version Control:** Git
- **Testing:** unittest (backend core logic), pytest (API tests)
- **API Documentation:** Auto-generated via FastAPI (Swagger UI)

---

## 3. System Architecture

### 3.1 High-Level Architecture

```
┌─────────────────────────────────────────────┐
│           Web Browser (Client)              │
│  ┌───────────────────────────────────────┐  │
│  │   HTML/CSS/JavaScript Frontend        │  │
│  │   - Interactive 5x5 Grid Display      │  │
│  │   - Command Buttons (UI Controls)     │  │
│  │   - Status Display                    │  │
│  └───────────────┬───────────────────────┘  │
└──────────────────┼─────────────────────────┘
                   │ HTTP/JSON
                   │ (REST API)
┌──────────────────▼─────────────────────────┐
│         FastAPI Backend Server             │
│  ┌───────────────────────────────────────┐ │
│  │   REST API Layer                      │ │
│  │   - Command Endpoints                 │ │
│  │   - State Management                  │ │
│  │   - Request Validation                │ │
│  └───────────────┬───────────────────────┘ │
│  ┌───────────────▼───────────────────────┐ │
│  │   Business Logic Layer                │ │
│  │   - Robot Class (existing)            │ │
│  │   - Table Class (modified)            │ │
│  │   - Command Processing                │ │
│  └───────────────────────────────────────┘ │
└────────────────────────────────────────────┘
```

### 3.2 Communication Flow

1. User interacts with frontend UI (clicks button or enters command)
2. JavaScript sends HTTP request to FastAPI backend
3. FastAPI validates request via Pydantic models
4. Backend executes robot command via existing Robot class
5. Backend returns updated state as JSON
6. Frontend updates visual grid and displays status

---

## 4. Backend Architecture

### 4.1 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   ├── robot.py            # Migrated Robot class
│   │   └── requests.py         # Pydantic request models
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # API endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   └── robot_service.py    # Business logic layer
│   └── config.py               # Configuration settings
├── tests/
│   ├── __init__.py
│   ├── test_robot.py           # Migrated unit tests
│   └── test_api.py             # API integration tests
├── requirements.txt
└── README.md
```

### 4.2 Core Components

#### 4.2.1 Robot Model (`app/models/robot.py`)
- Migrate existing `Robot` class from `robot.py`
- Add `to_dict()` method for JSON serialization
- Maintain all existing methods: `place()`, `move()`, `left()`, `right()`, `report()`

#### 4.2.2 Request Models (`app/models/requests.py`)
Pydantic models for request validation:
```python
class PlaceRequest(BaseModel):
    x: int = Field(ge=0, le=4)
    y: int = Field(ge=0, le=4)
    facing: Literal["NORTH", "SOUTH", "EAST", "WEST"]

class CommandRequest(BaseModel):
    command: Literal["MOVE", "LEFT", "RIGHT", "REPORT"]
```

#### 4.2.3 Robot Service (`app/services/robot_service.py`)
- Singleton pattern to maintain robot state during session
- Session management (future: support multiple robot instances)
- Command execution and state retrieval

### 4.3 API Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST | `/api/robot/place` | Place robot on grid | `PlaceRequest` | Robot state |
| POST | `/api/robot/command` | Execute command | `CommandRequest` | Robot state |
| GET | `/api/robot/state` | Get current state | - | Robot state |
| POST | `/api/robot/reset` | Reset robot | - | Success message |

#### 4.3.1 Response Format

**Success Response:**
```json
{
  "success": true,
  "data": {
    "x": 2,
    "y": 3,
    "facing": "NORTH",
    "placed": true
  },
  "message": "Command executed successfully"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Invalid placement: coordinates out of bounds",
  "code": "INVALID_PLACEMENT"
}
```

### 4.4 Error Handling

- **Validation Errors:** Handled by Pydantic (422 status)
- **Business Logic Errors:** Custom exceptions with appropriate HTTP status codes
- **Robot Not Placed:** 400 Bad Request with descriptive message
- **Invalid Commands:** 400 Bad Request

---

## 5. Frontend Architecture

### 5.1 Project Structure

```
frontend/
├── index.html              # Main HTML page
├── css/
│   ├── styles.css          # Main stylesheet
│   └── grid.css            # Grid-specific styles
├── js/
│   ├── app.js              # Application initialization
│   ├── api.js              # API communication layer
│   ├── grid.js             # Grid rendering logic
│   ├── controls.js         # UI controls and event handlers
│   └── state.js            # Frontend state management
└── assets/
    └── robot.svg           # Robot icon (optional)
```

### 5.2 Core Components

#### 5.2.1 Grid Display (`grid.js`)
- Renders 5x5 grid using CSS Grid
- Visual representation of robot position
- Direction indicator (arrow/emoji)
- Cell highlighting on hover

#### 5.2.2 API Client (`api.js`)
- Wrapper around Fetch API
- Centralized endpoint configuration
- Error handling and response parsing
- Request/response logging (dev mode)

#### 5.2.3 Controls (`controls.js`)
- Button controls for: PLACE, MOVE, LEFT, RIGHT, REPORT
- Input fields for PLACE command (x, y, direction)
- Keyboard shortcuts (optional enhancement)
- Command history display

#### 5.2.4 State Management (`state.js`)
- Simple reactive state object
- State change listeners
- Synchronization with backend state
- Local state for UI-specific data (e.g., command history)

### 5.3 UI Layout

```
┌────────────────────────────────────────────────┐
│              Toy Robot Simulator               │
├────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐   │
│  │                  │  │  Control Panel   │   │
│  │   5x5 Grid       │  │                  │   │
│  │   Display        │  │  [PLACE]         │   │
│  │                  │  │  X: [_] Y: [_]   │   │
│  │     🤖           │  │  Dir: [▼]        │   │
│  │                  │  │                  │   │
│  │                  │  │  [MOVE]          │   │
│  │                  │  │  [LEFT] [RIGHT]  │   │
│  │                  │  │  [REPORT]        │   │
│  └──────────────────┘  │  [RESET]         │   │
│                        │                  │   │
│  Status: 2, 3, NORTH   │  Command History │   │
│                        │  > PLACE 0,0,N   │   │
│                        │  > MOVE          │   │
│                        └──────────────────┘   │
└────────────────────────────────────────────────┘
```

### 5.4 Visual Design Requirements

- **Responsive:** Works on desktop and tablet (mobile-friendly)
- **Accessibility:** Proper ARIA labels, keyboard navigation
- **Visual Feedback:** Hover states, active states, disabled states
- **Error Display:** Clear error messages for invalid commands
- **Grid Styling:**
  - Clear cell boundaries
  - Robot representation (emoji or SVG)
  - Direction indicator (arrow)
  - Coordinate labels (0-4 on axes)

---

## 6. Data Models

### 6.1 Robot State Model

```python
{
    "x": int | None,         # X coordinate (0-4)
    "y": int | None,         # Y coordinate (0-4)
    "facing": str | None,    # "NORTH" | "SOUTH" | "EAST" | "WEST"
    "placed": bool           # Whether robot has been placed
}
```

### 6.2 Command Models

**PLACE Command:**
```python
{
    "x": int,        # 0-4
    "y": int,        # 0-4
    "facing": str    # "NORTH" | "SOUTH" | "EAST" | "WEST"
}
```

**Other Commands:**
```python
{
    "command": str   # "MOVE" | "LEFT" | "RIGHT" | "REPORT"
}
```

---

## 7. API Specification

### 7.1 POST /api/robot/place

Place the robot on the table at specified coordinates and direction.

**Request:**
```json
{
  "x": 2,
  "y": 3,
  "facing": "NORTH"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "x": 2,
    "y": 3,
    "facing": "NORTH",
    "placed": true
  },
  "message": "Robot placed successfully"
}
```

**Error Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "Invalid placement: coordinates out of bounds"
}
```

### 7.2 POST /api/robot/command

Execute a robot command (MOVE, LEFT, RIGHT, REPORT).

**Request:**
```json
{
  "command": "MOVE"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "x": 2,
    "y": 4,
    "facing": "NORTH",
    "placed": true
  },
  "message": "Move successful"
}
```

**Error Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "Robot not placed. Use PLACE command first."
}
```

### 7.3 GET /api/robot/state

Get current robot state without executing a command.

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "x": 2,
    "y": 4,
    "facing": "NORTH",
    "placed": true
  }
}
```

### 7.4 POST /api/robot/reset

Reset the robot state (remove from table).

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "x": null,
    "y": null,
    "facing": null,
    "placed": false
  },
  "message": "Robot reset successfully"
}
```

---

## 8. Security Considerations

### 8.1 CORS Configuration
- Allow requests from frontend origin
- Configure appropriate headers
- Restrict in production to specific domains

### 8.2 Input Validation
- All inputs validated via Pydantic models
- Type checking and range validation
- Sanitization of error messages

### 8.3 Rate Limiting (Future)
- Consider rate limiting for API endpoints
- Prevent abuse and ensure fair usage

---

## 9. Testing Strategy

### 9.1 Backend Testing

**Unit Tests:**
- Test Robot class methods (existing tests migrated)
- Test boundary conditions (grid edges)
- Test invalid inputs and error handling

**API Integration Tests:**
- Test all endpoints with valid requests
- Test error responses
- Test state persistence across requests
- Test CORS headers

**Coverage Goal:** 90%+ code coverage

### 9.2 Frontend Testing

**Manual Testing:**
- All UI controls functional
- Grid updates correctly
- Error messages display properly
- Responsive design works across devices

**Future Automation:**
- Consider Playwright/Cypress for E2E tests

---

## 10. Deployment Considerations

### 10.1 Development Environment
- Backend: `uvicorn app.main:app --reload --port 8000`
- Frontend: Serve via Python HTTP server or any static server
- CORS configured for localhost

### 10.2 Production Deployment Options

**Backend:**
- Docker container with Uvicorn
- Deploy to: Heroku, Railway, Render, AWS, Google Cloud
- Environment variables for configuration

**Frontend:**
- Static hosting: GitHub Pages, Netlify, Vercel
- CDN for asset delivery
- Minification and optimization

---

## 11. Future Enhancements (Post-MVP)

### 11.1 Session Management
- Support multiple robot instances per user
- Persistent state across browser refreshes
- User authentication (optional)

### 11.2 Advanced Features
- Command queue/batch execution
- Animation for robot movements
- Multiple robots on same grid
- Obstacles and advanced grid features
- Save/load robot scenarios
- WebSocket support for real-time updates

### 11.3 Developer Experience
- Docker Compose for easy local setup
- CI/CD pipeline (GitHub Actions)
- Automated testing on PR
- API versioning

---

## 12. Implementation Phases

### Phase 1: Architecture & Design ✓
- Define technology stack
- Design API endpoints
- Plan project structure
- Document architecture

### Phase 2: Backend Development
- Set up FastAPI project
- Migrate Robot class
- Implement API endpoints
- Add Pydantic models
- Write API tests
- Set up CORS

### Phase 3: Frontend Development
- Create HTML structure
- Implement CSS grid layout
- Build API client
- Implement UI controls
- Add state management
- Connect to backend API

### Phase 4: Integration & Testing
- End-to-end testing
- Bug fixes and refinements
- Cross-browser testing
- Performance optimization

### Phase 5: Documentation & Deployment
- API documentation
- User guide
- Deployment setup
- README updates

---

## 13. Development Timeline Estimate

| Phase | Estimated Duration |
|-------|-------------------|
| Phase 1: Architecture | 0.5 day (Complete) |
| Phase 2: Backend | 1-2 days |
| Phase 3: Frontend | 1-2 days |
| Phase 4: Integration & Testing | 1 day |
| Phase 5: Documentation & Deployment | 0.5 day |
| **Total** | **4-6 days** |

---

## 14. Success Criteria

- ✅ All existing robot functionality preserved
- ✅ All existing tests pass
- ✅ API endpoints respond correctly
- ✅ Frontend displays robot state accurately
- ✅ All commands executable via UI
- ✅ Responsive design works on multiple devices
- ✅ Error handling provides clear feedback
- ✅ API documentation auto-generated and accurate

---

## 15. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| CORS issues in development | Medium | Proper CORS middleware configuration |
| State synchronization bugs | High | Comprehensive API tests, clear state management |
| Browser compatibility | Low | Use standard web APIs, test on major browsers |
| Performance with animations | Low | Keep animations simple, use CSS transforms |

---

## Appendix A: File Migration Plan

### Files to Migrate/Modify
- `robot.py` → Split into `backend/app/models/robot.py` (Robot class) and `backend/app/services/robot_service.py`
- `test_robot.py` → Migrate to `backend/tests/test_robot.py`
- `README.md` → Update with new setup instructions

### New Files to Create
- `backend/app/main.py` - FastAPI application
- `backend/app/api/routes.py` - API endpoints
- `backend/app/models/requests.py` - Pydantic models
- `backend/requirements.txt` - Python dependencies
- `frontend/index.html` - Main HTML
- `frontend/js/*.js` - JavaScript modules
- `frontend/css/*.css` - Stylesheets

---

## Appendix B: Dependencies

### Backend (`requirements.txt`)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.1  # for testing
```

### Frontend
No external dependencies (Vanilla JS)

---

**Document End**

*This architecture is designed to be simple, maintainable, and scalable while preserving the existing robot logic and adding a modern web interface.*
