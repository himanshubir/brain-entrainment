# Map from current brain state to desired binaural frequency
BINAURAL_FREQUENCIES = {
    'GAMMA': {'description': 13, 'file': './audio_files/13Hz.wav'},
    'BETA': {'description': 10, 'file': './audio_files/10Hz.wav'},
    'ALPHA': {'description': 7, 'file': './audio_files/7Hz.wav'},
    'THETA': {'description': 4, 'file': './audio_files/5Hz.wav'},
    'DELTA': {'description': 7, 'file': './audio_files/7Hz.wav'},
}

HYSTERESIS_THRESHOLD = 0.20

SAMPLING_RATE = 500
WINDOW_SIZE = 4
BUFFER_SIZE = SAMPLING_RATE * WINDOW_SIZE
UPDATE_INTERVAL = 2

LSL_STREAM_NAME = "MW75 Neuro Neurable Stream"

BANDPASS_LOW = 3
BANDPASS_HIGH = 30

BAND_RANGES = {
    'delta': (0.5, 4),
    'theta': (4, 8),
    'alpha': (8, 13),
    'beta': (13, 30),
    'gamma': (30, 50)
}
