import matplotlib.pyplot as plt
from collections import deque
import numpy as np

class BrainStateVisualizer:
    def __init__(self, history_length=15):
        plt.ion()
        self.fig, (self.ax_time, self.ax_bar) = plt.subplots(2, 1, figsize=(10, 8))
        self.fig.suptitle('Brain Entrainment Monitor', fontsize=14, fontweight='bold')

        self.history_length = history_length
        self.times = deque(maxlen=history_length)
        self.band_history = {
            'delta': deque(maxlen=history_length),
            'theta': deque(maxlen=history_length),
            'alpha': deque(maxlen=history_length),
            'beta': deque(maxlen=history_length),
            'gamma': deque(maxlen=history_length)
        }

        self.colors = {
            'delta': '#1f77b4',
            'theta': '#ff7f0e',
            'alpha': '#2ca02c',
            'beta': '#d62728',
            'gamma': '#9467bd'
        }

        self.lines = {}
        for band, color in self.colors.items():
            line, = self.ax_time.plot([], [], label=band.capitalize(), color=color, linewidth=2)
            self.lines[band] = line

        self.ax_time.set_xlabel('Time (s)')
        self.ax_time.set_ylabel('Relative Power')
        self.ax_time.set_title('Bandpower Over Time')
        self.ax_time.legend(loc='upper left')
        self.ax_time.grid(True, alpha=0.3)

        self.bars = self.ax_bar.bar(range(5), [0]*5, color=list(self.colors.values()))
        self.ax_bar.set_xticks(range(5))
        self.ax_bar.set_xticklabels(['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma'])
        self.ax_bar.set_ylabel('Relative Power')
        self.ax_bar.set_title('Current Bandpower Distribution')
        self.ax_bar.set_ylim(0, 1)

        self.state_text = self.ax_bar.text(0.5, 0.95, '', transform=self.ax_bar.transAxes,
                                           ha='center', va='top', fontsize=12, fontweight='bold',
                                           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

        plt.tight_layout()
        self.start_time = None

    def update(self, power_bands, current_state, timestamp):
        if self.start_time is None:
            self.start_time = timestamp

        elapsed = timestamp - self.start_time
        self.times.append(elapsed)

        for band in self.band_history.keys():
            self.band_history[band].append(power_bands[band])

        if len(self.times) > 1:
            for band, line in self.lines.items():
                line.set_data(list(self.times), list(self.band_history[band]))

            self.ax_time.set_xlim(max(0, elapsed - 30), elapsed + 1)
            self.ax_time.set_ylim(0, max(max(max(v) if v else [0] for v in self.band_history.values()), 0.1) * 1.1)

        band_names = ['delta', 'theta', 'alpha', 'beta', 'gamma']
        band_values = [power_bands[band] for band in band_names]

        for i, (bar, value) in enumerate(zip(self.bars, band_values)):
            bar.set_height(value)
            if band_names[i] == current_state.lower():
                bar.set_color('gold')
                bar.set_edgecolor('black')
                bar.set_linewidth(3)
            else:
                bar.set_color(self.colors[band_names[i]])
                bar.set_edgecolor('none')

        self.state_text.set_text(f'Current State: {current_state}')

        plt.pause(0.01)
