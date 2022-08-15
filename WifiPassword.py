import subprocess
import time, os, sys, getpass
from sys import platform, setrecursionlimit
import os

try:
    import pexpect
except ModuleNotFoundError:
    if platform=="win32":
        pass
    elif platform=="linux" or platform=="linux2":
        pass
    else:
        pass

def windows():
    localtime = time.asctime( time.localtime(time.time()))
    data = subprocess.check_output(['netsh','wlan','show','profiles']).decode('utf-8').split('\n')
    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
    file = open("result.txt", "a")
    print("\n[+] Wifi Grabber: " + localtime + "\n")
    file.write("\n[+] Wifi Grabber: " + localtime + "\n")
    print("========================================================",file=file)
    print(localtime, file=file)
    print("========================================================",file=file)
    file.close
    for i in profiles:
        results = subprocess.check_output(['netsh','wlan','show','profile',i,
                                        'key=clear']).decode("utf-8").split('\n')
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        try:
            print("{:<30} | {:<}".format(i, results[0]),file=file)
            file.close
        except IndexError:
            print("{:<30} | {:<}".format(i, ""))

    time.sleep(3)
    sys.exit(1)

def linux():
    file = open("resultlinux.txt", 'a')
    localtime = time.asctime(time.localtime(time.time()))
    # data = subprocess.check_output(['sudo','iwlist','wlan0','scan']).decode('utf-8').split('\n')
    #command = "sudo cat /etc/NetworkManager/system-connections/* | egrep 'id=*|psk'".split('\n')
    #os.system(command)
    child = pexpect.spawn("/usr/bin/su root")
    u = getpass.getuser()
    username = input("Masukan Username (root,{}) = ".format(u))
    child = pexpect.spawn("/usr/bin/su {}".format(username))
    child.logfile_read = sys.stdout.buffer
    #child.expect("Password : ")
    #time.sleep(3)
    password = input("Masukan Password : ")
    child.sendline(password)
    child.expect("#")
    #child.sendline("whoami")
    child.sendline("echo [+] Wifi Grabber: $(date) >> resultlinux.txt")
    #child.expect("create new line")
    child.expect("#")
    child.sendline("echo '\n' >> resultlinux.txt")
    #child.expect("#")
    child.expect("#")
    child.sendline("cat /etc/NetworkManager/system-connections/* | egrep 'id=*|psk' >> resultlinux.txt")
    child.expect("#")
    child.sendline("echo '\n' >> resultlinux.txt")
    child.expect("#")
    print("file sudah tersimpan dengan nama resultlinux.txt")


def main():
    if platform=="win32":
        windows()
    elif platform=="linux" or platform=="linux2":
        linux()
    else:
        sys.exit(1)

if __name__ == "__main__":
    setrecursionlimit(5000)
    main()
#========================================
