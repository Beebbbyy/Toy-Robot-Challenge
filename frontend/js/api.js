/**
 * API Module - Backend Communication
 * Handles all HTTP requests to the backend API
 */

// API Configuration
const API_BASE_URL = 'http://localhost:8000/api/robot';
const HEALTH_URL = 'http://localhost:8000/health';

/**
 * Parse a PLACE command string
 * @param {string} command - Command string like "PLACE 0,0,NORTH"
 * @returns {Object|null} Parsed place data or null if invalid
 */
function parsePlaceCommand(command) {
    const placeMatch = command.match(/^PLACE\s+(\d+),(\d+),(NORTH|EAST|SOUTH|WEST)$/i);
    if (placeMatch) {
        return {
            x: parseInt(placeMatch[1], 10),
            y: parseInt(placeMatch[2], 10),
            facing: placeMatch[3].toUpperCase(),
        };
    }
    return null;
}

/**
 * Send a command to the robot
 * @param {string} command - The command to execute (e.g., 'PLACE 0,0,NORTH', 'MOVE', 'LEFT', 'RIGHT', 'REPORT')
 * @returns {Promise<Object>} Response from the server
 */
export async function sendCommand(command) {
    const trimmedCommand = command.trim().toUpperCase();

    try {
        // Check if it's a PLACE command
        if (trimmedCommand.startsWith('PLACE')) {
            const placeData = parsePlaceCommand(trimmedCommand);
            if (!placeData) {
                throw new Error('Invalid PLACE command format. Use: PLACE X,Y,F (e.g., PLACE 0,0,NORTH)');
            }

            const response = await fetch(`${API_BASE_URL}/place`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(placeData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || errorData.message || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return {
                success: true,
                placed: data.is_placed,
                position: data.is_placed ? { x: data.x, y: data.y, facing: data.facing } : null,
                message: data.message,
            };
        } else {
            // Handle MOVE, LEFT, RIGHT, REPORT commands
            const validCommands = ['MOVE', 'LEFT', 'RIGHT', 'REPORT'];
            if (!validCommands.includes(trimmedCommand)) {
                throw new Error(`Invalid command: ${trimmedCommand}. Valid commands: ${validCommands.join(', ')}, PLACE`);
            }

            const response = await fetch(`${API_BASE_URL}/command`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command: trimmedCommand }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || errorData.message || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // For REPORT command, extract output
            let output = null;
            if (trimmedCommand === 'REPORT' && data.is_placed) {
                output = `${data.x},${data.y},${data.facing}`;
            }

            return {
                success: true,
                placed: data.is_placed,
                position: data.is_placed ? { x: data.x, y: data.y, facing: data.facing } : null,
                message: data.message,
                output: output,
            };
        }
    } catch (error) {
        console.error('Error sending command:', error);
        return {
            success: false,
            message: error.message,
        };
    }
}

/**
 * Get the current robot state
 * @returns {Promise<Object>} Current robot state
 */
export async function getRobotState() {
    try {
        const response = await fetch(`${API_BASE_URL}/state`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return {
            success: true,
            placed: data.is_placed,
            position: data.is_placed ? { x: data.x, y: data.y, facing: data.facing } : null,
            message: data.message,
        };
    } catch (error) {
        console.error('Error getting robot state:', error);
        return {
            success: false,
            message: error.message,
        };
    }
}

/**
 * Reset the robot state
 * @returns {Promise<Object>} Response from the server
 */
export async function resetRobot() {
    try {
        const response = await fetch(`${API_BASE_URL}/reset`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return {
            success: true,
            message: data.message,
        };
    } catch (error) {
        console.error('Error resetting robot:', error);
        return {
            success: false,
            message: error.message,
        };
    }
}

/**
 * Execute multiple commands from a file
 * @param {string} commands - Commands separated by newlines
 * @returns {Promise<Object>} Response from the server
 */
export async function executeCommands(commands) {
    const commandList = commands
        .split('\n')
        .map(cmd => cmd.trim())
        .filter(cmd => cmd.length > 0);

    const results = [];

    for (const command of commandList) {
        try {
            const result = await sendCommand(command);
            results.push({
                command,
                success: result.success,
                result,
            });
        } catch (error) {
            results.push({
                command,
                success: false,
                error: error.message,
            });
        }
    }

    return results;
}

/**
 * Health check for the backend API
 * @returns {Promise<boolean>} True if API is healthy
 */
export async function healthCheck() {
    try {
        const response = await fetch(HEALTH_URL, {
            method: 'GET',
        });
        return response.ok;
    } catch (error) {
        console.error('Health check failed:', error);
        return false;
    }
}
