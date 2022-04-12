#!/usr/bin/env python3
from subprocess import run

NID=1
WORK_DIR="/data/data/com.termux/files/home/lyrics"

#make sure the api is running
run("termux-api-start", check=True)

run(["termux-notification", "-i", str(NID), "--ongoing", "--button1", "search lyrics",\
     "--button1-action",  f"python3 {WORK_DIR}/get_lyrics.py",\
     "-t", "fake-lyricsd is running"], check=True)
