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
    return mido.MidiFile(file_dialog.FileName)
