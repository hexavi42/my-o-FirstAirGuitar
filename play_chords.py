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
    notes = None
    name = None

    def __init__(self, name, *args):
        self.name = name
        self.notes = args

    def play(self, duration=3):
        delay = 0
        for i in self.notes:
            subprocess.Popen(['play', '-n', 'synth', 'pluck', i, 'delay', str(delay),'fade', '0', str(duration), '.1', 'norm', '-1'], stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL)
            delay = delay + 0.01

# We can also define sharps and flats:
# G# or Gb
# All notes are relative to middle A (440 hz)

g_chord = chord('G', 'G3', 'B3', 'D3', 'G3', 'B3', 'G')
d_chord = chord('D', 'D3', 'A3', 'D4', 'F#4')
em_chord = chord('Em', 'E2', 'B2', 'E3', 'G3', 'B3', 'E4')
c_chord = chord('C', 'C3', 'E3', 'G3', 'C4', 'E4')

chord_dict = {'C': g_chord, 'D': d_chord, 'E': em_chord, 'G': c_chord}

if __name__ == "__main__":
    note = str(getch()).upper()
    while True:
        print note,
        if note in chord_dict:
            s = chord_dict[note]
            s.play()
        elif note == 'Q':
            break
        note = str(getch()).upper()
