
import time
import numpy as np
%pip install midiutil
from midiutil import MIDIFile

# for now it's only converting the prime numbers array to midi

def note_to_midi(note):

    note_map = {'C3': 48, 'D3': 50, 'E3': 52, 'F3': 53, 'G3': 55, 'A3': 57, 'B3': 59, 'C4': 60,  'C#4': 61, 'D4': 62,  'D#4': 63, 'E4': 64, 'F4': 65,  'F#4': 66, 'G4': 67,  'G#4': 68, 'A4': 69,  'A#4': 70, 'B4': 71, 'C5': 72, 'D5': 74, 'E5': 76, 'F5': 77, 'G5': 79, 'A5': 81, 'B5': 83 }
    note_name, octave = note , int(note[-1])
    midi_note = note_map[note_name] + (octave - 4) * 12
  
    return midi_note


def array_to_mid(array, name):
    
    notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']

    midi = MIDIFile(1)  # 1 Track
    time = 154
    duration = 1
    midi.addProgramChange(0, 0, 0, 1) # 1 I think is bright grand
    
    midi.addTempo(0, 0, time)
    te = array.reshape(-1)//7

    
    for i, num in enumerate(array-1):
        
        position = int(num % 7)
        
        note = notes[position]
        
        midi_number = note_to_midi(note)
        
        midi.addNote(0, 0, midi_number, te[i] *duration, duration, 127)  # track, channel, pitch, start_time, duration and volume 

    with open(name, 'wb') as file:
        midi.writeFile(file)
    print('Midi saved to: '+name)


def prim(n):
    """ Returns a array of primes, 3 <= p < n """
    sieve = np.ones(n//2, dtype=bool)
    for i in range(3,int(n**0.5)+1,2):
        if sieve[i//2]:
            sieve[i*i//2::i] = False
    return 2*np.nonzero(sieve)[0][1::]+1


array = np.insert(prim(8000), 0,2)[:1000]

name = 'song.mid'

array_to_mid(array, name) 
