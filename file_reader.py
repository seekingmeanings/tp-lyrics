#/usr/bin/env python3
import sys
from subprocess import run
from math import ceil


file_name="/data/data/com.termux/files/home/lyrics/numbers"
lines_per_site=11
notification_id=3933

def create_not(content):
    run(["termux-notification", "-i", str(notification_id),  "--button1", "previous", "--button1-action",\
         "env python3 $HOME/lyrics/n_reader.py {}".format(idx-1), "--button2", "next", "--button2-action", \
         "env python3 $HOME/lyrics/n_reader.py {}".format(idx+1), "--button3", "exit", "--button3-action", \
         "termux-notification-remove {}".format(notification_id), "-t", file_name, "-c", ''.join(content) ])

with open(file_name, 'r') as f:
    nums=[line for line in f]
try:
    idx=int(sys.argv[1])
except IndexError:
    idx=0

_ceiled_val=ceil(int(len(nums) / lines_per_site))
if idx < 0:
    raise IndexError("index is negative")
elif idx > _ceiled_val:
    raise IndexError("index out of range")
elif idx == _ceiled_val:
    #that means. that the list is smaller than the screen
    #so the index for the print has to be set to max
    create_not(nums[idx*lines_per_site:])
else:
    create_not(nums[idx*lines_per_site:(idx+1)*lines_per_site])


    
