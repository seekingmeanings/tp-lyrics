#!/usr/bin/env python3
import subprocess as sp

def toast(msg, position="bottom", bc="white", tc="black"):
    sp.run(['termux-toast', '-g', position, '-b', bc, '-c', tc, str(msg)])

