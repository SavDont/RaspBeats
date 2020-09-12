import time

from constants import *
from read_signals import *
from mingus.midi import fluidsynth

PATH_TO_FIFO = "/home/pi/ECE5725-Final/akai_fifo"

fluidsynth.init("/home/pi/ECE5725-Final/sound_fonts/gen.sf2", "alsa")
fluidsynth.set_instrument(1, 13, 0)
track = []

def record():
    time.sleep(3)
    print ("start")
    start = time.time()
    recording = True
    while recording:
        with open(PATH_TO_FIFO) as fifo:
            for line in fifo:
                if reControlChange.match(line):
                    recording = False
                    break
                else:
                    if reNoteOn.match(line):
                        m = reNoteOn.match(line)
                        obj = NoteSignal("akai",time.time()-start,int(m.group(2)),int(m.group(3)),True)
                        track.append(obj)
                        obj.play()
                    if reNoteOff.match(line):
                        m = reNoteOff.match(line)
                        obj = NoteSignal("aka", time.time()-start, int(m.group(2)), int(m.group(3)),False)
                        track.append(obj)
                        obj.play()

def play():
    while True:
        start = time.time() - 0.1
        idx = 0
        while idx < len(track):
            if time.time() - start >= track[idx].midi_time:
                track[idx].play()
                idx += 1

if __name__ == "__main__":
    record()
    play()
