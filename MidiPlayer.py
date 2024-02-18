from mido import MidiFile
import pygame

def playMidi(mid:MidiFile):
    
    file = open(mid.filename)
    
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    pygame.mixer.music.get_busy()
