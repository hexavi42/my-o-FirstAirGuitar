#!/usr/bin/env python

import subprocess
from getch import getch
import os
from time import sleep

# You need to install SoX - Sound eXchange
# homebrew install:
# http://brewformulas.org/Sox
# sourceforge:
# http://sox.sourceforge.net/
# Other ways to install:
# http://superuser.com/questions/279675/installing-sox-sound-exchange-via-the-terminal-in-mac-os-x
# Usage:
# http://sox.sourceforge.net/sox.html

DEVNULL = open(os.devnull, 'wb')

class chord:

    def __init__(self, *args):
        self.notes = args
    def play(self, duration=3):
        for i in self.notes:
            subprocess.Popen(['play', '-n', 'synth', str(duration) , 'pluck', i], stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL)

# We can also define sharps and flats:
# G# or Gb
# All notes are relative to middle A (440 hz)
notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

note = str(getch()).upper()
while True:
    print note,
    if note in notes:
        s = chord(note)
        s.play()
    elif note == 'Q':
        break
    note = str(getch()).upper()
