from collections import defaultdict
from mido import MidiFile,MetaMessage
from pydub import AudioSegment
from pydub.generators import Sine
import pydub.generators as pygen

## transferring a midi message note to a frequency
def note_to_freq(note, concert_A=440.0):
  return (2.0 ** ((note - 69) / 12.0)) * concert_A

def ticks_to_ms(ticks,tempo,mid:MidiFile) -> float:
    print(tempo)
    tick_ms = (60000.0 / tempo) / mid.ticks_per_beat
  
    return ticks * tick_ms

def set_Tempo(msg:MetaMessage):
    return 60000/msg.tempo*1000

def convertMidToWav(mid:MidiFile):

    #mid = MidiFile("./lavandia.mid")
    output = AudioSegment.silent(mid.length * 1000.0)
    #print(f"TEMPO: {set_Tempo(mid)}")

    for track in mid.tracks:
        # position of rendering in ms
        current_pos = 0.0

        current_notes = defaultdict(dict)
        # current_notes = {
        #   channel: {
        #     note: (start_time, message)
        #   }
        # }
    
        for msg in track:
            if msg.type =="set_tempo":
                tempo = set_Tempo(msg)
            
            current_pos += ticks_to_ms(msg.time,tempo,mid)    

            if msg.type == 'note_on':
                current_notes[msg.channel][msg.note] = (current_pos, msg)
            
            if msg.type == 'note_off':
                start_pos, start_msg = current_notes[msg.channel].pop(msg.note)
            
                duration = current_pos - start_pos
            
                signal_generator = Sine(note_to_freq(msg.note))
                rendered = signal_generator.to_audio_segment(duration=duration-50, volume=-20).fade_out(100).fade_in(30)

                output = output.overlay(rendered, start_pos)

    s = str(mid.filename).removesuffix(".mid")
    output.export(f"{s}.wav", format="wav")