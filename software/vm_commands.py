import sys
import os
from time import sleep

def set_passwd(port, passwd):
    print("Setting password for virtual box: {}".format(port))
    SET_PASSWD_COMMAND = "VBoxManage guestcontrol \"{}\" run /home/vagrant/start_jupyter.py {} --username vagrant --password vagrant"
    os.system(SET_PASSWD_COMMAND.format(port, passwd))
    return port, passwd

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
        print("Error starting the vm")
        return False, ""

    print("Mounting the folder into correct directory")
    #os.system(VBOX_RUN_FILE.format(str(port)))
    
    set_passwd(port, passwd)
    print("Done")
    return port, passwd

def CloseVM(port):
    VBOX_CLOSE_COMMAND = "VBoxManage controlvm \"{}\" acpipowerbutton"
    os.system(VBOX_CLOSE_COMMAND.format(port))