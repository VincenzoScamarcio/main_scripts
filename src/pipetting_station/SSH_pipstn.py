#!/usr/bin/env python

import subprocess
from subprocess import call
import opentrons

# What to modify:
# - this function can be parametrized having has single param the name of the py script to execute in pypetting station
# - migrate all the protocols to data/user_storage and check if config.json is found (as protocols will persist over power cycles & software updates)

def exec_script_SSH (protocol_name):  #add param script to run

    #Two parameters to use if I log in in WSL --> password for sudo command and random command so that I
    #can execute the command in pipetting station. If I don't use sudo I cannot run the subrocess.
    # pwd = 'vincenzo'  #pwd WSL on windows laptop
    pwd = 'simo2023'  #pwd ubuntu laptop
    cmd = 'ls'

    #Series of commands to run specific file in pipetting station

    # call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)  # This is needed only for WSL because i need to run it with sudo

    # command = "sudo ssh -i /mnt/c/Users/scamarci/ot2_ssh_key_ubuntu root@169.254.237.234".split(" ")
    #
    # command.append('systemctl start opentrons-robot-server')
    #
    # subprocess.run(command)
    #command1 = "ssh -i /mnt/c/Users/scamarci/ot2_ssh_key_ubuntu root@169.254.237.234".split(" ")  --> works on WSL

    command1 = "ssh -i ot2_ssh_key root@169.254.237.234".split(" ")   #--> works on ubuntu

    # export RUNNING_ON_PI=1

    command1.append('export RUNNING_ON_PI=1; su -c "nohup opentrons_execute "'+protocol_name)     #nohup to run the protocol even if the SSH connection is closed
    # command1.append("export RUNNING_ON_PI=1; opentrons_execute " + protocol_name)  # nohup to run the protocol even if the SSH connection is closed
    print(command1)
    # input()

    subprocess.run(command1)


if __name__ == "__main__":
    exec_script_SSH("NaCRe_test1.py")

    print("finished pipetting")