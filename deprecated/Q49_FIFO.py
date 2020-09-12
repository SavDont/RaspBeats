import mido
import subprocess

with mido.open_input(u'Q49:Q49 MIDI 1 20:0') as inport:
    for msg in inport:
        cmd  = "echo {} > /home/pi/ECE5725/FinalProject/q49_fifo".format(msg)
        subprocess.check_output(cmd, shell=True)
