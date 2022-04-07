import json
import subprocess


#subprocess.run("termux-api-start")

json_not = subprocess.Popen('termux-notification-list', stdout=subprocess.PIPE)

true_json = json.loads(''.join([l.decode('utf-8').replace('\n', '') for l in json_not.stdout]))
json_not.stdout.close()


print(true_json[0].keys())
