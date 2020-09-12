import time

from mingus.containers import Note
from mingus.midi import fluidsynth

from constants import *
from signals import *

def metronome(recordings):
    '''
    metronome(recordings) - Takes in a dictionary and outputs a dictionary
    where keys [1,2,...,6] are empty lists and key 7 has a note played
    at the beginning of every bar
    '''
    for i in range(6):
        recordings[i+1] = []

    metronomeRec = []
    
    # Start of loop indicated by low pitched click
    note = NoteSignal("akai", 0, 64, 127, True, 7)
    metronomeRec.append(note)
    for i in range(int(beats_per_bar)-1):
        # All other clicks are higher pitched
        note = NoteSignal("akai", (60/bpm)*(i+1), 65, 127, True, 7)
        metronomeRec.append(note)

    recordings[7] = metronomeRec

if __name__ == "__main__":
    metronome()
