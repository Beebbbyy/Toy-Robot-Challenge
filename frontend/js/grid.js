/**
 * Grid Module - Grid Rendering and Visualization
 * Handles the visual representation of the 5x5 table and robot
 */

import { robotState, getGridIndex, getCoordinatesFromIndex } from './robot.js';

/**
 * Initialize the grid
 * Creates a 5x5 grid of cells
 */
export function initializeGrid() {
    const gridContainer = document.getElementById('gridContainer');
    gridContainer.innerHTML = '';

    // Create 25 cells (5x5 grid)
    for (let i = 0; i < 25; i++) {
        const cell = document.createElement('div');
        cell.className = 'grid-cell';

        // Get coordinates for this cell
        const { x, y } = getCoordinatesFromIndex(i);

        // Set data attributes for coordinates
        cell.dataset.x = x;
        cell.dataset.y = y;
        cell.dataset.index = i;

        gridContainer.appendChild(cell);
    }
}

/**
 * Render the robot on the grid
 * Updates the grid to show the robot at its current position
 */
export function renderRobot() {
    // Clear all cells
    const cells = document.querySelectorAll('.grid-cell');
    cells.forEach(cell => {
        cell.classList.remove('active');
        cell.innerHTML = '';
    });

    // If robot is placed, render it
    if (robotState.isPlaced) {
        const index = getGridIndex(robotState.x, robotState.y);
        const cell = cells[index];

        if (cell) {
            cell.classList.add('active');

            // Create robot element
            const robot = document.createElement('div');
            robot.className = 'robot';

            // Create robot icon
            const robotIcon = document.createElement('div');
            robotIcon.className = 'robot-icon';

            // Add robot symbol (emoji)
            const robotSymbol = document.createElement('span');
            robotSymbol.className = 'robot-symbol';
            robotSymbol.textContent = '🤖';

            robotIcon.appendChild(robotSymbol);
            robot.appendChild(robotIcon);

            // Add direction indicator
            const directionIndicator = document.createElement('div');
            directionIndicator.className = `robot-direction ${robotState.facing.toLowerCase()}`;
            robot.appendChild(directionIndicator);

            cell.appendChild(robot);
        }
    }
}

/**
 * Update the robot position display
 * Updates the text showing the robot's current position
 */
export function updatePositionDisplay() {
    const positionElement = document.getElementById('robotPosition');
    const directionElement = document.getElementById('robotDirection');

    if (robotState.isPlaced) {
        positionElement.textContent = `${robotState.x}, ${robotState.y}`;
        directionElement.textContent = robotState.facing;
    } else {
        positionElement.textContent = 'Not placed';
        directionElement.textContent = '-';
    }
}

/**
 * Animate robot movement
 * @param {number} fromX - Starting X coordinate
 * @param {number} fromY - Starting Y coordinate
 * @param {number} toX - Ending X coordinate
 * @param {number} toY - Ending Y coordinate
 */
export function animateRobotMovement(fromX, fromY, toX, toY) {
    // For now, just render the robot at the new position
    // In the future, this could include smooth transitions
    renderRobot();
    updatePositionDisplay();
}

/**
 * Highlight a cell temporarily
 * @param {number} x - X coordinate
 * @param {number} y - Y coordinate
 * @param {string} className - CSS class to add
 * @param {number} duration - Duration in milliseconds
 */
export function highlightCell(x, y, className = 'highlight', duration = 500) {
    const index = getGridIndex(x, y);
    const cells = document.querySelectorAll('.grid-cell');
    const cell = cells[index];

    if (cell) {
        cell.classList.add(className);
        setTimeout(() => {
            cell.classList.remove(className);
        }, duration);
    }
}

/**
 * Update the entire grid display
 */
export function updateGrid() {
    renderRobot();
    updatePositionDisplay();
}
