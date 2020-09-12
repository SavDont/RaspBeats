import re

# Record values
bpm = 110.0
beats_per_bar = 16.0
# record length in seconds
record_length = (60/bpm) * beats_per_bar

# Soundfont
general_soundfont = "/home/pi/ECE5725-Final/sound_fonts/gen.sf2"

# Instruments
instruments =  [
        (1, 114, 0),
        (2, 25, 0),
        (3, 0, 0),
        (4, 38, 0),
        (5, 52, 0),
        (6, 40, 120),
        (7, 25, 120)]

# Regex expressions for midi message matching
rgx_note_on = re.compile("note_on.*channel=(\d+).*note=(\d+).*velocity=(\d+).*time=(\d+)")
rgx_note_off = re.compile("note_off.*channel=(\d+).*note=(\d+).*velocity=(\d+).*time=(\d+)")
rgx_control_change = re.compile("control_change.*channel=(\d+).*control=(\d+).*value=(\d+).*time=(\d+)")
rgx_program_change = re.compile("program_change.*channel=(\d+).*program=(\d+).*time=(\d+)")

rgx_record_start = re.compile("START RECORD.*(\d+).*")
rgx_record_stop = re.compile("STOP RECORD.*(\d+).*")

# Midi input devices
akai_device = u'MPK Mini Mk II:MPK Mini Mk II MIDI 1 16:0'
q49_device = u'Q49:Q49 MIDI 1 20:0'

# Fifo directories
playback_fifo = "/home/pi/ECE5725-Final/playback_fifo"
record_fifo = "/home/pi/ECE5725-Final/record_fifo"
