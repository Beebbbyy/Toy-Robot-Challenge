/**
 * API Module - Backend Communication
 * Handles all HTTP requests to the backend API
 */

// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';

/**
 * Send a command to the robot
 * @param {string} command - The command to execute (e.g., 'PLACE 0,0,NORTH', 'MOVE', 'LEFT', 'RIGHT', 'REPORT')
 * @returns {Promise<Object>} Response from the server
 */
export async function sendCommand(command) {
    try {
        const response = await fetch(`${API_BASE_URL}/command`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ command: command.trim() }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error sending command:', error);
        throw error;
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

        return await response.json();
    } catch (error) {
        console.error('Error getting robot state:', error);
        throw error;
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

        return await response.json();
    } catch (error) {
        console.error('Error resetting robot:', error);
        throw error;
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
                success: true,
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
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: 'GET',
        });
        return response.ok;
    } catch (error) {
        console.error('Health check failed:', error);
        return false;
    }
}
