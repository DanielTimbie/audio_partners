#code to intake an audio file and output a spectrogram

import librosa
import matplotlib.pyplot as plt

audio = 'audio_partners/audio_files/Sewerslvt - Restlessness.wav'
x, sr = librosa.load(audio)
X = librosa.stft(x)
Xdb = librosa.amplitude_to_db(abs(X))
plt.figure(figsize = (10, 5))
librosa.display.specshow(Xdb, sr = sr, x_axis = 'time', y_axis = 'hz')
plt.colorbar()
plt.set_cmap('inferno')
plt.show()