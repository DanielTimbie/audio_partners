import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
from scipy.fft import fft
from scipy.signal import find_peaks
import wave
import pyaudio
from threading import Thread

# Open the WAV file for audio playback
audio_file = 'audio_partners/audio_files/DILATAÇÃO HIPNÓTICA 6.0.wav'
wf_playback = wave.open(audio_file, 'rb')

# Open the WAV file again for visualization
wf_visual = wave.open(audio_file, 'rb')

# Extract audio parameters
RATE = wf_playback.getframerate()
CHANNELS = wf_playback.getnchannels()
FORMAT = pyaudio.paInt16
CHUNK = 1024

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True)

# Function to play audio
def play_audio(stream, wf, CHUNK):
    data = wf.readframes(CHUNK)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    wf.close()
    p.terminate()

# Start the audio playback in a separate thread
audio_thread = Thread(target=play_audio, args=(stream, wf_playback, CHUNK))
audio_thread.start()

# Update function for the animation
def update_plot(frame, wf, bars, CHUNK, num_bins):
    data = wf.readframes(CHUNK)
    if len(data) == CHUNK * CHANNELS * 2:  # 2 bytes per sample
        waveform_data = np.frombuffer(data, dtype=np.int16)
        if CHANNELS == 2:
            waveform_data = np.mean(waveform_data.reshape(-1, 2), axis=1)  # Averaging stereo channels
        yf = fft(waveform_data)
        yf = 2.0 / CHUNK * np.abs(yf[:CHUNK // 2])
        # Bin the frequencies and magnitudes
        bin_means = [yf[int(bin_width / (RATE / CHUNK)) * i: int(bin_width / (RATE / CHUNK)) * (i + 1)].mean() for i in range(num_bins)]
        # Update the bar heights
        for bar, h in zip(bars, bin_means):
            bar.set_height(h)
    return bars

# Number of bins for the histogram
num_bins = 50  # For example, 50 bins across the frequency spectrum
bin_width = (RATE // 2) / num_bins  # Frequency range divided by the number of bins

# Set up the figure for the histogram-like plot
fig, ax = plt.subplots()
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
x = np.linspace(0, RATE // 2, num_bins)
# colors = cm.inferno(np.linspace(0, 1, num_bins))  # Generate colors from the inferno map
bars = ax.bar(x, np.zeros(num_bins), color = "green", edgecolor='black', width=bin_width, align='center')
ax.set_ylim(0, 2000)
ax.set_xlim(0, RATE // 2)
ax.set_yticklabels([])
ax.yaxis.set_ticks_position('none')
ax.set_xlabel('Frequency in Hz')


# Start the animation
ani = animation.FuncAnimation(fig, update_plot, fargs=(wf_visual, bars, CHUNK, num_bins),
                              interval=int(1000 * CHUNK / RATE), blit=False)

plt.show()

# When the plot is closed, ensure all threads are terminated
audio_thread.join()
wf_visual.close()
