
import socket
import sys
import os
from time import sleep
import database_commands
import file_commands
import vm_commands
import config

#Setup the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 8080))  #receive requests here
addr = ("127.0.0.1", 8081)      #send replies here

#availableVMs = [8888, 8889]     #Available VMs (port numbers)
#inUseVMs = {}                   #Currently reserved VMs per username (port numbers)

connect_message = """You need to forward this port in your Putty settings: {0}
If you are using ssh on terminal you need to open new terminal window and add this to your ssh-command: \"-R {0}:localhost:{0}\"
Your Jupyter Notebook password is: {1}
"""


def GiveVM(user):
    """
    Set user to next free virtual machine
    -------------------------------------------------------
    user = the username which we want to give the vm for
    -------------------------------------------------------
    On success will return port linked to that specific virtual machine and the password of the jupyter notebook.
    """
    #Get next free vm
    port, passwd, new_user = database_commands.set_student_on_vm(user)
    if port: #If got vm check if the user is just connecting or if it is reconnection situation
        if new_user:
            #In case of new user start virtual machine for them
            success, passwd = vm_commands.StartVM(port,user,passwd)
            if success:
                return port,passwd
            #If starting virtual machine failed we need to revert changes to database and close the vm
            FreeVM(user, port)
            return False, False
    return port, passwd

    #if not inUseVMs.get(user, None):
        #if len(availableVMs)>0:
            #inUseVMs[user] = availableVMs.pop()
            #StartVM(inUseVMs[user], user)
        #else:
            #return "Unfortunately, all virtual machines are currently reserved."

    #return str(inUseVMs[user])

#Release a VM that is reserved to a user
def FreeVM(user,port = None):
    """
    Empties virtual machine in database and shuts down the virtual machine
    -------------------------------------------------------
    user = the username whose virtual machine we want to close
    port = optional argument if we want to just close the virtual machine using the port number
    """
    success = database_commands.free_student_from_vm(user)
    
    
    if success:
        vm_commands.CloseVM(success)
    elif not port == None:
        vm_commands.CloseVM(port)
        database_commands.empty_vm(port)
        return True
    
    return success

#Wait for packets, then return a VM for them if available
while True:
    message, address = server_socket.recvfrom(1024)
    message = message.decode("utf-8")
    print(message)
    if "Connect:" in message: #When user connects try to start virtual machine for them
        user = message.split(':')[1]
        success, passwd = GiveVM(user)
        if success:
            server_socket.sendto(connect_message.format(success,passwd).encode("utf-8"),addr)
        else:
            server_socket.sendto("Error while trying to assign a virtual machine. Please contact your teacher.".encode("utf-8"),addr)
    elif "Disconnect:" in message: #When user disconnects free the virtual machine
        user = message.split(':')[1]
        success = FreeVM(user)
        server_socket.sendto("Disconnected".encode("utf-8"),addr)
        if not success == False:
            print("Succesfully disconnected user")
        else:
            print("Error in disconnecting user")
    elif "User_left:" in message: #If connection to user is lost don't close the virtual machine
        user = message.split(':')[1]
        success = database_commands.disconnect_student(user)
        server_socket.sendto("Disconnected user but the virtual machine will keep running".encode("utf-8"),addr)
