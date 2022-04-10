#!/usr/bin/env python3
import subprocess as sp
from time import asctime
import sys
import json
import lyricsgenius

from local_utils import toast


DATA="/data/data/com.termux/files/home/lyrics/data"

#get the api-token
with open("/data/data/com.termux/files/home/lyrics/genius-token") as f:
    token=str().join(f.readlines())


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

def fetch_lyrics(current):
    lapi=lyricsgenius.Genius(token, skip_non_songs=Truep)
    song=lapi.search_song(str(current[0][1]), str(current[0][0]))

    try:
        with open("{D}/{artist}%{song}".format(D=DATA,artist=current[0][0],song=current[0][1]), 'w') as f:
            f.write(song.lyrics)
    except AttributeError:
        toast("genius didn't send anything back")
        return False
    toast("lyrics fetched")
    return song.lyrics


def getLyrics(current):
    #this if statement should be in the level above
    if len(current) != 1: raise IndexError("failed to get the current song name.\nGot: {}".format(current))
    try:
        with open("{D}/{artist}%{song}".format(D=DATA,artist=current[0][0],song=current[0][1]), 'r') as f:
            toast("lyrics found")
            return f.readlines()
    except FileNotFoundError:
        return fetch_lyrics(current)


if __name__ == "__main__":
    print(getLyrics(getCurrent()))
