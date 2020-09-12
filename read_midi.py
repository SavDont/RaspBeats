import time
import sys
import subprocess

import mido
import RPi.GPIO as GPIO

from constants import *

record_start_time = None

def poll_midi_device(device, playback_fifo, record_fifo, current_channel, record_on, volumes):
    '''
    poll_midi_device(device, playback_fifo, record_fifo, current_channel, record_on, volumes) - Reads midi
    input signals from device specified and sends to playback_fifo. If a record signal has been sent
    then we also send the signals to record_fifo
    '''

    global record_start_time
    record_start_time = None
    with mido.open_input(device) as midi_input:
        while True:
            # Send end recording signal to record fifo when time has exceeded record_lenght, but only if we have akai device
            if device == akai_device and record_on.value and (time.time() > record_start_time + record_length):
                    print ("Done recording into {}".format(current_channel.value))
                    record_on.value = 0 # set record to false
                    record_start_time = None
                    subprocess.check_output("echo STOP RECORD {}  > {}".format(current_channel.value, record_fifo), shell=True)
            for msg in midi_input.iter_pending():
                # Record signals can only be sent via program change and akai_device since it has more functionality
                if msg.type == "program_change" and device == akai_device:
                    m = rgx_program_change.match(str(msg))
                    
                    # if we receive a program change 7 message, we start recording
                    if int(m.group(2)) == 7 and not record_on.value:
                        record_on.value = 1
                        record_start_time = time.time()
                        print ("Start recording into {}".format(current_channel.value))
                        subprocess.check_output("echo START RECORD {} > {}".format(current_channel.value, record_fifo), shell=True)
                    # if we receive other number program change, we change the channel/instrument when not recording
                    # should not be able to switch instruments in the middle of active recording
                    elif not record_on.value:
                        current_channel.value = int(m.group(2))+1
                        print ("Current track switched to {}".format(current_channel.value))
                elif msg.type == "control_change" and device == akai_device:
                    # knob turns on akai are read as control change, used to set volume for channels
                    m = rgx_control_change.match(str(msg))
                    
                    # Only have 7 tracks, cannot change volume on track 8
                    if int(m.group(2)) < 8:
                        volumes[int(m.group(2))] = int(m.group(3))
                        print("Volume for channel {} changed to {}".format(int(m.group(2)), int(m.group(3))))
                elif msg.type == "note_on" or msg.type == "note_off":
                    # change channel value to current instrument and send to playback_fifo
                    msg = msg.copy(channel=current_channel.value)
                    playback_cmd = "echo {} > {}".format(msg, playback_fifo)
                    subprocess.check_output(playback_cmd, shell=True)
                    
                    # if currently recording, send to record_fifo
                    if record_on.value:
                        record_cmd = "echo {} > {}".format(msg, record_fifo)
                        subprocess.check_output(record_cmd, shell=True)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ("Incorrect number of arguments. Please enter device name")
        exit(1)
    elif sys.argv[1] == "akai":
        poll_midi_device(akai_device, akai_playback_fifo, akai_record_fifo, akai_control_fifo)
    elif sys.argv[1] == "q49":
        poll_midi_device(q49_device, q49_playback_fifo, q49_record_fifo, q49_control_fifo)
