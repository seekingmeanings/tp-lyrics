#!/usr/bin/env python3
import subprocess as sp
import os.path
import json
import re

from utils import termux_api_toast as toast
from file_reader import open_file

WORK_DIR = "/data/data/com.termux/files/home/tp-lyrics"
DATA_DIR = WORK_DIR + "/cache"

# reqd config
with open(f"{WORK_DIR}/conf.json", "r") as file:
    conf = json.load(file)


def getCurrent():
    try:
        # current = []
        otp = sp.Popen('termux-notification-list', stdout=sp.PIPE)
        otp.wait()
        # for n in json.loads(
        #        str().join([str(line.decode('utf-8').replace('\n', ''))
        #                    for line in otp.stdout])):
        #    if n['packageName'] == 'com.rhapsody.alditalk' and n['id'] != 1:
        #        current.append((n['content'], n['title']))

        current = [(n["content"], n["title"],) for n in
                   json.loads("".join(
                       [str(line.decode("utf-8").replace("\n", ""))
                        for line in otp.stdout]))
                   if any(all(n[attr] == val for attr, val in provider.items())
                          for provider in conf["player_signatures"].values())
                   ]
        
    finally:
        otp.stdout.close()

    if len(current) > 1:
        toast("to many players running")
        raise IndexError("found multiple music control notifications")
    elif len(current) == 0:
        toast("nothing is playing, couldn't search for lyrics")
        raise IndexError(f"failed to get current song name.\nGot: {current}")

    try:
        fc = f"{current[0][0]}%{current[0][1]}"
        with open(f"{WORK_DIR}/name_sub.conf", 'r') as f:
            print("sub file found")
            for i, line in enumerate(f):
                print(line)
                rp = [i.lstrip('"') for i in re.split(r"\", \"", line)]
                print(len(rp), ":\t", rp)
                fc = re.sub(rp[0], rp[1], fc)
    except FileNotFoundError:
        print("no sub file found, skipping")
        pass
    else:
        current = [fc.replace("\n", '').split('%')]
        print(current)

    return (current, "{D}/{artist}%{song}".format(D=DATA_DIR,
                                                  artist=current[0][0],
                                                  song=current[0][1]))


def fetch_lyrics(current, path):
    """
    fetch lytics from genius and store it locally
    in the coressponding file that has been given to it
    """
    import lyricsgenius

    headline = \
        f"^([0-9]+) Contributors(Translations.+)?{current[0][1]} Lyrics"
    try:
        lapi = lyricsgenius.Genius(
            conf["genius_token"],
            skip_non_songs=True,
        )
        song = lapi.search_song(str(current[0][1]), str(current[0][0]))
    except ConnectionError as e:
        toast("connection to genius timed out")
        raise ConnectionError(e)

    try:
        if not re.match(headline + '.*', song.lyrics.splitlines()[0]):
            toast("genius sent back bullshit")
            raise RuntimeError("headlines don't match:\n- {exp}\n- {got}"
                               .format(exp=headline,
                                       got=song.lyrics.splitlines()[0]))
        with open(path, 'x') as f:
            f.write(re.sub(headline, '', song.lyrics))
            #    song.lyrics.replace(f"{current[0][1]} Lyrics", '', 1))
        toast("lyrics fetched from genius")
    except AttributeError:
        toast("genius didn't send anything back")
        raise RuntimeError("genius api didn't open up lyrics attribute")
    except FileExistsError:
        toast('found local lyrics, cannot overwrite')
        raise RuntimeError("lyrics file found, delete it if you want to"
                           + " refetch automatically")


def print_lyrics(current):
    try:
        with open("{D}/{artist}%{song}".format(D=DATA_DIR,
                                               artist=current[0][0],
                                               song=current[0][1]),
                  'r') as f:
            toast("lyrics found")
            return f.readlines()
    except FileNotFoundError:
        return fetch_lyrics(current)


def main():
    # add argparse so current can be read from args
    crt, path = getCurrent()
    if not os.path.exists(path):
        fetch_lyrics(crt, path)
    open_file(path, full_path_title=False)


if __name__ == "__main__":
    main()
