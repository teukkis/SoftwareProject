import random
import socket
import sys
import os
from time import sleep
import database_commands
import file_commands
#import vm_commands

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 8080))  #receive requests here
addr = ("127.0.0.1", 8081)      #send replies here

#availableVMs = [8888, 8889]     #Available VMs (port numbers)
#inUseVMs = {}                   #Currently reserved VMs per username (port numbers)

def get_random_string(length):
    letters = "abcdefghijklmnopqrstuvwxyz1234567890-_"
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def set_passwd(port, passwd):
    print("Setting password for virtual box: {}".format(port))
    SET_PASSWD_COMMAND = "VBoxManage guestcontrol \"{}\" run /home/vagrant/work/projects/set_passwd.sh {} --username vagrant --password vagrant"
    os.system(SET_PASSWD_COMMAND.format(port, passwd))
    return True

def StartVM(port, user, passwd):
    VBOX_START_COMMAND = "VBoxManage startvm \"{}\" --type headless"
    VBOX_RUN_FILE = "VBoxManage guestcontrol \"{}\" run /home/vagrant/work/projects/mount.sh --username vagrant --password vagrant"

    HOST_MOUNT_FOLDER = "VBoxManage sharedfolder add \"{}\" --name Chip --hostpath \"/home/{}/chipwhisperer\" --transient"
    IS_VBOX_RUNNING_COMMAND = "VBoxManage showvminfo \"{}\" | grep -c \"running (since\""
    print("Starting virtualbox with name: {}".format(str(port)))
    os.system(VBOX_START_COMMAND.format(str(port)))
    sleep(1)

    print("Mounting folder: /home/{}/chipwhisperer into the virtual machine".format(user))
    os.system(HOST_MOUNT_FOLDER.format(str(port), user))
    tries = 0
    success = False
    while tries < 20:
        sleep(1)
        tries += 1
        if os.system(VBOX_RUN_FILE.format(str(port))) == 0:
            success = True
            break

    if not success:
        FreeVM(user)
        print("Error starting the vm")
        return False

    print("Mounting the folder into correct directory")
    #os.system(VBOX_RUN_FILE.format(str(port)))
    
    set_passwd(port, passwd)
    print("Done")
    return True

def CloseVM(port):
    VBOX_CLOSE_COMMAND = "vboxmanage controlvm \"{}\" acpipowerbutton"
    os.system(VBOX_CLOSE_COMMAND.format(port))

def GiveVM(user, passwd):    
    success, new_user = database_commands.set_student_on_vm(user)
    if success:
        if new_user:
            return StartVM(success,user,passwd)
        return set_passwd(success, passwd)
    return success

    #if not inUseVMs.get(user, None):
        #if len(availableVMs)>0:
            #inUseVMs[user] = availableVMs.pop()
            #StartVM(inUseVMs[user], user)
        #else:
            #return "Unfortunately, all virtual machines are currently reserved."

    #return str(inUseVMs[user])

#Release a VM that is reserved to a user
def FreeVM(user):
    success = database_commands.free_student_from_vm(user)
    if success:
        CloseVM(success)
    return success

#Wait for packets, then return a VM for them if available
while True:
    message, address = server_socket.recvfrom(1024)
    message = message.decode("utf-8")
    print(message)
    if "Connect:" in message:
        user = message.split(':')[1]
        passwd = get_random_string(8)
        success = GiveVM(user, passwd)
        if success:
            server_socket.sendto("You need to forward this port in your Putty settings: {}\nYour Jupyter Notebook password is: {}".format(success,passwd).encode("utf-8"),addr)
        else:
            server_socket.sendto("Error while trying to assign a virtual machine. Please contact your teacher.".encode("utf-8"),addr)
    elif "Disconnect:" in message:
        user = message.split(':')[1]
        success = FreeVM(user)
        server_socket.sendto("Disconnected".encode("utf-8"),addr)
        if not success == False:
            print("Succesfully disconnected user")
        else:
            print("Error in disconnecting user")
    elif "User_left:" in message:
        user = message.split(':')[1]
        success = database_commands.disconnect_student(user)
        server_socket.sendto("Disconnected user but the virtual machine will keep running".encode("utf-8"),addr)
