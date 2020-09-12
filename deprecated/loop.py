from signals import *
from mingus.midi import fluidsynth
from constants import *

import RPi.GPIO as GPIO
import time
import mido
import multiprocessing

recordMode = False
startRecordTime = 0.0
track1 = []
recordLength = 10.0


bpm = 100
bars = 4
beats = 4

def read_akai(synth):
    global recordMode
    global startRecordTime
    global track1
    global recordLength

    with mido.open_input(u'MPK Mini Mk II:MPK Mini Mk II MIDI 1 20:0') as inport:
        for msg in inport:
            #print(msg)
            if msg.type == "note_on" or msg.type == "note_off":
                obj = NoteSignal("akai", time.time(), msg.note, msg.velocity, msg.type == "note_on")
                obj.play(synth)

            if recordMode and (time.time() - startRecordTime > recordLength):
                print("Record Mode Turned Off")
                recordMode = False
            elif recordMode:
                print("Record Event")
                track1.append((time.time()-startRecordTime, obj))
'''
    PATH_TO_FIFO = "/home/pi/ECE5725-Final/akai_fifo"
    while True:
        with open(PATH_TO_FIFO) as fifo:
            for line in fifo:
                if reNoteOn.match(line):
                    m = reNoteOn.match(line)
                    obj = NoteSignal("akai", time.time(),int(m.group(2)), int(m.group(3)),True)
                    obj.play()
                elif reNoteOff.match(line):
                    m = reNoteOff.match(line)
                    obj = NoteSignal("akai",time.time(), int(m.group(2)), int(m.group(3)),False)
                    obj.play()
                
                if recordMode and (time.time()-startRecordTime > recordLength):
                    print("Record Mode Turned Off")
                    recordMode = False
                elif recordMode and (reNoteOn.match(line) or reNoteOff.match(line)):
                    print("Record Event")
                    track1.append((time.time()-startRecordTime,obj))
'''

def setup_pins():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def record_start(channel):
    print("Record Start")
    global recordMode
    global startRecordTime
    global track1
    recordMode = True
    startRecordTime = time.time()
    track1 = []

def play(synth):
    global track1
    global recordMode

    while True:
        idx = 0
        start = time.time()
        if not recordMode:
            while idx < len(track1):
                if time.time() - start >= track1[idx][0]:
                    track1[idx][1].play(synth)
                    idx += 1
                time.sleep(0.05)



if __name__ == "__main__":
    print("Initializing Pins ...")
    setup_pins()
    GPIO.add_event_detect(17, GPIO.FALLING, callback=record_start, bouncetime=300)
    
    print("Initializing FluidSynth ...")

    fluidsynth.init("/home/pi/ECE5725-Final/sound_fonts/gen.sf2", "alsa")
    fluidsynth.set_instrument(1, 114, 0)
    fluidsynth.play_Note(Note("C-5"))

    print("Setting Up Processes ...")
    midiRecord = multiprocessing.Process(target=read_akai, args=(fluidsynth,)) 
    playMode = multiprocessing.Process(target=play, args=(fluidsynth,))

    print("Processes Starting Up ...")
    print("Press Button 17 To Start Recording ...")
    midiRecord.start()
    playMode.start()

    midiRecord.join()
    playMode.join()

    print("done")
