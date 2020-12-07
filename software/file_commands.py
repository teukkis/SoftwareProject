import os
import subprocess
import traceback
import sys

def run_sudo(cmd):
    sudo_pass = "SoftwareProject"
    sudo_pass_cmd = subprocess.Popen(['echo', sudo_pass], stdout=subprocess.PIPE)
    p=subprocess.Popen(["sudo","-S"] + cmd,stdin=sudo_pass_cmd.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    output = output.strip().decode("utf-8")
    error = error.decode("utf-8")
    if p.returncode !=0:
        return error, False
    return output, True

def run(cmd):
    p=subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    output = output.strip().decode("utf-8")
    error = error.decode("utf-8")
    if p.returncode !=0:
        return error, False
    return output, True

def create_user(username):
    cmd = ["useradd","-g", "student", "-d", "/home/"+username, "-m", username]
    return run_sudo(cmd)

def delete_user(username):
    cmd = ["userdel", "-r", username]
    return run_sudo(cmd)

def set_ssh_key(username, key):
    ssh_folder = "/home/{}/.ssh".format(username)
    if not os.path.exists(ssh_folder):
        cmd = [ "mkdir", ssh_folder]
        output, success = run_sudo(cmd)
        if not success:
            return output, False
        cmd = ["chmod", "700", ssh_folder]
        output, success = run_sudo(cmd)
        if not success:
            return output, False
        cmd = ["chown", username, ssh_folder]
        output, success = run_sudo(cmd)
        if not success:
            return output, False
    key_file = ssh_folder+"/authorized_keys"
    with open("tmp_keys","w") as f:
        f.seek(0)
        f.write(key)
        f.truncate()
        
    cmd = ["mv", "tmp_keys", key_file]
    output, success = run_sudo(cmd)
    if not success:
        return output, False
    cmd = ["chmod", "600", key_file]
    output, success = run_sudo(cmd)
    if not success:
        return output, False
    cmd = ["chown", username, key_file]
    output, success = run_sudo(cmd)
    if not success:
        return output, False
    
    return "Added key file succesfully", True
    
def copy_chip_folder(username):
    user_folder = "/home/{}/".format(username)
    cmd = ["cp", "-r", "/home/developer/Software/chipwhisperer", user_folder]
    output,success = run_sudo(cmd)
    return output, success

def add_student(username, key):
    output, success = create_user(username)
    if not success:
        return output, False
    
    output, success = set_ssh_key(username, key)
    if not success:
        return output, False
    
    bashrc_file = "/home/{}/.bashrc".format(username)
    cmd = ["echo", "python /home/developer/Software/start.py", ">>", bashrc_file]
    output,success = run_sudo(cmd)
    if not success:
        return output, False
    
    output, success = copy_chip_folder(username)
    if not success:
        return output, False
    return "Succesfully added user", True
if __name__ == "__main__":
    if len(sys.argv)>2:
        print(add_student(sys.argv[1], sys.argv[2]))
    else:
        print(delete_user(sys.argv[1]))
