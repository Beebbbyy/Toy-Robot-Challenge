/**
 * Utils Module - Utility Functions
 * Common utility functions for the application
 */

/**
 * Add output to the output container
 * @param {string} message - Message to display
 * @param {string} type - Type of message (info, success, error)
 */
export function addOutput(message, type = 'info') {
    const outputContainer = document.getElementById('outputContainer');

    // Remove placeholder if it exists
    const placeholder = outputContainer.querySelector('.placeholder');
    if (placeholder) {
        placeholder.remove();
    }

    // Create output line
    const line = document.createElement('div');
    line.className = `output-line output-${type}`;
    line.textContent = `${getCurrentTimestamp()} ${message}`;

    // Add to container
    outputContainer.appendChild(line);

    // Auto-scroll to bottom
    outputContainer.scrollTop = outputContainer.scrollHeight;

    // Limit output lines to 100
    const lines = outputContainer.querySelectorAll('.output-line');
    if (lines.length > 100) {
        lines[0].remove();
    }
}

/**
 * Add success message to output
 * @param {string} message - Success message
 */
export function addSuccess(message) {
    addOutput(`✓ ${message}`, 'success');
}

/**
 * Add error message to output
 * @param {string} message - Error message
 */
export function addError(message) {
    addOutput(`✗ ${message}`, 'error');
}

/**
 * Add info message to output
 * @param {string} message - Info message
 */
export function addInfo(message) {
    addOutput(`ℹ ${message}`, 'info');
}

/**
 * Clear the output container
 */
export function clearOutput() {
    const outputContainer = document.getElementById('outputContainer');
    outputContainer.innerHTML = '<p class="placeholder">Command results will appear here...</p>';
}

/**
 * Get current timestamp for output
 * @returns {string} Formatted timestamp
 */
function getCurrentTimestamp() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    return `[${hours}:${minutes}:${seconds}]`;
}

/**
 * Debounce function to limit function calls
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
export function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle function to limit function calls
 * @param {Function} func - Function to throttle
 * @param {number} limit - Time limit in milliseconds
 * @returns {Function} Throttled function
 */
export function throttle(func, limit) {
    let inThrottle;
    return function executedFunction(...args) {
        if (!inThrottle) {
            func(...args);
            inThrottle = true;
            setTimeout(() => (inThrottle = false), limit);
        }
    };
}

/**
 * Format error message for display
 * @param {Error|string} error - Error object or message
 * @returns {string} Formatted error message
 */
export function formatError(error) {
    if (error instanceof Error) {
        return error.message;
    }
    return String(error);
}

/**
 * Validate command format
 * @param {string} command - Command string
 * @returns {boolean} True if valid
 */
export function validateCommand(command) {
    const validCommands = ['PLACE', 'MOVE', 'LEFT', 'RIGHT', 'REPORT'];
    const upperCommand = command.trim().toUpperCase();

    // Check if it's a simple command
    if (validCommands.includes(upperCommand)) {
        return true;
    }

    // Check if it's a PLACE command with coordinates
    if (upperCommand.startsWith('PLACE ')) {
        const placePattern = /^PLACE \d+,\d+,(NORTH|EAST|SOUTH|WEST)$/;
        return placePattern.test(upperCommand);
    }

    return false;
}

/**
 * Parse PLACE command
 * @param {string} command - PLACE command string
 * @returns {Object|null} Parsed command {x, y, facing} or null if invalid
 */
export function parsePlaceCommand(command) {
    const upperCommand = command.trim().toUpperCase();

    if (!upperCommand.startsWith('PLACE ')) {
        return null;
    }

    const parts = upperCommand.substring(6).split(',');

    if (parts.length !== 3) {
        return null;
    }

    const x = parseInt(parts[0], 10);
    const y = parseInt(parts[1], 10);
    const facing = parts[2].trim();

    if (isNaN(x) || isNaN(y)) {
        return null;
    }

    const validDirections = ['NORTH', 'EAST', 'SOUTH', 'WEST'];
    if (!validDirections.includes(facing)) {
        return null;
    }

    return { x, y, facing };
}

/**
 * Show a notification (toast)
 * @param {string} message - Notification message
 * @param {string} type - Type (success, error, info)
 * @param {number} duration - Duration in milliseconds
 */
export function showNotification(message, type = 'info', duration = 3000) {
    // This could be expanded to create toast notifications
    // For now, just log to console
    console.log(`[${type.toUpperCase()}] ${message}`);
}
