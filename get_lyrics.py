#!/usr/bin/env python3
import subprocess as sp
from time import asctime
import sys
import json

#make sure the api is running
sp.run("termux-api-start", check=True)


def toast(msg, position="bottom", bc="white", tc="black"):
    sp.run(['termux-toast', '-g', position, '-b', bc, '-c', tc, msg])


def getCurrent():
    try:
        current=[]
        otp = sp.Popen('termux-notification-list', stdout=sp.PIPE)
        
        otp.wait()
        for n in json.loads(str().join([str(l.decode('utf-8').replace('\n', '')) for l in otp.stdout])):
            if n['packageName'] == 'com.rhapsody.alditalk' and n['id'] != 1:
                current.append((n['content'],n['title']))
    finally:
        otp.stdout.close()
    return current



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
    print(getLyrics(getCurrent()))
