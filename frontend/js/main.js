/**
 * Main Module - Application Entry Point
 * Initializes the application and coordinates all modules
 */

import { initializeGrid, updateGrid } from './grid.js';
import { initializeControls } from './controls.js';
import { initializeHistory } from './history.js';
import { healthCheck } from './api.js';
import { addInfo, addError, addSuccess } from './utils.js';

/**
 * Initialize the application
 */
async function init() {
    try {
        // Display welcome message
        addInfo('Toy Robot Simulator initialized');
        addInfo('Checking backend connection...');

        // Check backend health
        const isHealthy = await healthCheck();

        if (isHealthy) {
            addSuccess('Backend connected successfully');
        } else {
            addError('Warning: Backend server not responding');
            addInfo('Make sure the backend server is running on http://localhost:8000');
        }

        // Initialize grid
        initializeGrid();
        updateGrid();
        addInfo('Grid initialized');

        // Initialize controls
        initializeControls();
        addInfo('Controls initialized');

        // Initialize history
        initializeHistory();
        addInfo('Command history ready');

        // Display help message
        displayHelp();

    } catch (error) {
        console.error('Initialization error:', error);
        addError(`Initialization failed: ${error.message}`);
    }
}

/**
 * Display help information
 */
function displayHelp() {
    addInfo('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    addInfo('Available Commands:');
    addInfo('  PLACE X,Y,F - Place robot at position (X,Y) facing F');
    addInfo('                where X,Y are 0-4 and F is NORTH/EAST/SOUTH/WEST');
    addInfo('  MOVE        - Move robot one unit forward');
    addInfo('  LEFT        - Rotate robot 90° left');
    addInfo('  RIGHT       - Rotate robot 90° right');
    addInfo('  REPORT      - Display current position');
    addInfo('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
}

/**
 * Handle application errors
 * @param {Error} error - Error object
 */
function handleError(error) {
    console.error('Application error:', error);
    addError(`Error: ${error.message}`);
}

/**
 * Set up global error handlers
 */
function setupErrorHandlers() {
    window.addEventListener('error', (event) => {
        handleError(event.error);
    });

    window.addEventListener('unhandledrejection', (event) => {
        handleError(new Error(event.reason));
    });
}

// Initialize when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        setupErrorHandlers();
        init();
    });
} else {
    setupErrorHandlers();
    init();
}

// Export for debugging
export { init };
