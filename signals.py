from constants import *
from mingus.containers import Note
from mingus.midi import fluidsynth

class EventSignal(object):
    '''
    MidiSignal - An object that includes basic MIDI event information
    including the device it is coming from  and the time of the event
    '''
    def __init__(self, device, midi_time):
        self.device = device
        self.midi_time = midi_time
    
    def __str__(self):
        return str(self.__dict__)

class NoteSignal(EventSignal):
    '''
    Note - An object that extends the MidiSignal class and adds
    information on the note, velocity and whether the note was 
    pressed down or released as well as what channel it was on
    '''
    def __init__(self, device, midi_time, note, velocity, on_off,channel):
        EventSignal.__init__(self, device, midi_time)
        self.note = Note().from_int(note)
        self.note.velocity = 127
        self.note.channel = channel
        self.channel = channel
        self.on_off = on_off
    
    def __str__(self):
        return str(self.__dict__)
    
    def play(self, volume = 127):
        '''
        play - plays a note at specified volume if it was a note_on event and stops a note 
        if it was a note_off event
        '''
        self.note.velocity = volume
        if self.on_off:
            fluidsynth.play_Note(self.note,self.channel)
        else:
            fluidsynth.stop_Note(self.note, self.channel)
