import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


def plot_spectrogram(audio_path, save_path=None):
    """
    Plots a spectrogram for the audio file at the given path.

    Parameters:
    - audio_path: str, path to the audio file
    - save_path: str, path to save the spectrogram image, if None it will just display

    """
    # Load the audio file
    y, sr = librosa.load(audio_path)
    
    # Compute the spectrogram magnitude and phase
    S_full, phase = librosa.magphase(librosa.stft(y))

    plt.figure(figsize=(10, 4))

    # Display the spectrogram
    librosa.display.specshow(librosa.amplitude_to_db(S_full, ref=np.max),
                             y_axis='log', x_axis='time', sr=sr)
    
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.xlabel('Time')
    plt.ylabel('Frequency')

    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()