import sys
import os
from time import sleep
def startVM(vm, folder):
    VBOX_START_COMMAND = "VBoxManage startvm \"{}\" --type headless"
    VBOX_RUN_FILE = "VBoxManage guestcontrol \"{}\" run /home/vagrant/work/projects/mount.sh --username vagrant --password vagrant"

    HOST_MOUNT_FOLDER = "VBoxManage sharedfolder add \"{}\" --name Chip --hostpath \"{}\" --transient"


    print("Starting virtualbox with name: {}".format(vm))
    os.system(VBOX_START_COMMAND.format(vm))
    sleep(1)

    print("Mounting folder: {} into the virtual machine".format(folder))
    os.system(HOST_MOUNT_FOLDER.format(vm,folder))
    sleep(10)

    print("Mounting the folder into correct directory")
    os.system(VBOX_RUN_FILE.format(vm))

    print("Done")
    return True
