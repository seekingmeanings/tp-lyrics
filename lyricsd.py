#!/usr/bin/env python3
import subprocess as sp
from time import asctime
from notification import getCurrent

start_time=str(asctime())
sp.run("termux-api-start")
sp.run("termux-notification --priority min -t 'lyricsd running' -c 'since {}'".format(start_time), shell=True)

