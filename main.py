from lsl_stream import LSLDataSource
from signal_processing import SignalProcessor
from state_detector import BrainStateDetector
from visualization import BrainStateVisualizer
from datetime import datetime
from config import BINAURAL_FREQUENCIES
import sounddevice as sd
import soundfile as sf
import time

def main():
    lsl_source = LSLDataSource(use_csv=False)
    processor = SignalProcessor()
    detector = BrainStateDetector()
    visualizer = BrainStateVisualizer()

    current_audio_file = None

    print(f"{'Time':<10} | {'Current State':<14} | {'Playing Audio':>10}")
    print("-" * 50)

    iteration = 0
    while True:
        buffer = lsl_source.get_buffer()
        # buffer = lsl_source.get_recorded_buffer()
        power_bands = processor.process(buffer)
        state = detector.detect_state(power_bands)

        audio_file = BINAURAL_FREQUENCIES[state]['file']

        if audio_file != current_audio_file:
            sd.stop()
            data, fs = sf.read(audio_file, dtype="float32")
            sd.play(data, fs)
            current_audio_file = audio_file

        timestamp_str = datetime.now().strftime("%H:%M:%S")
        freq_desc = BINAURAL_FREQUENCIES[state]['description']
        print(f"{timestamp_str:<10} | {state:<14} | {freq_desc:>10.1f} Hz")

        visualizer.update(power_bands, state, iteration * 2)
        iteration += 1

if __name__ == "__main__":
    main()
