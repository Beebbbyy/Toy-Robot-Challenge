/**
 * Grid Module - Grid Rendering and Visualization
 * Handles the visual representation of the 5x5 table and robot
 */

import { robotState, getGridIndex, getCoordinatesFromIndex } from './robot.js';

// Grid visualization state
let isIsometricView = false;
let currentZoomLevel = 100;
let pathTrail = [];
let isDraggingRobot = false;
let ghostPreviewCell = null;

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

        // Add click handler for placing robot
        cell.addEventListener('click', () => handleCellClick(x, y));

        // Add mouse enter handler for ghost preview
        cell.addEventListener('mouseenter', () => showGhostPreview(cell, x, y));
        cell.addEventListener('mouseleave', () => hideGhostPreview(cell));

        // Add drag and drop handlers
        cell.addEventListener('dragover', (e) => handleDragOver(e, cell));
        cell.addEventListener('dragleave', () => handleDragLeave(cell));
        cell.addEventListener('drop', (e) => handleDrop(e, x, y));

        gridContainer.appendChild(cell);
    }

    // Initialize grid controls
    initializeGridControls();
}

/**
 * Render the robot on the grid
 * Updates the grid to show the robot at its current position
 */
export function renderRobot() {
    // Clear all cells (except path trail)
    const cells = document.querySelectorAll('.grid-cell');
    cells.forEach(cell => {
        cell.classList.remove('active');
        // Preserve path trail when clearing
        const hasTrail = cell.classList.contains('path-trail');
        cell.innerHTML = '';
        if (!hasTrail) {
            cell.classList.remove('path-trail');
        }
    });

    // Render path trail
    renderPathTrail();

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

            // Make robot draggable
            robotIcon.draggable = true;
            robotIcon.addEventListener('dragstart', handleRobotDragStart);
            robotIcon.addEventListener('dragend', handleRobotDragEnd);

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
    // Add old position to path trail
    if (fromX !== null && fromY !== null) {
        addToPathTrail(fromX, fromY);
    }

    // Add smooth transition class
    const cells = document.querySelectorAll('.grid-cell');
    const fromIndex = getGridIndex(fromX, fromY);
    const toIndex = getGridIndex(toX, toY);

    if (cells[fromIndex]) {
        cells[fromIndex].classList.add('robot-moving');
    }

    // Render robot at new position with animation
    setTimeout(() => {
        renderRobot();
        updatePositionDisplay();

        // Remove animation class
        if (cells[toIndex]) {
            setTimeout(() => {
                cells[toIndex].classList.remove('robot-moving');
            }, 500);
        }
    }, 50);
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

/**
 * Initialize grid controls (isometric, zoom, path clear)
 */
function initializeGridControls() {
    // Isometric toggle
    const btnToggleIsometric = document.getElementById('btnToggleIsometric');
    if (btnToggleIsometric) {
        btnToggleIsometric.addEventListener('click', toggleIsometricView);
    }

    // Zoom controls
    const btnZoomIn = document.getElementById('btnZoomIn');
    const btnZoomOut = document.getElementById('btnZoomOut');

    if (btnZoomIn) {
        btnZoomIn.addEventListener('click', () => adjustZoom(25));
    }

    if (btnZoomOut) {
        btnZoomOut.addEventListener('click', () => adjustZoom(-25));
    }

    // Clear path trail
    const btnClearPath = document.getElementById('btnClearPath');
    if (btnClearPath) {
        btnClearPath.addEventListener('click', clearPathTrail);
    }
}

/**
 * Toggle isometric view
 */
function toggleIsometricView() {
    isIsometricView = !isIsometricView;
    const gridContainer = document.getElementById('gridContainer');

    if (isIsometricView) {
        gridContainer.classList.add('isometric');
    } else {
        gridContainer.classList.remove('isometric');
    }
}

/**
 * Adjust zoom level
 * @param {number} delta - Amount to change zoom by
 */
function adjustZoom(delta) {
    const zoomLevels = [50, 75, 100, 125, 150];
    const currentIndex = zoomLevels.indexOf(currentZoomLevel);
    const newIndex = Math.max(0, Math.min(zoomLevels.length - 1, currentIndex + (delta > 0 ? 1 : -1)));

    currentZoomLevel = zoomLevels[newIndex];

    const gridContainer = document.getElementById('gridContainer');
    const zoomLevelDisplay = document.getElementById('zoomLevel');

    // Remove all zoom classes
    zoomLevels.forEach(level => {
        gridContainer.classList.remove(`zoom-${level}`);
    });

    // Add new zoom class
    gridContainer.classList.add(`zoom-${currentZoomLevel}`);

    // Update display
    if (zoomLevelDisplay) {
        zoomLevelDisplay.textContent = `${currentZoomLevel}%`;
    }
}

/**
 * Add position to path trail
 * @param {number} x - X coordinate
 * @param {number} y - Y coordinate
 */
function addToPathTrail(x, y) {
    const posKey = `${x},${y}`;
    if (!pathTrail.includes(posKey)) {
        pathTrail.push(posKey);
    }
}

/**
 * Render path trail on grid
 */
function renderPathTrail() {
    const cells = document.querySelectorAll('.grid-cell');

    pathTrail.forEach(posKey => {
        const [x, y] = posKey.split(',').map(Number);
        const index = getGridIndex(x, y);

        if (cells[index] && !cells[index].classList.contains('active')) {
            cells[index].classList.add('path-trail');
        }
    });
}

/**
 * Clear path trail
 */
function clearPathTrail() {
    pathTrail = [];
    const cells = document.querySelectorAll('.grid-cell');
    cells.forEach(cell => {
        cell.classList.remove('path-trail');
    });
    renderRobot();
}

/**
 * Handle cell click for placing robot
 * @param {number} x - X coordinate
 * @param {number} y - Y coordinate
 */
function handleCellClick(x, y) {
    // Only auto-place if robot is not already placed
    if (!robotState.isPlaced) {
        // Import and call place function
        import('./controls.js').then(module => {
            if (module.placeRobotAtCoordinates) {
                module.placeRobotAtCoordinates(x, y, 'NORTH');
            }
        });
    }
}

/**
 * Show ghost preview of robot
 * @param {HTMLElement} cell - Cell element
 * @param {number} x - X coordinate
 * @param {number} y - Y coordinate
 */
function showGhostPreview(cell, x, y) {
    // Only show preview if robot is not placed
    if (!robotState.isPlaced) {
        cell.classList.add('ghost-preview');

        const ghostRobot = document.createElement('div');
        ghostRobot.className = 'ghost-robot';

        const ghostIcon = document.createElement('div');
        ghostIcon.className = 'ghost-robot-icon';

        const ghostSymbol = document.createElement('span');
        ghostSymbol.className = 'ghost-robot-symbol';
        ghostSymbol.textContent = '🤖';

        ghostIcon.appendChild(ghostSymbol);
        ghostRobot.appendChild(ghostIcon);
        cell.appendChild(ghostRobot);

        ghostPreviewCell = cell;
    }
}

/**
 * Hide ghost preview
 * @param {HTMLElement} cell - Cell element
 */
function hideGhostPreview(cell) {
    cell.classList.remove('ghost-preview');
    const ghostRobot = cell.querySelector('.ghost-robot');
    if (ghostRobot) {
        ghostRobot.remove();
    }
    ghostPreviewCell = null;
}

/**
 * Handle robot drag start
 * @param {DragEvent} e - Drag event
 */
function handleRobotDragStart(e) {
    isDraggingRobot = true;
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', `${robotState.x},${robotState.y}`);

    // Add dragging class to current cell
    const currentIndex = getGridIndex(robotState.x, robotState.y);
    const cells = document.querySelectorAll('.grid-cell');
    if (cells[currentIndex]) {
        cells[currentIndex].classList.add('dragging');
    }
}

/**
 * Handle robot drag end
 * @param {DragEvent} e - Drag event
 */
function handleRobotDragEnd(e) {
    isDraggingRobot = false;

    // Remove dragging class from all cells
    const cells = document.querySelectorAll('.grid-cell');
    cells.forEach(cell => {
        cell.classList.remove('dragging');
        cell.classList.remove('drag-over');
    });
}

/**
 * Handle drag over cell
 * @param {DragEvent} e - Drag event
 * @param {HTMLElement} cell - Cell element
 */
function handleDragOver(e, cell) {
    if (isDraggingRobot) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        cell.classList.add('drag-over');
    }
}

/**
 * Handle drag leave cell
 * @param {HTMLElement} cell - Cell element
 */
function handleDragLeave(cell) {
    cell.classList.remove('drag-over');
}

/**
 * Handle drop on cell
 * @param {DragEvent} e - Drag event
 * @param {number} x - X coordinate
 * @param {number} y - Y coordinate
 */
function handleDrop(e, x, y) {
    if (isDraggingRobot) {
        e.preventDefault();

        // Import and call place function to move robot
        import('./controls.js').then(module => {
            if (module.placeRobotAtCoordinates) {
                module.placeRobotAtCoordinates(x, y, robotState.facing);
            }
        });

        // Remove drag-over class
        const cells = document.querySelectorAll('.grid-cell');
        cells.forEach(cell => {
            cell.classList.remove('drag-over');
        });
    }
}
