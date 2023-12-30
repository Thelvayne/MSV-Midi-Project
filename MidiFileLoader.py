import sys
import ctypes

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
    result = file_dialog.ShowDialog()
    if result == 1:
        print(file_dialog.FileName)
