
import matplotlib.pyplot as plt
import librosa.display
import numpy as np



def bin_search(arr, target):
    index = int(len(arr) / 2)
    min_index = 0
    max_index = len(arr) - 1
    found = False

    if target < arr[0]:
        return 0

    if target > arr[len(arr) - 1]:
        return len(arr) - 1

    while not found:

        if min_index == len(arr) - 2:
            return len(arr) - 1

        if arr[index] < target < arr[index + 1] or arr[index] == target:
            return index

        if arr[index] > target:
            max_index = index
        else:
            min_index = index

        index = int((min_index + max_index) / 2)





class AudioAnalyzer:

    def __init__(self):
        self.frequencies_index_ratio = 0  # array for frequencies
        self.time_index_ratio = 0  # array of time periods
        self.spectrogram = None  # a matrix that contains decibel values according to frequency and time indexes


    def load(self, filename):

        time_series, sample_rate = librosa.load(filename)  # getting information from the file

        # getting a matrix which contains amplitude values according to frequency and time indexes
        stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))

        self.spectrogram = librosa.amplitude_to_db(stft, ref=np.max)  # converting the matrix to decibel matrix

        frequencies = librosa.core.fft_frequencies(n_fft=2048*4)  # getting an array of frequencies

        # getting an array of time periodic
        times = librosa.core.frames_to_time(np.arange(self.spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4)

        self.time_index_ratio = len(times)/times[len(times) - 1]

        self.frequencies_index_ratio = len(frequencies)/frequencies[len(frequencies)-1]

    def fft(self, time_sec):
        """
        Returns a 1D array of decibel values for all frequencies at the given time (in seconds).
        Useful for visualizers.
        """
        time_index = int(time_sec * self.time_index_ratio)
        time_index = min(max(time_index, 0), self.spectrogram.shape[1] - 1)

        return self.spectrogram[:, time_index]

