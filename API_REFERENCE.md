# API Reference - Toy Robot Simulator

Quick reference guide for the Toy Robot Simulator REST API.

**Base URL:** `http://localhost:8000`
**API Version:** 1.0
**Content-Type:** `application/json`

---

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/robot/place` | Place robot on the grid |
| POST | `/api/robot/command` | Execute a command |
| GET | `/api/robot/state` | Get current robot state |
| POST | `/api/robot/reset` | Reset robot to initial state |

---

## 1. Place Robot

Place the robot on the 5x5 grid at specified coordinates and direction.

### Request

```http
POST /api/robot/place
Content-Type: application/json

{
  "x": 2,
  "y": 3,
  "facing": "NORTH"
}
```

### Parameters

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `x` | integer | Yes | 0-4 | X coordinate on grid |
| `y` | integer | Yes | 0-4 | Y coordinate on grid |
| `facing` | string | Yes | NORTH, SOUTH, EAST, WEST | Direction robot faces |

### Success Response

```http
HTTP/1.1 200 OK
Content-Type: application/json

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

### Error Responses

**Invalid Coordinates:**
```http
HTTP/1.1 400 Bad Request

{
  "success": false,
  "error": "Invalid placement: coordinates out of bounds"
}
```

**Invalid Direction:**
```http
HTTP/1.1 422 Unprocessable Entity

{
  "detail": [
    {
      "loc": ["body", "facing"],
      "msg": "unexpected value; permitted: 'NORTH', 'SOUTH', 'EAST', 'WEST'",
      "type": "value_error.const"
    }
  ]
}
```

### Example Usage

**JavaScript (Fetch API):**
```javascript
const placeRobot = async (x, y, facing) => {
  const response = await fetch('http://localhost:8000/api/robot/place', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ x, y, facing })
  });
  return await response.json();
};

// Usage
const result = await placeRobot(2, 3, 'NORTH');
console.log(result);
```

**cURL:**
```bash
curl -X POST http://localhost:8000/api/robot/place \
  -H "Content-Type: application/json" \
  -d '{"x": 2, "y": 3, "facing": "NORTH"}'
```

---

## 2. Execute Command

Execute a robot command (MOVE, LEFT, RIGHT, REPORT).

### Request

```http
POST /api/robot/command
Content-Type: application/json

{
  "command": "MOVE"
}
```

### Parameters

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `command` | string | Yes | MOVE, LEFT, RIGHT, REPORT | Command to execute |

### Command Descriptions

- **MOVE**: Move robot one unit forward in current direction
- **LEFT**: Rotate robot 90° counter-clockwise
- **RIGHT**: Rotate robot 90° clockwise
- **REPORT**: Return current position (no state change)

### Success Response

```http
HTTP/1.1 200 OK
Content-Type: application/json

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

### Error Responses

**Robot Not Placed:**
```http
HTTP/1.1 400 Bad Request

{
  "success": false,
  "error": "Robot not placed. Use PLACE command first."
}
```

**Invalid Command:**
```http
HTTP/1.1 422 Unprocessable Entity

{
  "detail": [
    {
      "loc": ["body", "command"],
      "msg": "unexpected value; permitted: 'MOVE', 'LEFT', 'RIGHT', 'REPORT'",
      "type": "value_error.const"
    }
  ]
}
```

### Example Usage

**JavaScript:**
```javascript
const executeCommand = async (command) => {
  const response = await fetch('http://localhost:8000/api/robot/command', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ command })
  });
  return await response.json();
};

// Usage
await executeCommand('MOVE');
await executeCommand('LEFT');
await executeCommand('RIGHT');
const state = await executeCommand('REPORT');
```

**cURL:**
```bash
# Move
curl -X POST http://localhost:8000/api/robot/command \
  -H "Content-Type: application/json" \
  -d '{"command": "MOVE"}'

# Turn left
curl -X POST http://localhost:8000/api/robot/command \
  -H "Content-Type: application/json" \
  -d '{"command": "LEFT"}'
```

---

## 3. Get Robot State

Retrieve current robot state without executing any command.

### Request

```http
GET /api/robot/state
```

### Parameters

None

### Success Response

**Robot Placed:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

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

**Robot Not Placed:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "data": {
    "x": null,
    "y": null,
    "facing": null,
    "placed": false
  }
}
```

### Example Usage

**JavaScript:**
```javascript
const getRobotState = async () => {
  const response = await fetch('http://localhost:8000/api/robot/state');
  return await response.json();
};

// Usage
const state = await getRobotState();
console.log(`Robot at ${state.data.x}, ${state.data.y} facing ${state.data.facing}`);
```

**cURL:**
```bash
curl http://localhost:8000/api/robot/state
```

---

## 4. Reset Robot

Reset the robot to initial state (remove from table).

### Request

```http
POST /api/robot/reset
```

### Parameters

None

### Success Response

```http
HTTP/1.1 200 OK
Content-Type: application/json

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

### Example Usage

**JavaScript:**
```javascript
const resetRobot = async () => {
  const response = await fetch('http://localhost:8000/api/robot/reset', {
    method: 'POST'
  });
  return await response.json();
};

