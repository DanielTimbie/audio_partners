# main.py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pyaudio
import wave
from threading import Thread
from src.real_time_spectrum import compute_spectrum
from src.real_time_goniometer import setup_goniometer_subplot, update_goniometer

# Define constants
CHUNK = 1024
audio_file = 'audio_partners/audio_files/Morgan Wallen - In The Bible ft. HARDY.wav'

# Load audio for playback and visualization
wf_playback = wave.open(audio_file, 'rb')
wf_visual = wave.open(audio_file, 'rb')

# Extract audio parameters
RATE = wf_playback.getframerate()
CHANNELS = wf_playback.getnchannels()
FORMAT = pyaudio.paInt16
p = pyaudio.PyAudio()

# Function to play audio
def play_audio(stream, wf, CHUNK):
    data = wf.readframes(CHUNK)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

# Open audio stream
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)

# Start audio playback in a separate thread
audio_thread = Thread(target=play_audio, args=(stream, wf_playback, CHUNK))
audio_thread.start()

# Prepare the matplotlib figure for the animation with two subplots
fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 8))  # Two subplots for spectrum and goniometer
fig.patch.set_facecolor('black')
ax1.set_facecolor('black')
x = np.linspace(0, RATE // 2, 50)  # 50 frequency bins
bars = ax1.bar(x, np.zeros(50), width=(RATE // 2) / 50, align='center', color='green', edgecolor='black')
ax1.set_ylim(0, 2000)
ax1.set_xlim(0, RATE // 2)
ax1.set_yticklabels([])
ax1.yaxis.set_ticks_position('none') 
ax1.set_xlabel('Frequency in Hz')
line = setup_goniometer_subplot(ax2)

# Define an update function for both the spectrum and goniometer
def update(frame, wf_visual, bars, line, CHUNK, RATE, CHANNELS):
    # Update the spectrum
    compute_spectrum(frame, wf_visual, bars, CHUNK, RATE, CHANNELS)
    
    # Extract data for the goniometer
    data = np.frombuffer(wf_visual.readframes(CHUNK), dtype=np.int16)
    if CHANNELS == 2:
        data = data.reshape(-1, 2).T  # Transpose to get two rows: one for each channel

    # Update the goniometer
    update_goniometer(line, data, CHANNELS)

    return bars, line

# Start the animation
ani = animation.FuncAnimation(fig, update, fargs=(wf_visual, bars, line, CHUNK, RATE, CHANNELS),
                              interval=int(1000 * CHUNK / RATE), blit=False)

plt.tight_layout()
plt.show()

# Clean up
stream.stop_stream()
stream.close()
wf_visual.close()
p.terminate()
audio_thread.join()