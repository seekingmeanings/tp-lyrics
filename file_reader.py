#/usr/bin/env python3
import argparse
from subprocess import run

from math import ceil
from random import randint

from local_utils import toast

HOME_DIR="/data/data/com.termux/files/home"

def open_file(file_name:str,nid=randint(10,10000),idx=0,fp=False):
    #fp stands for full_path
    fp= False if fp is None else fp
        
    #stoopid
    idx=int(idx)
    nid=int(nid)
    
    LINES_PER_SITE=11
    SELF_CALL=f"env python3 $HOME/lyrics/file_reader.py -i {nid} -f '{file_name}'"\
        + (" -m" if fp else "") + " -p {i}"

    print(SELF_CALL)
    with open(file_name, 'r') as f:
        nums=[line for line in f]

    if len(nums) == 0:
        #importing it here 'cause it's rarly used
        from re import sub as rs
        r_e=f"^{HOME_DIR}"
        
        run(["termux-notification", "-i", str(nid), "--button1", "exit", \
             "--button1-action", f"termux-notification-remove {nid}", "-t",\
             f"file '{rs(r_e, '~', file_name)[:50]}' is empty"\
             if fp else "{} (empty cache)"\
             .format(file_name.split('/')[-1].replace('%', ' - ')),\
             "-c", '' if fp else f"file '{rs(r_e, '~', file_name)}' is empty" ],\
            check=True)
    else:
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
                 "--alert-once", "-t", file_name if fp else\
                 file_name.split('/')[-1].replace('%', ' - '), "-c",\
                 ''.join(content) ], check=True)
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--notification_id", type=int, default=randint(10,10000))
    parser.add_argument("-f", "--file_name", type=str)
    parser.add_argument("-p", "--page", type=int, default=0)
    parser.add_argument("-m", "--music_mode", action="store_true")
    args=parser.parse_args()

    open_file(file_name=args.file_name, nid=args.notification_id,\
              idx=args.page, fp=args.music_mode)
