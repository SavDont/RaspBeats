import time

from signals import *
from mingus.midi import fluidsynth

from constants import *

def record_channel(record_fifo, recordings):
    '''
    record_channel(record_fifo, recordings) - Continuously reads from record_fifo and updates
    appropriate channel in recordings dictionary to reflect that
    '''
    current_recording = []
    start = None
    while True:
        with open(record_fifo) as f:
            for line in f:
                if rgx_record_start.match(line):
                    print("Record Started in Record")
                    m = rgx_record_start.match(line)
                    # Set channel recordings and current recording to empty list and timestamp the start of recording
                    recordings[int(m.group(1))] = []
                    current_recording = []
                    start = time.time()
                elif rgx_record_stop.match(line):
                    print("Record Stopped in Record")
                    m = rgx_record_stop.match(line)
                    # Set channel recording to current recording
                    recordings[int(m.group(1))] = current_recording
                elif rgx_note_on.match(line):
                    # Append note_on events to current recording timestamped from start of recording
                    m = rgx_note_on.match(line)
                    note = NoteSignal("akai", time.time()-start, int(m.group(2)), int(m.group(3)), True, int(m.group(1)))
                    current_recording.append(note)
                elif rgx_note_off.match(line):
                    # Append note_off events to current recording timestamped from start of recording
                    m = rgx_note_off.match(line)
                    note = NoteSignal("akai", time.time()-start, int(m.group(2)), int(m.group(3)), False, int(m.group(1)))
                    current_recording.append(note)

if __name__ == "__main__":
    record_track(akai_record_fifo)
