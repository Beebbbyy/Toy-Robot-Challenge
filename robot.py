class Robot:
    def __init__(self):
        self.x = None
        self.y = None
        self.facing = None

    def place(self, x, y, facing):
        if 0 <= x <= 4 and 0 <= y <= 4 and facing in ('NORTH', 'SOUTH', 'EAST', 'WEST'):
            self.x = x
            self.y = y
            self.facing = facing
            return True  # Placement successful
        else:
            return False  # Invalid placement

    def move(self):
        if self.facing == 'NORTH':
            self.y = min(self.y + 1, 4)  # Stay within Y bounds
        elif self.facing == 'SOUTH':
            self.y = max(self.y - 1, 0)  # Stay within Y bounds
        elif self.facing == 'EAST':
            self.x = min(self.x + 1, 4)  # Stay within X bounds
        elif self.facing == 'WEST':
            self.x = max(self.x - 1, 0)  # Stay within X bounds

    def left(self):
        directions = ['NORTH', 'EAST', 'SOUTH', 'WEST']
        self.facing = directions[(directions.index(self.facing) - 1) % 4]

    def right(self):
        directions = ['NORTH', 'EAST', 'SOUTH', 'WEST']
        self.facing = directions[(directions.index(self.facing) + 1) % 4]

    def report(self):
        if self.x is not None and self.y is not None:  # Check if placed
            return f"{self.x}, {self.y}, {self.facing}"
        else:
            return "Not placed"

class Table:
    def __init__(self):
        self.robot = Robot()

    def process_command(self, command):
        parts = command.split()
        if parts[0] == 'PLACE':
            x, y, facing = map(str.strip, parts[1].split(','))
            if self.robot.place(int(x), int(y), facing):
                return "Robot placed successfully."
            else:
                return "Invalid placement."
        elif parts[0] == 'MOVE' and self.robot.x is not None:  # Check if placed
            self.robot.move()
            return "Move successful."
        elif parts[0] in ('LEFT', 'RIGHT') and self.robot.x is not None:
            getattr(self.robot, parts[0].lower())()  # Call left or right method
            return f"{parts[0]} successful."
        elif parts[0] == 'REPORT' and self.robot.x is not None:
            return self.robot.report()
        else:
            return "Invalid command."

def print_table(robot):
    for row in range(4, -1, -1):
        row_str = "|"
        for col in range(5):
            if robot.x == col and robot.y == row:
                row_str += " 🤖"
            else:
                row_str += "   "
            row_str += "|"
        print(row_str)
        if row > 0:
            print("+---+---+---+---+---+")

# Main Interaction
if __name__ == '__main__':
    table = Table()
    while True:
        cmd = input("Enter command: ")
        result = table.process_command(cmd)
        print(result)
        print_table(table.robot)
