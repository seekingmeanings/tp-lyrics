#!/usr/bin/env python3

import argparse
from subprocess import run

from math import ceil
from random import randint

from utils import termux_api_toast as toast

HOME_DIR = "/data/data/com.termux/files/home"


def open_file(file_name: str, nid: int,
              idx: int = 0, fp: bool = False):
    # fp stands for full_path
    
    LINES_PER_SITE = 11
    SELF_CALL = "env python3 $HOME/lyrics/file_reader.py " +\
        f"-i {nid} -f '{file_name}'"\
        + (" -m" if fp else "") + " -p {i}"

    print(SELF_CALL)
    with open(file_name, 'r') as f:
        nums = [line for line in f]

    if len(nums) == 0:
        # importing it here 'cause it's rarly used
        from re import sub as rs
        r_e = f"^{HOME_DIR}"
        
        run(["termux-notification", "-i", str(nid), "--button1", "exit",
             "--button1-action", f"termux-notification-remove {nid}", "-t",
             f"file '{rs(r_e, '~', file_name)[:50]}' is empty"
             if fp else "{} (empty cache)"
             .format(file_name.split('/')[-1].replace('%', ' - ')),
             "-c", '' if fp else f"file '{rs(r_e, '~', file_name)}' is empty"],
            check=True)
    else:
        _ceiled_val = ceil(int(len(nums) / LINES_PER_SITE))
        if idx < 0 or idx > _ceiled_val:
            raise IndexError("index OOR")

        if idx == _ceiled_val:
            # that means. that the list is smaller than the screen
            # so the index for the print has to be set to max
            content = nums[idx*LINES_PER_SITE:]
        else:
            content = nums[idx*LINES_PER_SITE:(idx+1)*LINES_PER_SITE]

        toast(content)
        
        # really inside of the if else statement?
        run(["termux-notification", "-i", str(nid),
             "--button1", "previous",
             "--button1-action", SELF_CALL.format(i=idx-1),
             "--button2", "next",
             "--button2-action", SELF_CALL.format(i=idx+1),
             "--button3", "exit",
             "--button3-action", f"termux-notification-remove {nid}",
             "--alert-once",
             "-t", file_name if fp else
             file_name.split('/')[-1].replace('%', ' - '),
             "-c", ''.join(content)],
            check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--notification_id", type=int, default=randint(10,10000))
    parser.add_argument("-f", "--file_name", type=str)
    parser.add_argument("-p", "--page", type=int, default=0)
    parser.add_argument("-m", "--music_mode", action="store_true")
    args = parser.parse_args()

    open_file(file_name=args.file_name, nid=int(args.notification_id),
              idx=int(args.page), fp=args.music_mode)
