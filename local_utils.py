#!/usr/bin/env python3
import subprocess as sp

def toast(msg, p="bottom", bc="white", tc="black"):
    sp.run(['termux-toast', '-g', str(p), '-b', str(bc), '-c', str(tc), str(msg)])

