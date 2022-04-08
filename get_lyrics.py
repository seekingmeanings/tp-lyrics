#!/usr/bin/env python3
import subprocess as sp
from time import asctime
from notification import getCurrent
import sys


def toast(msg, position="bottom", bc="white", tc="black"):
    sp.run(['termux-toast', '-g', position, '-b', bc, '-c', tc, msg])

#make sure the api is running
sp.run("termux-api-start")


def getLyrics(current):
    if len(current) != 1: raise IndexError("failed to get the current song name.\nGot: {}".format(current))
    try:
        with open("data/{artist}%{song}".format(artist=current[0][0],song=current[0][1]), 'r') as f:
            toast("lyrics found")
            return f.readlines()
    except FileNotFoundError:
        toast("no lyrics found")
        return False


if __name__ == "__main__":
    print(ck_lyrics(getCurrent()))
