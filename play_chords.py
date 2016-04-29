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

    def play(self, duration=3, delay_inc=0.015):
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

    def reverse(self):
        return chord(self.name, *list(reversed(list(self.notes))))

    def stop(self):
        for string in self.ringing:
            os.killpg(os.getpgid(string.pid), signal.SIGTERM)
        self.ringing = []


class Guitar(object):
    strings = ['E2', 'A2', 'D3', 'G3', 'B3', 'E4']
    scale = ["A", "A#", 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    ringing = [None for string in strings]
    capo = 0
    over = 0
    gain = 0
    sustain = 0
    DEVNULL = open(os.devnull, 'wb')

    def __init__(self, tuning=None, overdrive=0, gain=-40, sus=3):
        if tuning is not None:
            self.tune(tuning)
        self.over = overdrive
        self.gain = gain
        self.sustain = sus

    def strum_chord(self, notes, up=False, delay_inc=0.015, power=0):
        assert isinstance(notes, list) and isinstance(notes[0], str),\
            "{0} is not a list of strings.".format(notes)
        delay = 0 + len(self.strings) * delay_inc * up
        way = 1 * -up
        for index in range(len(self.strings)):
            if notes[index] == "X":
                if self.ringing[index] is not None:
                    self.mute_string(index)
            elif notes[index] == "S":
                # just here for symbolism - sometimes we want to sustain notes
                # while changing chords, and using S the note spot supports it
                pass
            else:
                if self.ringing[index] is not None:
                    self.mute_string(index)
                self.ringing[index] = \
                    subprocess.Popen(['play', '-n', 'synth', 'pluck',
                                      notes[index], 'delay', str(delay),
                                      'fade', '0', str(self.sustain), '.1',
                                      'overdrive', str(self.over),
                                      'gain', '-e', str(self.gain+20*power),
                                      'norm', '-1'], stdin=self.DEVNULL,
                                     stdout=self.DEVNULL, stderr=self.DEVNULL,
                                     preexec_fn=os.setsid)
                delay = delay + delay_inc

    # frets should be a list of strings to allow for X's on not played notes
    def strum_fret(self, frets=None, up=False, delay_inc=0.015, power=0):
        if frets is not None:
            assert isinstance(frets, list) and isinstance(frets[0], str),\
                "{0} is not a list of strings.".format(frets)
            # turn that sucker into a list of notes instead, using capo and scale
            # as the other other inputs - X gets muted, S gets sustained
            notes = self.fret_to_notes(frets)
            self.strum_chord(notes, power=power)

    def tune(tuning):
        # assert something about tuning char set here too
        assert isinstance(tuning, list), \
            "Tuning is not a list - how am I tuning to {0}?".format(tuning)
        if isinstance(tuning[0], str):
            self.strings = tuning
        elif isinstance(tuning[0], int):
            pass
        else:
            raise ValueError("We don't handle {0} as tuning!".format(tuning))

    def set_distortion(self, dist_int):
        self.over = dist_int

    def silence(self):
        for index in range(len(self.ringing)):
            self.mute_string(index)

    def mute_string(self, index):
        try:
            os.killpg(os.getpgid(self.ringing[index].pid), signal.SIGTERM)
            self.ringing[index] = None
        except:
            pass

    def inc_to_note(self, old_note, inc):
        # split string tuning into note and number
        # go up scale to current position for note name,
        # resetting to A after G# and inc number if nes
        noteName = old_note[:-1]
        noteNum = int(old_note[-1])
        note = "{0}{1}".format(
                    self.scale[(self.scale.index(noteName) + inc) % len(self.scale)],
                    noteNum + inc / len(self.scale)
                )
        return note

    def fret_to_notes(self, frets):
        notes = []
        for ind in range(len(frets)):
            f = frets[ind]
            if f == "X" or f == "S":
                notes.append(f)
            else:
                try:
                    inc = int(f) if f != '0' else self.capo
                except:
                    raise ValueError("{0} is not a fret character!".format(f))
                else:
                    notes.append(self.inc_to_note(self.strings[ind],inc))
        return notes

# We can also define sharps and flats:
# G# or Gb
# All notes are relative to middle A (440 hz)

g_chord = chord('G', 'G2', 'B3', 'D3', 'G3', 'B3', 'G4')
d_chord = chord('D', 'D3', 'A3', 'D4', 'F#4')
em_chord = chord('Em', 'E2', 'B2', 'E3', 'G3', 'B3', 'E4')
c_chord = chord('C', 'C3', 'E3', 'G3', 'C4', 'E4')

chord_dict = {'A': g_chord, 'S': d_chord, 'D': em_chord, 'F': c_chord,
              'Z': g_chord.reverse(), 'X': d_chord.reverse(),
              'C': em_chord.reverse(), 'V': c_chord.reverse()}

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
