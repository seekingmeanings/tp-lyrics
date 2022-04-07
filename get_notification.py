import json
import subprocess


subprocess.run("termux-api-start")

json_not= subprocess,Popen("termux-notifications-list", stdout=subprocess.PIPE)

print(json_not)
