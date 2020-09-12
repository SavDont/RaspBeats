import sys
import time
import threading

from mingus.containers import Note
from mingus.midi import fluidsynth

from signals import *
from constants import *


def fluidsynth_init():
    '''
    fluidsynth_init - initializes fluidsynth to the soundfont file and sets the
    instrument for each channel according to the list in constants.py
    '''
    fluidsynth.init(general_soundfont, "alsa")
    for i in instruments:
        fluidsynth.set_instrument(i[0], i[1], i[2])

def playback_from_fifo(fifo, volumes):
    '''
    playback_from_fifo(fifo, volumes) - Continuously reads from the fifo given and
    plays the notes upon read
    '''
    fluidsynth_init()
    while True:
        with open(fifo) as f:
            for line in f:
                # First regex match whether we have a note_on or note_off event
                if rgx_note_on.match(line):
                    m = rgx_note_on.match(line)
                    obj = NoteSignal("akai", time.time(),int(m.group(2)), int(m.group(3)),True,int(m.group(1)))
                    obj.play(volumes[int(m.group(1))]) # Play at volume specified for channel
                elif rgx_note_off.match(line):
                    m = rgx_note_off.match(line)
                    obj = NoteSignal("akai",time.time(), int(m.group(2)), int(m.group(3)),False, int(m.group(1)))
                    obj.play(volumes[int(m.group(1))]) # Play at volume specified for channel

def playback_from_recordings(recordings, volumes):
    '''
    playback_from_recordings(recordings, volumes) - Takes in dictionaries of recordings and volumes
    and plays the notes on repeat
    '''
    fluidsynth_init()

    while True:
        start = time.time() # start of current loop
        
        # cur_notes used to keep track of notes currently on in the loop
        cur_notes = [0 if recordings[x+1] else -1 for x in range(len(recordings))]
        
        # loop for record_length specified
        while time.time() - start < record_length:
            # iterate through every channel
            for i in range(len(recordings)):
                cur_note = cur_notes[i]
                # if we are past the current notes start time, play the note
                if cur_note > -1 and cur_note < len(recordings[i+1]) and time.time() - start >= recordings[i+1][cur_note].midi_time:
                    cur_volume = volumes[recordings[i+1][cur_note].channel]
                    recordings[i+1][cur_note].play(cur_volume)
                    cur_notes[i] += 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("Incorrect number of arguments. Please enter device name")
        exit(1)
    elif sys.argv[1] == "akai":
        playback_from_fifo("akai", akai_playback_fifo)
    elif sys.argv[1] == "q49":
        playback_from_fifo("q49", q49_playback_fifo)
