import os

def shutdown():
    os.system("/usr/bin/sudo /sbin/shutdown -h now")

def reboot():
    os.system("/usr/bin/sudo /sbin/shutdown -r now")
