#!/usr/bin/env python

import os
import signal
import subprocess
from getch import getch
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


class chord(object):
    notes = None
    name = None
    ringing = []

    def __init__(self, name, *args):
        self.name = name
        self.notes = args
        if "reverse" not in name:
            self.reverse = chord(self.name+"_reverse", *list(reversed(list(self.notes))))

    def play(self, duration=3, delay_inc=0.011):
        delay = 0
        for i in self.notes:
            if i == "X":
                pass
            else:
                self.ringing.append(
                    subprocess.Popen(['play', '-n', 'synth', 'pluck', i, 'delay',
                                     str(delay), 'fade', '0', str(duration), '.1',
                                     'norm', '-1'], stdin=DEVNULL, stdout=DEVNULL,
                                     stderr=DEVNULL, preexec_fn=os.setsid))
                delay = delay + delay_inc

    def stop(self):
        for string in self.ringing:
            os.killpg(os.getpgid(string.pid), signal.SIGTERM)
        self.ringing = []


class guitar(object):
    strings = ['E2', 'A2', 'D3', 'G3', 'B3', 'E4']
    scale = ["A", "A#", 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    ringing = [None for string in strings]
    capo = 0

    def __init__(self, tuning=None):
        # assert something about tuning here
        if tuning is not None:
            self.tune(tuning)

    def strum_chord(self, notes, up=False, delay_inc=0.015):
        assert isinstance(notes, list) and isinstance(notes[0], str),\
            "{0} is not a list of strings.".format(notes)
        delay = 0 + len(strings) * delay_inc * up
        way = 1 * -up
        for index in range(len(strings)):
            if notes[index] == "X":
                if ringing[index] is not None:
                    mute_string(string)
            elif notes[index] == "S":
                # just here for symbolism - sometimes we want to sustain notes
                # while changing chords, and using S the note spot supports it
                pass
            else:
                if ringing[index] is not None:
                    mute_string(string)
                self.ringing[index] = \
                    subprocess.Popen(['play', '-n', 'synth', 'pluck',
                                      notes[index], 'delay', str(delay),
                                      'fade', '0', str(duration), '.1',
                                     'norm', '-1'], stdin=DEVNULL,
                                     stdout=DEVNULL, stderr=DEVNULL,
                                     preexec_fn=os.setsid)
                delay = delay + delay_inc

    # frets should be a list of strings to allow for X's on not played notes
    def strum_fret(self, frets=None, up=False, delay_inc=0.015):
        assert isinstance(notes, list) and isinstance(notes[0], str),\
            "{0} is not a list of strings.".format(frets)
        # turn that sucker into a list of notes instead, using capo and scale
        # as the other other inputs
        notes = self.fret_to_notes(frets)
        self.strum_chord(notes)

    def tune(tuning):
        assert isinstance(tuning, list), \
            "Tuning is not a list - how am I tuning to {0}?".format(tuning)
        if isinstance(tuning[0], str):
            self.strings = tuning
        elif isinstance(tuning[0], int):
            pass
        else:
            raise ValueError("We don't handle {0} as tuning!".format(tuning))

    def silence(self):
        for index in range(len(self.ringing)):
            self.mute_string(index)

    def mute_string(self, index):
        try:
            os.killpg(os.getpgid(self.ringing[index].pid), signal.SIGTERM)
            self.ringing[index] = None
        except:
            pass

    def fret_to_notes(self, frets):
        notes = []
        for f in frets:
            curr_pos = f+self.capo
            # more here later

# We can also define sharps and flats:
# G# or Gb
# All notes are relative to middle A (440 hz)

g_chord = chord('G', 'G2', 'B2', 'D3', 'G3', 'B3', 'G4')
d_chord = chord('D', 'D3', 'A3', 'D4', 'F#4')
em_chord = chord('Em', 'E2', 'B2', 'E3', 'G3', 'B3', 'E4')
c_chord = chord('C', 'C3', 'E3', 'G3', 'C4', 'E4')

chord_dict = {'A': g_chord, 'S': d_chord, 'D': em_chord, 'F': c_chord,
              'Z': g_chord.reverse, 'X': d_chord.reverse,
              'C': em_chord.reverse, 'V': c_chord.reverse}

if __name__ == "__main__":
    s = None
    note = str(getch()).upper()
    while True:
        print note,
        if note in chord_dict:
            if s:
                try:
                    s.stop()
                except:
                    pass
            s = chord_dict[note]
            s.play()
        elif note == 'M':
            if s:
                try:
                    s.stop()
                except:
                    pass
        elif note == 'Q':
            break
        note = str(getch()).upper()
