from mido import MidiFile,Message,MetaMessage
import pygame

def note_to_freq(note, concert_A=440.0):
  return (2.0 ** ((note - 69) / 12.0)) * concert_A

def ticks_to_ms(ticks,tempo,mid:MidiFile) -> float:
    print(tempo)
    tick_ms = (60000.0 / tempo) / mid.ticks_per_beat
  
    return ticks * tick_ms

def set_Tempo(msg:MetaMessage):
    return 60000/msg.tempo*1000

def playMidi(mid:MidiFile):
    
    file = open(mid.filename)
    
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    pygame.mixer.music.get_busy()