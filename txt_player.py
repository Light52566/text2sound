import numpy as np
import simpleaudio as sa
from scipy.io.wavfile import write

#generates a sine wave according to the given frequency for spesified duration T
def genSin(freq, T, sample_rate):
    t = np.linspace(0,T, num=int(T * sample_rate))
    fade = np.linspace(1,0,num=int(T * sample_rate))
    return np.multiply(np.sin(freq * t * 2 * np.pi),fade)

#generates chord according to given chord name in the form rootnote:scale for spesified duration T
def genChord(crd_name, T, sample_rate):
    if crd_name == 'N\n':
        return np.zeros(np.size(np.linspace(0,T, num=int(T * sample_rate))))
    A_freq = 440
    note_dict= {'A': A_freq * 2 ** (0 / 12), 'A#': A_freq * 2 ** (1 / 12), 'B': A_freq * 2 ** (2 / 12),
                'C': A_freq * 2 ** (3 / 12), 'C#': A_freq * 2 ** (4 / 12), 'D': A_freq * 2 ** (5 / 12),
                'D#': A_freq * 2 ** (6 / 12), 'E': A_freq * 2 ** (7 / 12), 'F': A_freq * 2 ** (8 / 12),
                'F#': A_freq * 2 ** (9 / 12), 'G': A_freq * 2 ** (10 / 12), 'G#': A_freq * 2 ** (11 / 12)}
    crd_dict_min = {'A':['A','C','E'], 'A#':['A#','C#','F'], 'Bb':['A#','C#','F'], 'B':['B','D','F#'],
                    'C':['C','D#','G'], 'C#':['C#','E','G#'], 'Db':['C#','E','G#'], 'D':['D','F','A'],
                    'D#':['D#','F#','A#'], 'Eb':['D#','F#','A#'], 'E':['E','G','B'], 'F':['F','G#','C'],
                    'F#':['F#','A','C#'], 'G':['G','A#','D'], 'G#':['G#','B','D#'], 'Ab':['G#','B','D#']}
    crd_dict_maj = {'A':['A','C#','E'], 'A#':['A#','D','F'], 'Bb':['A#','D','F'], 'B':['B','D#','F#'],
                    'C':['C','E','G'], 'C#':['C#','F','G#'], 'Db':['C#','F','G#'], 'D':['D','F#','A'],
                    'D#':['D#','G','A#'], 'Eb':['D#','G','A#'], 'E':['E','G#','B'], 'F':['F','A','C'],
                    'F#':['F#','A#','C#'], 'G':['G','B','D'], 'G#':['G#','C','D#'],'Ab':['G#','C','D#']}
    crd = crd_name.split(':')
    notes = []
    if 'maj' in crd[1]:
        for note in crd_dict_maj[crd[0]]:
            notes.append(genSin(note_dict[note],T,sample_rate))

    elif 'min' in crd[1]:
        for note in crd_dict_min[crd[0]]:
            notes.append(genSin(note_dict[note],T,sample_rate))
    
    output_chord = np.zeros(np.size(np.linspace(0,T, num=int(T * sample_rate))))
    for note in notes:
        output_chord += note
    return output_chord

#reads chord start and end times with the respective note from 
def readTxt(txtpath,sample_rate):
    chord_prog = []
    with open(txtpath, 'r') as f:
        for line in f:
            segment = line.split('\t')
            T = float(segment[1])-float(segment[0])
            chord = genChord(segment[2], T, sample_rate)
            chord_prog.append(chord)
            
            
    audio = np.hstack(chord_prog)
    audio *= 32767 / np.max(np.abs(audio))
    audio = audio.astype(np.int16)
    return audio
    
sample_rate = 44100
audio = readTxt('chord_audio.txt',sample_rate)

write("output.wav", sample_rate, audio)

# start playback
play_obj = sa.play_buffer(audio, 1, 2, sample_rate)

# wait for playback to finish before exiting
play_obj.wait_done()