#!/usr/bin/env python3
import subprocess as sp
import os.path
import json, re

from local_utils import toast
from file_reader import open_file

WORK_DIR="/data/data/com.termux/files/home/lyrics"
DATA_DIR=WORK_DIR + "/data"

#get the api-token
with open("/data/data/com.termux/files/home/lyrics/genius-token") as f:
    token=str().join(f.readlines())


def getCurrent():
    try:
        current=[]
        otp = sp.Popen('termux-notification-list', stdout=sp.PIPE)
        otp.wait()
        for n in json.loads(str().join([str(l.decode('utf-8').replace('\n', ''))\
                                        for l in otp.stdout])):
            if n['packageName'] == 'com.rhapsody.alditalk' and n['id'] != 1:
                current.append((n['content'],n['title']))
    finally:
        otp.stdout.close()
    
    if len(current) > 1:
        toast("to many players running")
        raise IndexError("found multiple music control notifications")
    elif len(current) == 0:
        toast("nothing is playing, couldn't search for lyrics")
        raise IndexError("failed to get the current song name.\nGot: {}".format(crt))

    try:
        fc= f"{current[0][0]}%{current[0][1]}"
        with open(f"{WORK_DIR}/name_sub.conf", 'r') as f:
            print("sylib file found")
            for i, line in enumerate(f):
                print(line)
                rp=[i.lstrip('"')  for i in re.split(r"\", \"", line)]
                print(len(rp), ":\t", rp)
                fc=re.sub(rp[0], rp[1], fc)
    except FileNotFoundError:
        print("no sub file found, skipping")
        pass
    else:
        current=[fc.split('%')]
        print(current)

    
    return (current, "{D}/{artist}%{song}".format(D=DATA_DIR,artist=current[0][0],\
                                                  song=current[0][1]))



def fetch_lyrics(current, path):
    import lyricsgenius
    
    headline=f"{current[0][1]} Lyrics"

    try:
        lapi=lyricsgenius.Genius(token, skip_non_songs=True)
        song=lapi.search_song(str(current[0][1]), str(current[0][0]))
    except ConnectionError as e:
        toast("connection to genius timed out")
        raise ConnectionError(e)
        
    try:
        if not re.match(headline + '.*', song.lyrics.splitlines()[0]):
             toast("genius sent back bullshit")
             raise RuntimeError("headlines don't match:\n- {exp}\n- {got}"\
                                .format(exp=headline,\
                                        got=song.lyrics.splitlines()[0]))
        with open(path, 'x') as f:
            f.write(song.lyrics.replace(f"{current[0][1]} Lyrics", '', 1))
        toast("lyrics fetched from genius")
    except AttributeError:
        toast("genius didn't send anything back")
        raise RuntimeError("genius api didn't open up lyrics attribute")
    except FileExistsError:
        toast('found local lyrics, cannot overwrite')
        raise RuntimeError("lyrics file found, delete it if you want to overwrite")
    

def print_lyrics(current):
    #this if statement should be in the level above
    try:
        with open("{D}/{artist}%{song}".format(D=DATA_DIR,artist=current[0][0],song=current[0][1]), 'r') as f:
            toast("lyrics found")
            return f.readlines()
    except FileNotFoundError:
        return fetch_lyrics(current)

                           
if __name__ == "__main__":
    #add argparse so current can be read from args
    crt, path=getCurrent()
    if not os.path.exists(path): fetch_lyrics(crt, path)
    open_file(path, fp=False)
    
