import numpy as np
import pandas as pd
import time
from mne_lsl.stream import StreamLSL
from config import LSL_STREAM_NAME, BUFFER_SIZE, SAMPLING_RATE, BANDPASS_LOW, BANDPASS_HIGH, WINDOW_SIZE

class LSLDataSource:
    def __init__(self, csv_path='raw_data.csv', use_csv=True):
        self.use_csv = use_csv

        if not use_csv:
            self.stream = StreamLSL(bufsize=4, name=LSL_STREAM_NAME).connect()
            self.stream.pick("eeg").filter(BANDPASS_LOW, BANDPASS_HIGH)
            self.stream.get_data()

        self.df = pd.read_csv(csv_path)
        self.csv_index = 0

    def get_buffer(self):
        time.sleep(0.1)
        winsize = WINDOW_SIZE
        data, _ = self.stream.get_data(winsize)

        return data.T

    def get_recorded_buffer(self):
        samples = []

        for _ in range(BUFFER_SIZE):
            if self.csv_index >= len(self.df):
                self.csv_index = 0

            row = self.df.iloc[self.csv_index]
            sample = [
                row['Ch1RawEEG'], row['Ch2RawEEG'], row['Ch3RawEEG'],
                row['Ch4RawEEG'], row['Ch5RawEEG'], row['Ch6RawEEG'],
                row['Ch7RawEEG'], row['Ch8RawEEG'], row['Ch9RawEEG'],
                row['Ch10RawEEG'], row['Ch11RawEEG'], row['Ch12RawEEG']
            ]
            samples.append(sample)
            self.csv_index += 1
            time.sleep(1 / SAMPLING_RATE)

        return np.array(samples)
