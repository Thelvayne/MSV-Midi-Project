import sys
import ctypes
import mido

co_initialize = ctypes.windll.ole32.CoInitialize
#   Force STA mode
co_initialize(None)

import clr 

clr.AddReference('System.Windows.Forms')

from System.Windows.Forms import OpenFileDialog

def loadMidiFile():
    file_dialog:OpenFileDialog = OpenFileDialog()
    file_dialog.Filter = "MIDI files (*.mid)|*.mid"
    file_dialog.FilterIndex = 2
    file_dialog.ShowDialog()  
    filename = file_dialog.FileName
    if filename is not "":
        midifile = mido.MidiFile(file_dialog.FileName)
        if midifile is not None:
            return midifile
    #else: 
    #    return 
