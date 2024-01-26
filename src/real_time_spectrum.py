# real_time_spectrum.py
import numpy as np
from scipy.fft import fft

def compute_spectrum(frame, wf, bars, CHUNK, RATE, CHANNELS):
    data = wf.readframes(CHUNK)
    if len(data) == CHUNK * CHANNELS * 2:  # 2 bytes per sample
        waveform_data = np.frombuffer(data, dtype=np.int16)
        if CHANNELS == 2:
            waveform_data = np.mean(waveform_data.reshape(-1, 2), axis=1)  # Averaging stereo channels
        yf = fft(waveform_data)
        yf = 2.0 / CHUNK * np.abs(yf[:CHUNK // 2])
        bin_width = (RATE // 2) / len(bars)
        bin_means = [yf[int(bin_width / (RATE / CHUNK)) * i: int(bin_width / (RATE / CHUNK)) * (i + 1)].mean() for i in range(len(bars))]
        for bar, h in zip(bars, bin_means):
            bar.set_height(h)
    return bars