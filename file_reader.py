#/usr/bin/env python3
import argparse

from subprocess import run

from math import ceil
from random import randint


def open_file(file_name:str,nid=randint(10,10000),idx=0):

    idx=int(idx)
    nid=int(nid)
    
    LINES_PER_SITE=11
    SELF_CALL=f"env python3 $HOME/lyrics/file_reader.py -i {nid} -f '{file_name}'"\
        + " -p {i}"

    with open(file_name, 'r') as f:
        nums=[line for line in f]
        
        _ceiled_val=ceil(int(len(nums) / LINES_PER_SITE))
        if idx < 0:
            raise IndexError("index is negative")
        elif idx > _ceiled_val:
            raise IndexError("index out of range")
        elif idx == _ceiled_val:
            #that means. that the list is smaller than the screen
            #so the index for the print has to be set to max
            content=nums[idx*LINES_PER_SITE:]
        else:
            content=nums[idx*LINES_PER_SITE:(idx+1)*LINES_PER_SITE]
            
            
            run(["termux-notification", "-i", str(nid),  "--button1", "previous",\
                 "--button1-action", SELF_CALL.format(i=idx-1), "--button2", "next",\
                 "--button2-action", SELF_CALL.format(i=idx+1), "--button3", "exit", \
                 "--button3-action", f"termux-notification-remove {nid}",\
                 "--ongoing", "-t", file_name, "-c", ''.join(content) ])
            
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--notification_id", type=int, default=randint(10,10000))
    parser.add_argument("-f", "--file_name", type=str)
    parser.add_argument("-p", "--page", type=int, default=0)
    args=parser.parse_args()

    open_file(file_name=args.file_name, nid=args.notification_id,idx=args.page)
