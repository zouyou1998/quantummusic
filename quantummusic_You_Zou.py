#!/usr/bin/env python
# coding: utf-8

# In[1]:


from qiskit import QuantumCircuit, transpile, assemble, Aer, execute
from qiskit.visualization import circuit_drawer
import random

# create a quantum circuit
qc = QuantumCircuit(4, 4)

# Hadamard gate on each qubit
for qubit in range(4):
    qc.h(qubit)

# measure result
qc.measure(range(4), range(4))

# print the circuit
print("The quantum circuit:")
print(circuit_drawer(qc))

# simulate the circuit
simulator = Aer.get_backend('qasm_simulator')
compiled_circuit = transpile(qc, simulator)

# an empty list, will generate 300 times 4-bit number in binary system 
music_number=[]

for i in range(300):
    # 300 times simulate, each time 1 shot, and put the result in empty list
    job = assemble(compiled_circuit, shots=1)  
    result = execute(compiled_circuit, simulator, shots=1).result() 
    counts = result.get_counts(compiled_circuit)
    for key in counts:
        music_number.append(key)

# show the result of the 300 times 4-bit number in binary system 
print("The 4-bit number in binary system for offset:")
print(music_number)

# defining the grade of a note
notes = list(range(16))  # 0到16

# defining the number of a note
num_notes = 300

# starting with a random number as first note from 0-16
current_note = random.choice(notes)

# save the list of generated notes
generated_notes = [current_note]  

# generate new note
for bit_number in music_number:
    
    # calculate the offset based on the number of bits
    offset = 0
    if bit_number == '0000':
        offset = -3
    elif bit_number == '0001' or bit_number == '0010':
        offset = -2
    elif bit_number in ['0011', '0100', '0101', '0110']:
        offset = -1
    elif bit_number == '0111' or bit_number == '1000':
        offset = 0
    elif bit_number in ['1001', '1010', '1011', '1100']:
        offset = 1
    elif bit_number in ['1101', '1110']:
        offset = 2
    elif bit_number == '1111':
        offset = 3

    # calculate new next note
    new_note = current_note + offset

    # check the boundary condition
    if new_note < 0:
        new_note = 0
    elif new_note > 16:
        new_note = 16

    generated_notes.append(new_note)
    current_note = new_note

# print the result
print("The non-standarlized generated notes:")
print(generated_notes)


# In[2]:


# Dictionary defining the correspondence between numbers and MIDI pitches
mapping_dict = {
    0: 56,
    1: 58,
    2: 60,
    3: 61,
    4: 63,
    5: 65,
    6: 67,
    7: 68,
    8: 70,
    9: 72,
    10: 73,
    11: 75,
    12: 77,
    13: 79,
    14: 80,
    15: 82,
    16: 84
}

# generate a new list based on the input list
output_list = [mapping_dict[num] for num in generated_notes]

# prints a new list of outputs
print("The standarlized generated notes:")
print(output_list)


# In[ ]:


from music21 import stream, note, instrument
import pygame

# initialising Pygame
pygame.init()

# create a music stream object
s = stream.Stream()

# define Violin Instrument
violin = instrument.Violin()

#-----------------------------------

# loop through the list of notes
for note_value in output_list:
    # calculating pitch with C4 as the base pitch
    pitch = note_value  

    # create a note object
    n = note.Note()
    n.pitch.midi = pitch

    # add the note object to the music stream object
    s.append(n)

# add the Violin Instrument object to the Music Stream object
s.insert(0, violin)

# save music streams as MIDI files
s.write('midi', 'violin_music.mid')

# load music files
pygame.mixer.music.load('violin_music.mid')

# playing music
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    continue

# stop Pygame
pygame.quit()


# In[ ]:





# In[ ]:




