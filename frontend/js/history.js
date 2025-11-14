/**
 * History Module - Command History Management
 * Manages command history tracking and display
 */

// Command history storage
const commandHistory = [];
const MAX_HISTORY_SIZE = 50;

/**
 * Add a command to history
 * @param {string} command - The command that was executed
 * @param {boolean} success - Whether the command succeeded
 * @param {string} output - Optional output from the command
 */
export function addToHistory(command, success, output = '') {
    const historyItem = {
        command,
        success,
        output,
        timestamp: new Date(),
    };

    commandHistory.unshift(historyItem);

    // Keep only the last MAX_HISTORY_SIZE items
    if (commandHistory.length > MAX_HISTORY_SIZE) {
        commandHistory.pop();
    }

    renderHistory();
}

/**
 * Clear all command history
 */
export function clearHistory() {
    commandHistory.length = 0;
    renderHistory();
}

/**
 * Get the full command history
 * @returns {Array} Command history array
 */
export function getHistory() {
    return [...commandHistory];
}

/**
 * Render the command history to the DOM
 */
export function renderHistory() {
    const historyContainer = document.getElementById('historyContainer');

    if (!historyContainer) {
        return;
    }

    // Clear container
    historyContainer.innerHTML = '';

    if (commandHistory.length === 0) {
        const placeholder = document.createElement('p');
        placeholder.className = 'placeholder';
        placeholder.textContent = 'Command history will appear here...';
        historyContainer.appendChild(placeholder);
        return;
    }

    // Render history items
    commandHistory.forEach((item, index) => {
        const historyItem = createHistoryItem(item, index);
        historyContainer.appendChild(historyItem);
    });
}

/**
 * Create a history item element
 * @param {Object} item - History item object
 * @param {number} index - Item index
 * @returns {HTMLElement} History item element
 */
function createHistoryItem(item, index) {
    const div = document.createElement('div');
    div.className = `history-item ${item.success ? 'success' : 'error'}`;
    div.setAttribute('role', 'listitem');
    div.setAttribute('aria-label', `History item: ${item.command}, ${item.success ? 'successful' : 'failed'}`);

    // Command text
    const commandSpan = document.createElement('span');
    commandSpan.className = 'history-command';
    commandSpan.textContent = item.command;

    // Timestamp
    const timestampSpan = document.createElement('span');
    timestampSpan.className = 'history-timestamp';
    timestampSpan.textContent = formatTimestamp(item.timestamp);

    div.appendChild(commandSpan);
    div.appendChild(timestampSpan);

    // Click to reuse command
    div.addEventListener('click', () => {
        const commandInput = document.getElementById('commandInput');
        if (commandInput) {
            commandInput.value = item.command;
            commandInput.focus();
        }
    });

    // Keyboard accessibility
    div.tabIndex = 0;
    div.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            div.click();
        }
    });

    return div;
}

/**
 * Format timestamp for display
 * @param {Date} date - Date object
 * @returns {string} Formatted timestamp
 */
function formatTimestamp(date) {
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return `${hours}:${minutes}:${seconds}`;
}

/**
 * Toggle history visibility
 */
export function toggleHistory() {
    const historyContainer = document.getElementById('historyContainer');
    const toggleButton = document.getElementById('btnToggleHistory');
    const toggleText = document.getElementById('toggleHistoryText');

    if (!historyContainer || !toggleButton || !toggleText) {
        return;
    }

    const isHidden = historyContainer.classList.toggle('hidden');

    // Update button text and aria-expanded
    toggleText.textContent = isHidden ? 'Show' : 'Hide';
    toggleButton.setAttribute('aria-expanded', !isHidden);
}

/**
 * Initialize history controls
 */
export function initializeHistory() {
    const clearHistoryBtn = document.getElementById('btnClearHistory');
    const toggleHistoryBtn = document.getElementById('btnToggleHistory');

    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener('click', () => {
            if (confirm('Are you sure you want to clear the command history?')) {
                clearHistory();
            }
        });
    }

    if (toggleHistoryBtn) {
        toggleHistoryBtn.addEventListener('click', toggleHistory);
    }

    // Initial render
    renderHistory();
}

/**
 * Export history as text
 * @returns {string} History as formatted text
 */
export function exportHistory() {
    if (commandHistory.length === 0) {
        return 'No commands in history.';
    }

    return commandHistory
        .map((item) => {
            const status = item.success ? '✓' : '✗';
            const time = formatTimestamp(item.timestamp);
            return `[${time}] ${status} ${item.command}`;
        })
        .join('\n');
}
