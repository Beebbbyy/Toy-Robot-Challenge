# Toy-Robot-Challenge

# Toy Robot Simulator

This project is a simple implementation of a toy robot simulator in Python. The simulator consists of a `Robot` class and a `Table` class to control the robot's movements on a 5x5 tabletop.

## Robot Class

The `Robot` class represents the toy robot with the following functionalities:

- `place(x, y, facing)`: Places the robot on the tabletop at the specified coordinates (x, y) and facing direction ('NORTH', 'SOUTH', 'EAST', 'WEST').
- `move()`: Moves the robot one unit forward in the current facing direction, staying within the bounds of the tabletop.
- `left()`: Rotates the robot 90 degrees to the left.
- `right()`: Rotates the robot 90 degrees to the right.
- `report()`: Returns the current position (x, y) and facing direction of the robot.

## Table Class

The `Table` class manages the interaction with the robot, processing user commands and updating the robot's state accordingly.

## Usage

To interact with the toy robot simulator, run the `robot.py` script. The simulator supports the following commands:

- `PLACE x, y, facing`: Place the robot on the tabletop at the specified coordinates (x, y) and facing direction.
- `MOVE`: Move the robot one unit forward in the current facing direction.
- `LEFT`: Rotate the robot 90 degrees to the left.
- `RIGHT`: Rotate the robot 90 degrees to the right.
- `REPORT`: Display the current position and facing direction of the robot.

For example:

```bash
python robot.py
```

Enter commands when prompted to control the toy robot on the tabletop.

Example COMMAND:

```bash
PLACE 0,0,NORTH
```

## Assumptions

- The tabletop is a 5x5 grid, and the robot cannot move beyond these bounds.
- The `PLACE` command is necessary before any other movement commands (`MOVE`, `LEFT`, `RIGHT`, `REPORT`).
- **The commands are case-sensitive.**
- Invalid commands or placements are gracefully handled, and the user is notified.

## Notes

The `print_table` function visually represents the robot's position on the tabletop using ASCII characters. The robot is represented by the emoji 🤖 for better visualization.

Feel free to explore the code and experiment with different commands to navigate the toy robot on the tabletop.
