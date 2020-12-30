import unittest
import database_commands
import vm_commands
import file_commands

class TestDatabaseCommands(unittest.TestCase):
    def test_addusser(self):
        database_commands.add_student("test_student")