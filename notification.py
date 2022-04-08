import json
import subprocess
from time import sleep


def getCurrent():
    try:
        otp = subprocess.Popen('termux-notification-list', stdout=subprocess.PIPE)
        current=[]
        otp.wait()
        for n in json.loads(''.join([l.decode('utf-8').replace('\n', '') for l in otp.stdout])):
            if n['packageName'] == 'com.rhapsody.alditalk' and n['id'] != 1:
                current.append((n['content'],n['title']))
    finally:
        otp.stdout.close()
    return current



if __name__ == "__main__":
    print(getCurrent())
