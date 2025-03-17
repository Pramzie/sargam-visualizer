import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from colorama import Fore, Style, init
import time

# Initialize colorama
init(autoreset=True)

# Frequencies for Indian classical notes in C Major scale
notes = {
    'Sa': 261.63,   # C
    'Re': 293.66,   # D
    "Re'": 587.33, # D (Higher octave)
    'Ga': 311.13,   # E
    'Ma': 349.23,   # F
    'Pa': 392.00,   # G
    'Dha': 440.00,  # A
    'ni': 466.16,   # Bb (Komal Ni)
    'Ni': 493.88,   # B
    "Sa'": 523.25, # C (Higher octave)
    'dha': 415.30,  # Ab (Komal Dha)
}

# Full melody for the sargam sequence with sargam lyrics and additional text
melody = [
    ('Pa', 0.75, 'Pa', 'Sajan Bin Aaaye Na'), ('Pa', 0.5, 'Pa', 'Sajan Bin Aaaye Na'), ('ni', 0.5, 'ni', 'Sajan Bin Aaaye Na'), ("Sa'", 0.5, "Sa'", 'Sajan Bin Aaaye Na'), ("Re'", 0.5, "Re'", 'Sajan Bin Aaaye Na'),
    ("Re'", 0.5, "Re'", 'Sajan Bin Aaaye Na'), ("Sa'", 0.5, "Sa'", 'Sajan Bin Aaaye Na'),
    ('dha', 0.5, 'dha', 'Sajan Bin Aaaye Na'), ('ni', 0.5, 'ni', 'Sajan Bin Aaaye Na'), ('Pa', 1.5, 'Pa', 'Sajan Bin Aaaye Na'),
    ('Ga', 0.5, 'Ga', 'Mohe Nindiya'), ('Ma', 0.5, 'Ma', 'Mohe Nindiya'), ('ni', 0.5, 'ni', 'Mohe Nindiya'), ('dha', 0.5, 'dha', 'Mohe Nindiya'), ('Pa', 1.5, 'Pa', 'Mohe Nindiya'),

    ('Ma', 0.75, 'Ma', 'Rain Bhar Aaye Re'), ('Pa', 0.5, 'Pa', 'Rain Bhar Aaye Re'), ('ni', 0.5, 'ni', 'Rain Bhar Aaye Re'), ("Sa'", 0.5, "Sa'", 'Rain Bhar Aaye Re'), ('Re', 0.5, 'Re', 'Rain Bhar Aaye Re'),
    ("Sa'", 0.5, "Sa'", 'Rain Bhar Aaye Re'), ("Re'", 0.5, "Re'", 'Rain Bhar Aaye Re'), ("Sa'", 0.5, "Sa'", 'Rain Bhar Aaye Re'),
    ('dha', 0.5, 'dha', 'Rain Bhar Aaye Re'), ('ni', 0.5, 'ni', 'Rain Bhar Aaye Re'), ('Pa', 1.5, 'Pa', 'Rain Bhar Aaye Re'),
    ('Ga', 0.5, 'Ga', 'Jaage Ratiya'), ('Ma', 0.5, 'Ma', 'Jaage Ratiya'), ('Re', 0.5, 'Re', 'Jaage Ratiya'), ('Sa', 0.5, 'Sa', 'Jaage Ratiya'), ('Re', 0.85, 'Re', 'Jaage Ratiya'),
  
    ('Pa', 0.5, 'Pa', 'Kahe tu Mohe Sajan Piya Re'), ('Ga', 0.5, 'Ga', 'Kahe tu Mohe Sajan Piya Re'), ('Ma', 0.5, 'Ma', 'Kahe tu Mohe Sajan Piya Re'), ('Re', 0.5, 'Re', 'Kahe tu Mohe Sajan Piya Re'), ('Sa', 0.5, 'Sa', 'Kahe tu Mohe Sajan Piya Re'),
    ('ni', 0.55, 'ni', 'Kahe tu Mohe Sajan Piya Re'), ('Sa', 0.5, 'Sa', 'Kahe tu Mohe Sajan Piya Re'), ('ni', 0.5, 'ni', 'Kahe tu Mohe Sajan Piya Re'), ('Sa', 0.5, 'Sa', 'Kahe tu Mohe Sajan Piya Re'), ('Re', 0.5, 'Re', 'Kahe tu Mohe Sajan Piya Re'), ('Sa', 0.55, 'Sa', 'Kahe tu Mohe Sajan Piya Re'),
  
    ('Re', 0.5, 'Re', 'Dikhe Ye Najare, Maney na'), ('Ma', 0.5, 'Ma', 'Dikhe Ye Najare, Maney na'), ('Re', 0.5, 'Re', 'Dikhe Ye Najare, Maney na'), ('Ma', 0.5, 'Ma', 'Dikhe Ye Najare, Maney na'), ('Pa', 0.5, 'Pa', 'Dikhe Ye Najare, Maney na'), ('ni', 0.5, 'ni', 'Dikhe Ye Najare, Maney na'),
    ('Ma', 0.5, 'Ma', 'Dikhe Ye Najare, Maney na'), ('Pa', 0.5, 'Pa', 'Dikhe Ye Najare, Maney na'), ('ni', 0.5, 'ni', 'Dikhe Ye Najare, Maney na'), ("Sa'", 0.75, "Sa'", 'Dikhe Ye Najare, Maney na'),
  
    ("Re'", 0.5, "Re'", 'Apni Akhiya'), ('Pa', 0.5, 'Pa', 'Apni Akhiya'), ("Ga'", 0.5, "Ga'", 'Apni Akhiya'), ("Ma'", 0.5, "Ma'", 'Apni Akhiya'),
    ("Re'", 0.5, "Re'", 'Apni Akhiya'), ("Re'", 0.5, "Re'", 'Apni Akhiya'), ("Sa'", 0.75, "Sa'", 'Apni Akhiya'),
    ('Pa', 0.75, 'Pa', 'Sajan Bin Aaaye Na'), ('Pa', 0.5, 'Pa', 'Sajan Bin Aaaye Na'), ('ni', 0.5, 'ni', 'Sajan Bin Aaaye Na'), ("Sa'", 0.5, "Sa'", 'Sajan Bin Aaaye Na'), ("Re'", 0.5, "Re'", 'Sajan Bin Aaaye Na'),
    ("Re'", 0.5, "Re'", 'Sajan Bin Aaaye Na'), ("Sa'", 0.5, "Sa'", 'Sajan Bin Aaaye Na'),
    ('dha', 0.5, 'dha', 'Sajan Bin Aaaye Na'), ('ni', 0.5, 'ni', 'Sajan Bin Aaaye Na'), ('Pa', 1.5, 'Pa', 'Sajan Bin Aaaye Na'),
    ('Ga', 0.5, 'Ga', 'Mohe Nindiya'), ('Ma', 0.5, 'Ma', 'Mohe Nindiya'), ('ni', 0.5, 'ni', 'Mohe Nindiya'), ('dha', 0.5, 'dha', 'Mohe Nindiya'), ('Pa', 1.5, 'Pa', 'Mohe Nindiya')
]

# Sampling rate
sampling_rate = 44100

# Function to generate a sine wave for a given frequency and duration
def generate_wave(frequency, duration):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    return wave

# Display lyrics using matplotlib
plt.ion()
fig, ax = plt.subplots()
text_display = ax.text(0.5, 0.6, '', ha='center', va='center', fontsize=30, fontweight='bold', family='serif', color='blue')
subtext_display = ax.text(0.5, 0.4, '', ha='center', va='center', fontsize=20, family='serif', color='red')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# Play the melody and display sargam and additional text
for i, (note, duration, lyric, subtext) in enumerate(melody):
    if note in notes:
        text_display.set_text(lyric)
        subtext_display.set_text(subtext)
        fig.canvas.draw()
        fig.canvas.flush_events()
        wave = generate_wave(notes[note], duration)
        sd.play(wave, samplerate=sampling_rate)
        sd.wait()
        time.sleep(0.02)

plt.ioff()
plt.show()
