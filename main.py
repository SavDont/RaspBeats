from multiprocessing import Process, Manager, Value

from mingus.midi import fluidsynth
import RPi.GPIO as GPIO

from record import *
from read_midi import *
from metronome import *
from playback import *
from volume import *

def setup_pins():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def reset_recordings(channel):
    global recordings
    metronome(recordings)

if __name__ == "__main__":
    manager = Manager()
    
    # Initialize shared variables for recordings and volumes
    recordings = manager.dict()
    volumes = manager.dict()

    # Metronome initializes the recordings with a metronome on channel 7
    metronome_proc = Process(target=metronome, args=(recordings,))
    metronome_proc.start()
    metronome_proc.join()
    
    # Sets volumes to 127 initially
    setVolumes = Process(target=set_volumes, args=(volumes,))
    setVolumes.start()
    setVolumes.join()

    setup_pins()
    GPIO.add_event_detect(17, GPIO.FALLING, callback=reset_recordings, bouncetime=300)

    # Shared variables used for communication between midi input processes
    current_channel = Value('i', 1)
    record_on = Value('i', 0)

    # Midi input processes
    akai_reader = Process(target=poll_midi_device, args=(akai_device, playback_fifo, record_fifo,current_channel, record_on, volumes))
    q49_reader = Process(target=poll_midi_device, args=(q49_device, playback_fifo, record_fifo,current_channel, record_on, volumes))

    record_playback = Process(target=playback_from_recordings, args=(recordings,volumes))
    record = Process(target=record_channel, args=(record_fifo, recordings))
    playback = Process(target=playback_from_fifo, args=(playback_fifo,volumes))

    akai_reader.start()
    q49_reader.start()
    playback.start()
    record.start()
    record_playback.start()
    
    akai_reader.join()
    q49_reader.join()
    playback.join()
    record.join()
    record_playback.join()
