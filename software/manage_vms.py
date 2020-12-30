import database_commands
import sys
if sys.argv[1] == "A":
    print(database_commands.add_vm(sys.argv[2]))
elif sys.argv[1] == "R":
    print(database_commands.delete_vm(sys.argv[2]))