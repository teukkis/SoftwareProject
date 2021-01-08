from Crypto.PublicKey import RSA
import file_commands
import database_commands
import sys
def genSSH():
    key = RSA.generate(2048)
    public = key.publickey()
    return key.exportKey('PEM'), public.exportKey('OpenSSH')


def create_user(username):
    fail = database_commands.add_student(username)

    if not fail==False:
        print("Error adding user to the database")
        print(fail)
        return
    
    private,public = genSSH()

    output,success = file_commands.add_student(username, public)
    if not success:
        print("Error creating the user into the filesystem")
        print(output)
        database_commands.delete_student(username)
        return
    
    print("Successfully created user with username: {} \n Send this private key to the student:\n{}".format(username,private))
    return
def delete_user(username):
    file_commands.delete_user(username)
    fail = database_commands.delete_student(username)
    if not fail == False:
        print("Error removing user from database")
        print(fail)
        return
    print("Succesfully removed user {}".format(username))
    return

def regenSSH(username):
    private,public = genSSH()

    output, success = file_commands.set_ssh_key(username,public)
    if not success:
        print("Failed changing the ssh key for user: {}".format(username))
        print(output)
        return
    print("Succesfully updated the ssh key for user: {}\n Send this private key to the student:\n{}".format(username,private))
    return

if __name__ == "__main__":
    if sys.argv[1] == "A":
        create_user(sys.argv[2])
    elif sys.argv[1] == "R":
        delete_user(sys.argv[2])
    elif sys.argv[1] == "S":
        regenSSH(sys.argv[2])
