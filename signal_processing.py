import numpy as np
from scipy.signal import butter, filtfilt, welch
from scipy.integrate import simpson
from config import (SAMPLING_RATE, BANDPASS_LOW, BANDPASS_HIGH, BAND_RANGES)

class SignalProcessor:
    def __init__(self):
        nyquist = SAMPLING_RATE / 2
        self.b, self.a = butter(4, [BANDPASS_LOW / nyquist, BANDPASS_HIGH / nyquist], btype='band')

    def process(self, data):
        filtered = filtfilt(self.b, self.a, data, axis=0)

        left_data = filtered[:, :6].T
        right_data = filtered[:, 6:].T

        left_powers = self._compute_all_bandpowers(left_data)
        right_powers = self._compute_all_bandpowers(right_data)

        return {
            'delta': (left_powers['delta'] + right_powers['delta']) / 2,
            'theta': (left_powers['theta'] + right_powers['theta']) / 2,
            'alpha': (left_powers['alpha'] + right_powers['alpha']) / 2,
            'beta': (left_powers['beta'] + right_powers['beta']) / 2,
            'gamma': (left_powers['gamma'] + right_powers['gamma']) / 2
        }

    def _compute_all_bandpowers(self, data):
        freqs, psd = welch(data, SAMPLING_RATE)
        freq_res = freqs[1] - freqs[0]

        band_powers = {}
        for band, (low, high) in BAND_RANGES.items():
            idx = np.logical_and(freqs >= low, freqs <= high)
            bp = simpson(psd[:, idx], dx=freq_res)
            band_powers[band] = np.mean(bp / simpson(psd, dx=freq_res))

        return band_powers
