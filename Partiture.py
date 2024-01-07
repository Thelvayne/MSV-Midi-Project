#TODO: 
#
# Miditracks = anzahl der Reiter
#
# Separate Anzeigebereich:
# BPM Anzeige
# Taktanzeige
# Tonartanzeige
# Zeitanzeige

import mido, pydub
from mido import Message,MetaMessage



class Partiture():
    
    def __init__(self,midifile:mido.MidiFile):
        self.channels=midifile.tracks
        self.name = midifile.filename