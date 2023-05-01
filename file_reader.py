#!/usr/bin/env python3

import argparse
from subprocess import run

from math import ceil
from random import randint

HOME_DIR = "/data/data/com.termux/files/home"
DEBUG = False


def open_file(file_name: str, nid: int,
              page_idx: int = 0, full_path_title: bool = False):
    LINES_PER_SITE = 11
    SELF_CALL = "python3 $HOME/tp-lyrics/file_reader.py " +\
        f"-i {nid} -f '{file_name}'" +\
        (" -m" if full_path_title else "") + " -p {i}" +\
        (" >$HOME/tpl.log 2>&1" if DEBUG else "")

    with open(file_name, 'r') as f:
        file_content = [line for line in f]

    if len(file_content) == 0:
        # the file is empty

        # importing it here 'cause it's rarly used
        from re import sub as rs
        r_e = f"^{HOME_DIR}"

        run(["termux-notification", "-i", str(nid), "--button1", "exit",
             "--button1-action", f"termux-notification-remove {nid}", "-t",
             f"file '{rs(r_e, '~', file_name)[:50]}' is empty"
             if full_path_title else "{} (empty cache)"
             .format(file_name.split('/')[-1].replace('%', ' - ')),
             "-c", '' if full_path_title
             else f"file '{rs(r_e, '~', file_name)}' is empty"],
            check=True)
    else:
        pages_in_file = ceil(int(len(file_content) / LINES_PER_SITE))
        if page_idx < 0 or page_idx > pages_in_file:
            raise IndexError("index OOR")

            # that means. that the list is smaller than the screen
            # so the index for the print has to be set to max
        content = file_content[page_idx*LINES_PER_SITE:]\
            if page_idx == pages_in_file\
            else file_content[page_idx*LINES_PER_SITE:(page_idx+1)*LINES_PER_SITE]

        print(SELF_CALL.format(i=page_idx))
        run(["termux-notification", "-i", str(nid),
             "--button1", "previous",
             "--button1-action", SELF_CALL.format(i=page_idx-1),
             "--button2", "next",
             "--button2-action", SELF_CALL.format(i=page_idx+1),
             "--button3", "exit",
             "--button3-action", f"termux-notification-remove {nid}",
             "--alert-once",
             "-t", file_name if full_path_title else
             file_name.split('/')[-1].replace('%', ' - '),
             "-c", ''.join(content)],
            check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--notification_id", type=int,
                        default=randint(10, 10000))
    parser.add_argument("-f", "--file_name", type=str)
    parser.add_argument("-p", "--page", type=int, default=0)
    parser.add_argument("-m", "--music_mode", action="store_true")
    args = parser.parse_args()

    open_file(file_name=args.file_name, nid=int(args.notification_id),
              page_idx=int(args.page), full_path_title=args.music_mode)
