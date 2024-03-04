import unittest
from robot import Table

class TestRobotTable(unittest.TestCase):
    def setUp(self):
        self.table = Table()

    def test_place_command(self):
        self.assertEqual(self.table.process_command("PLACE 0,0,NORTH"), "Robot placed successfully.")
        self.assertEqual(self.table.process_command("REPORT"), "0, 0, NORTH")

    def test_move_command(self):
        self.table.process_command("PLACE 0,0,NORTH")
        self.assertEqual(self.table.process_command("MOVE"), "Move successful.")
        self.assertEqual(self.table.process_command("REPORT"), "0, 1, NORTH")

    def test_left_command(self):
        self.table.process_command("PLACE 0,0,NORTH")
        self.assertEqual(self.table.process_command("LEFT"), "LEFT successful.")
        self.assertEqual(self.table.process_command("REPORT"), "0, 0, WEST")

    def test_complex_commands(self):
        self.assertEqual(self.table.process_command("PLACE 1,2,EAST"), "Robot placed successfully.")
        self.assertEqual(self.table.process_command("MOVE"), "Move successful.")
        self.assertEqual(self.table.process_command("MOVE"), "Move successful.")
        self.assertEqual(self.table.process_command("LEFT"), "LEFT successful.")
        self.assertEqual(self.table.process_command("MOVE"), "Move successful.")
        self.assertEqual(self.table.process_command("REPORT"), "3, 3, NORTH")

if __name__ == '__main__':
    unittest.main()
