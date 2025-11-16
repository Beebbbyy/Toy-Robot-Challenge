/**
 * Robot Module - Robot State Management
 * Manages the robot state and position on the frontend
 */

/**
 * Robot state
 */
export const robotState = {
    x: null,
    y: null,
    facing: null,
    isPlaced: false,
    previousX: null,
    previousY: null,
};

/**
 * Update the robot state
 * @param {number|null} x - X coordinate (0-4)
 * @param {number|null} y - Y coordinate (0-4)
 * @param {string|null} facing - Direction (NORTH, EAST, SOUTH, WEST)
 */
export function updateRobotState(x, y, facing) {
    // Store previous position for animation
    robotState.previousX = robotState.x;
    robotState.previousY = robotState.y;

    // Update current position
    robotState.x = x;
    robotState.y = y;
    robotState.facing = facing;
    robotState.isPlaced = x !== null && y !== null && facing !== null;

    // Trigger animation if position changed
    if (robotState.previousX !== null && robotState.previousY !== null &&
        (robotState.previousX !== x || robotState.previousY !== y)) {
        // Import and call animation function
        import('./grid.js').then(module => {
            if (module.animateRobotMovement) {
                module.animateRobotMovement(robotState.previousX, robotState.previousY, x, y);
            }
        });
    }
}

/**
 * Reset the robot state
 */
export function resetRobotState() {
    updateRobotState(null, null, null);
}

/**
 * Get the current robot position as a string
 * @returns {string} Position string (e.g., "0,0,NORTH" or "Not placed")
 */
export function getRobotPositionString() {
    if (!robotState.isPlaced) {
        return 'Not placed';
    }
    return `${robotState.x},${robotState.y},${robotState.facing}`;
}

/**
 * Get the robot direction string
 * @returns {string} Direction or "-"
 */
export function getRobotDirectionString() {
    return robotState.facing || '-';
}

/**
 * Validate if coordinates are within table bounds
 * @param {number} x - X coordinate
 * @param {number} y - Y coordinate
 * @returns {boolean} True if valid
 */
export function isValidPosition(x, y) {
    return x >= 0 && x <= 4 && y >= 0 && y <= 4;
}

/**
 * Validate if direction is valid
 * @param {string} facing - Direction
 * @returns {boolean} True if valid
 */
export function isValidDirection(facing) {
    const validDirections = ['NORTH', 'EAST', 'SOUTH', 'WEST'];
    return validDirections.includes(facing.toUpperCase());
}

/**
 * Parse robot state from API response
 * @param {Object} apiResponse - Response from the API
 * @returns {Object} Parsed robot state
 */
export function parseRobotState(apiResponse) {
    if (apiResponse.placed && apiResponse.position) {
        const { x, y, facing } = apiResponse.position;
        return { x, y, facing, isPlaced: true };
    }
    return { x: null, y: null, facing: null, isPlaced: false };
}

/**
 * Get the grid index from coordinates
 * The grid is displayed with (0,0) at bottom-left, but DOM renders top-left first
 * @param {number} x - X coordinate
 * @param {number} y - Y coordinate
 * @returns {number} Grid cell index
 */
export function getGridIndex(x, y) {
    // Convert from bottom-left origin to top-left origin
    const gridY = 4 - y;
    return gridY * 5 + x;
}

/**
 * Get coordinates from grid index
 * @param {number} index - Grid cell index
 * @returns {Object} Coordinates {x, y}
 */
export function getCoordinatesFromIndex(index) {
    const x = index % 5;
    const gridY = Math.floor(index / 5);
    const y = 4 - gridY; // Convert back to bottom-left origin
    return { x, y };
}