// Usage
await resetRobot();
```

**cURL:**
```bash
curl -X POST http://localhost:8000/api/robot/reset
```

---

## Response Schema

### Standard Response Object

All successful API responses follow this structure:

```typescript
{
  success: boolean,        // Always true for successful responses
  data: RobotState,       // Robot state object
  message?: string        // Optional message (for mutations)
}
```

### RobotState Object

```typescript
{
  x: number | null,       // X coordinate (0-4) or null if not placed
  y: number | null,       // Y coordinate (0-4) or null if not placed
  facing: string | null,  // "NORTH" | "SOUTH" | "EAST" | "WEST" | null
  placed: boolean         // Whether robot is on the table
}
```

### Error Response Object

```typescript
{
  success: false,
  error: string,          // Human-readable error message
  code?: string          // Optional error code
}
```

---

## Complete Usage Example

Here's a complete example workflow:

```javascript
// 1. Place robot at origin facing north
const placeResult = await fetch('http://localhost:8000/api/robot/place', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ x: 0, y: 0, facing: 'NORTH' })
});
console.log(await placeResult.json());
// { success: true, data: { x: 0, y: 0, facing: "NORTH", placed: true }, ... }

// 2. Move forward
const moveResult = await fetch('http://localhost:8000/api/robot/command', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ command: 'MOVE' })
});
console.log(await moveResult.json());
// { success: true, data: { x: 0, y: 1, facing: "NORTH", placed: true }, ... }

// 3. Turn right (now facing east)
const rightResult = await fetch('http://localhost:8000/api/robot/command', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ command: 'RIGHT' })
});
console.log(await rightResult.json());
// { success: true, data: { x: 0, y: 1, facing: "EAST", placed: true }, ... }

// 4. Move forward (now at 1, 1)
await fetch('http://localhost:8000/api/robot/command', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ command: 'MOVE' })
});

// 5. Get current state
const stateResult = await fetch('http://localhost:8000/api/robot/state');
console.log(await stateResult.json());
// { success: true, data: { x: 1, y: 1, facing: "EAST", placed: true } }

// 6. Reset robot
const resetResult = await fetch('http://localhost:8000/api/robot/reset', {
  method: 'POST'
});
console.log(await resetResult.json());
// { success: true, data: { x: null, y: null, facing: null, placed: false }, ... }
```

---

## Grid Coordinate System

The 5x5 grid uses the following coordinate system:

```
y
4  [ ][ ][ ][ ][ ]
3  [ ][ ][ ][ ][ ]
2  [ ][ ][ ][ ][ ]
1  [ ][ ][ ][ ][ ]
0  [ ][ ][ ][ ][ ]
   0  1  2  3  4   x

- Origin (0,0) is at the SOUTH-WEST corner
- X increases EAST (right)
- Y increases NORTH (up)
- Valid coordinates: x ∈ [0,4], y ∈ [0,4]
```

### Direction Reference

- **NORTH**: Increases Y (+1)
- **SOUTH**: Decreases Y (-1)
- **EAST**: Increases X (+1)
- **WEST**: Decreases X (-1)

### Rotation Reference

Starting from **NORTH**:
- **LEFT** rotation: NORTH → WEST → SOUTH → EAST → NORTH
- **RIGHT** rotation: NORTH → EAST → SOUTH → WEST → NORTH

---

## Error Codes

| HTTP Status | Meaning | Common Causes |
|-------------|---------|---------------|
| 200 | Success | Request completed successfully |
| 400 | Bad Request | Robot not placed, invalid placement |
| 422 | Unprocessable Entity | Invalid request format, validation error |
| 500 | Internal Server Error | Server-side error |

---

## CORS Configuration

The API supports CORS for development:

**Allowed Origins:** `http://localhost:3000`, `http://localhost:8080`, `http://127.0.0.1:3000`
**Allowed Methods:** `GET`, `POST`, `OPTIONS`
**Allowed Headers:** `Content-Type`, `Authorization`

For production, configure specific allowed origins.

---

## Testing the API

### Using Swagger UI

Visit `http://localhost:8000/docs` for interactive API documentation.

### Using ReDoc

Visit `http://localhost:8000/redoc` for alternative API documentation.

### Using cURL (Full Test Sequence)

```bash
# 1. Place robot
curl -X POST http://localhost:8000/api/robot/place \
  -H "Content-Type: application/json" \
  -d '{"x": 1, "y": 2, "facing": "EAST"}'

# 2. Move
curl -X POST http://localhost:8000/api/robot/command \
  -H "Content-Type: application/json" \
  -d '{"command": "MOVE"}'

# 3. Turn left
curl -X POST http://localhost:8000/api/robot/command \
  -H "Content-Type: application/json" \
  -d '{"command": "LEFT"}'

# 4. Report current state
curl -X POST http://localhost:8000/api/robot/command \
  -H "Content-Type: application/json" \
  -d '{"command": "REPORT"}'

# 5. Get state
curl http://localhost:8000/api/robot/state

# 6. Reset
curl -X POST http://localhost:8000/api/robot/reset
```

---

## Rate Limiting

Currently no rate limiting is implemented. Consider adding rate limiting for production deployments.

---

## Changelog

### Version 1.0 (Initial Design)
- Initial API design
- Four core endpoints
- JSON request/response format
- Pydantic validation
- CORS support

---

**For implementation details, see:** `ARCHITECTURE.md`
**For implementation roadmap, see:** `IMPLEMENTATION_ROADMAP.md`
