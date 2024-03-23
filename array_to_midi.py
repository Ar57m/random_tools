
import time
import numpy as np
%pip install midiutil
from midiutil import MIDIFile

# for now it's only converting the prime numbers array to midi

def note_to_midi(note):
    
    map = {'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67, 'A': 69, 'B': 71}
    
    note_name, octave = note[:-1], int(note[-1])
    
    midi = map[note_name] + (octave - 4) * 12
    return midi


def array_to_mid(array, name):
    
    notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']

    midi = MIDIFile(1)  # 1 Track
    time = 110
    midi.addProgramChange(0, 0, 0, 41) # 41 is violin
    
    midi.addTempo(0, 0, time)
    te = array.reshape(-1)//7

    
    for i, num in enumerate(array-1):
        
        position = num % 7
        
        note = notes[position]
        
        midi_number = note_to_midi(note)
        
        midi.addNote(0, 0, midi_number, te[i] *0.7, 0.7, 100)  # track, channel, pitch, start_time, duration and volume 

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
