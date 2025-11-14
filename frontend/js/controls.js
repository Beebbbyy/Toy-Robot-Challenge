/**
 * Controls Module - User Interface Controls
 * Handles all user interactions with buttons and input fields
 */

import { sendCommand, resetRobot, executeCommands } from './api.js';
import { updateRobotState, resetRobotState, parseRobotState } from './robot.js';
import { updateGrid } from './grid.js';
import { addOutput, clearOutput, addError, addSuccess, addInfo } from './utils.js';
import { addToHistory } from './history.js';

/**
 * Initialize all control event listeners
 */
export function initializeControls() {
    // Place button
    document.getElementById('btnPlace').addEventListener('click', handlePlaceCommand);

    // Movement buttons
    document.getElementById('btnMove').addEventListener('click', () => handleSimpleCommand('MOVE'));
    document.getElementById('btnLeft').addEventListener('click', () => handleSimpleCommand('LEFT'));
    document.getElementById('btnRight').addEventListener('click', () => handleSimpleCommand('RIGHT'));

    // Action buttons
    document.getElementById('btnReport').addEventListener('click', handleReportCommand);
    document.getElementById('btnReset').addEventListener('click', handleResetCommand);

    // Command input
    document.getElementById('btnExecute').addEventListener('click', handleExecuteCommand);
    document.getElementById('commandInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleExecuteCommand();
        }
    });

    // File upload
    document.getElementById('btnLoadFile').addEventListener('click', handleFileUpload);

    // Clear output
    document.getElementById('btnClearOutput').addEventListener('click', clearOutput);
}

/**
 * Handle PLACE command from UI controls
 */
async function handlePlaceCommand() {
    const x = document.getElementById('placeX').value;
    const y = document.getElementById('placeY').value;
    const f = document.getElementById('placeF').value;

    const command = `PLACE ${x},${y},${f}`;

    try {
        addInfo(`Executing: ${command}`);
        const response = await sendCommand(command);

        if (response.success) {
            const state = parseRobotState(response);
            updateRobotState(state.x, state.y, state.facing);
            updateGrid();
            addSuccess(`Robot placed at ${x},${y} facing ${f}`);
            addToHistory(command, true, `Placed at ${x},${y} facing ${f}`);
        } else {
            addError(response.message || 'Failed to place robot');
            addToHistory(command, false, response.message);
        }
    } catch (error) {
        addError(`Error: ${error.message}`);
        addToHistory(command, false, error.message);
    }
}

/**
 * Handle simple commands (MOVE, LEFT, RIGHT)
 * @param {string} command - Command name
 */
async function handleSimpleCommand(command) {
    try {
        addInfo(`Executing: ${command}`);
        const response = await sendCommand(command);

        if (response.success) {
            const state = parseRobotState(response);
            updateRobotState(state.x, state.y, state.facing);
            updateGrid();
            addSuccess(`Command executed: ${command}`);
            addToHistory(command, true);
        } else {
            addError(response.message || `Failed to execute ${command}`);
            addToHistory(command, false, response.message);
        }
    } catch (error) {
        addError(`Error: ${error.message}`);
        addToHistory(command, false, error.message);
    }
}

/**
 * Handle REPORT command
 */
async function handleReportCommand() {
    try {
        addInfo('Executing: REPORT');
        const response = await sendCommand('REPORT');

        if (response.success && response.output) {
            addSuccess(`REPORT: ${response.output}`);
            addToHistory('REPORT', true, response.output);

            // Update state from report
            const state = parseRobotState(response);
            updateRobotState(state.x, state.y, state.facing);
            updateGrid();
        } else {
            addError(response.message || 'No output from REPORT');
            addToHistory('REPORT', false, response.message);
        }
    } catch (error) {
        addError(`Error: ${error.message}`);
        addToHistory('REPORT', false, error.message);
    }
}

/**
 * Handle RESET command
 */
async function handleResetCommand() {
    try {
        addInfo('Resetting robot...');
        const response = await resetRobot();

        if (response.success) {
            resetRobotState();
            updateGrid();
            addSuccess('Robot reset successfully');
            addToHistory('RESET', true);

            // Reset input fields
            document.getElementById('placeX').value = '0';
            document.getElementById('placeY').value = '0';
            document.getElementById('placeF').value = 'NORTH';
        } else {
            addError('Failed to reset robot');
            addToHistory('RESET', false);
        }
    } catch (error) {
        addError(`Error: ${error.message}`);
        addToHistory('RESET', false, error.message);
    }
}

/**
 * Handle command execution from text input
 */
async function handleExecuteCommand() {
    const input = document.getElementById('commandInput');
    const command = input.value.trim();

    if (!command) {
        addError('Please enter a command');
        return;
    }

    try {
        addInfo(`Executing: ${command}`);
        const response = await sendCommand(command);

        if (response.success) {
            const state = parseRobotState(response);
            updateRobotState(state.x, state.y, state.facing);
            updateGrid();

            if (response.output) {
                addSuccess(`Output: ${response.output}`);
                addToHistory(command, true, response.output);
            } else {
                addSuccess('Command executed successfully');
                addToHistory(command, true);
            }
        } else {
            addError(response.message || 'Command failed');
            addToHistory(command, false, response.message);
        }
    } catch (error) {
        addError(`Error: ${error.message}`);
        addToHistory(command, false, error.message);
    }

    // Clear input
    input.value = '';
}

/**
 * Handle file upload and command execution
 */
async function handleFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (!file) {
        addError('Please select a file');
        return;
    }

    try {
        const text = await file.text();
        addInfo(`Loading commands from file: ${file.name}`);

        const results = await executeCommands(text);

        // Display results
        results.forEach(result => {
            if (result.success) {
                addSuccess(`${result.command} - Success`);
                if (result.result.output) {
                    addOutput(`  → ${result.result.output}`);
                    addToHistory(result.command, true, result.result.output);
                } else {
                    addToHistory(result.command, true);
                }
            } else {
                addError(`${result.command} - ${result.error}`);
                addToHistory(result.command, false, result.error);
            }
        });

        // Update state from last successful command
        const lastSuccess = results.reverse().find(r => r.success);
        if (lastSuccess) {
            const state = parseRobotState(lastSuccess.result);
            updateRobotState(state.x, state.y, state.facing);
            updateGrid();
        }

        addInfo(`File processing complete: ${results.length} commands executed`);
    } catch (error) {
        addError(`Error reading file: ${error.message}`);
    }

    // Clear file input
    fileInput.value = '';
}
