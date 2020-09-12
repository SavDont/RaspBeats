import re
import time
import RPi.GPIO as GPIO

from constants import *
from signals import *
from mingus.midi import fluidsynth

fluidsynth.init("/home/pi/ECE5725-Final/sound_fonts/gen.sf2","alsa")
fluidsynth.set_instrument(1, 13, 0)

# Regex expressions for matching
reNoteOn = re.compile("note_on.*channel=(\d+).*note=(\d+).*velocity=(\d+).*time=(\d+)")
reNoteOff = re.compile("note_off.*channel=(\d+).*note=(\d+).*velocity=(\d+).*time=(\d+)")
reControlChange = re.compile("control_change.*channel=(\d+).*control=(\d+).*value=(\d+).*time=(\d+)")
'''
recordMode = False
startRecordTime = time.time()

def setup_pins():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_UP)

def record_start():
    #if currently recording send event to fifo, otherwise send cancel
    if not recordMode:
        recordMode = True
        startRecordTime = time.time()
        obj = RecordSignal("global", startRecordTime, RECORD_START)
    else:
        recordMode = False
        obj = RecordSignal("global",time.time(), RECORD_CANCEL)

def loop():
    if not recordMode:
        while not recordMode:
            with open("/home/pi/ECE5725-Final/akai_fifo") as fifo:
                for line in fifo:
                    if reNote.match(line):
                        m = reNoteOn.match(line)
                        obj = NoteSignal("akai",time.time(),int(m.group(2)),int(m.group(3)),1)
                        obj.play()
                    elif reNoteOff.match(line):
                        m = reNoteOff.match(line)
                        obj = NoteSignal("akai",time.time(),int(m.group(2)), int(m.group(3)),0)
                        obj.play()

'''
if __name__ == "__main__":
    while True:
        with open("/home/pi/ECE5725-Final/akai_fifo") as fifo:
            for line in fifo:
                if reNoteOn.match(line):
                    m = reNoteOn.match(line)
                    obj = NoteSignal("akai",time.time(),int(m.group(2)),int(m.group(3)),1)
                    obj.play()
                elif reNoteOff.match(line):
                    m = reNoteOff.match(line)
                    obj = NoteSignal("akai",time.time(),int(m.group(2)),int(m.group(3)),0)
                    obj.play()
                else: 
                    #used for volume change, effects, etc
                    m = reControlChange.match(line)
                    obj = ControlChangeSignal("akai",time.time(), int(m.group(2)),int(m.group(3)))

                print(obj)

'''

setup_pins()
GPIO.add_event_detect(17, GPIO.FALLING, callback=record_start, bouncetime=300)
'''
