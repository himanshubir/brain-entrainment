import time
import uuid

import numpy as np
from matplotlib import colormaps
from matplotlib import pyplot as plt
from mne.io import read_raw_fif
from mne.time_frequency import psd_array_multitaper
from numpy.typing import NDArray
from scipy.integrate import simpson
from scipy.signal import periodogram, welch

from mne_lsl.datasets import sample
from mne_lsl.player import PlayerLSL
from mne_lsl.stream import StreamLSL

# # dataset used in the example
# raw = read_raw_fif(sample.data_path() / "sample-ant-raw.fif", preload=False)
# raw.crop(40, 60).load_data()
# raw

def bandpower(
    data: NDArray[np.float64],
    fs: float,
    method: str,
    band: tuple[float, float],
    relative: bool = True,
    **kwargs,
) -> NDArray[np.float64]:
    """Compute the bandpower of the individual channels.

    Parameters
    ----------
    data : array of shape (n_channels, n_samples)
        Data on which the the bandpower is estimated.
    fs : float
        Sampling frequency in Hz.
    method : 'periodogram' | 'welch' | 'multitaper'
        Method used to estimate the power spectral density.
    band : tuple of shape (2,)
        Frequency band of interest in Hz as 2 floats, e.g. ``(8, 13)``. The
        edges are included.
    relative : bool
        If True, the relative bandpower is returned instead of the absolute
        bandpower.
    **kwargs : dict
        Additional keyword arguments are provided to the power spectral density
        estimation function.
        * 'periodogram': scipy.signal.periodogram
        * 'welch'``: scipy.signal.welch
        * 'multitaper': mne.time_frequency.psd_array_multitaper

        The only provided arguments are the data array and the sampling
        frequency.

    Returns
    -------
    bandpower : array of shape (n_channels,)
        The bandpower of each channel.
    """
    # compute the power spectral density
    assert data.ndim == 2, (
        "The provided data must be a 2D array of shape (n_channels, n_samples)."
    )
    if method == "periodogram":
        freqs, psd = periodogram(data, fs, **kwargs)
    elif method == "welch":
        freqs, psd = welch(data, fs, **kwargs)
    elif method == "multitaper":
        psd, freqs = psd_array_multitaper(data, fs, verbose="ERROR", **kwargs)
    else:
        raise RuntimeError(f"The provided method '{method}' is not supported.")
    # compute the bandpower
    assert len(band) == 2, "The 'band' argument must be a 2-length tuple."
    assert band[0] <= band[1], (
        "The 'band' argument must be defined as (low, high) (in Hz)."
    )
    freq_res = freqs[1] - freqs[0]
    idx_band = np.logical_and(freqs >= band[0], freqs <= band[1])
    bandpower = simpson(psd[:, idx_band], dx=freq_res)
    bandpower = bandpower / simpson(psd, dx=freq_res) if relative else bandpower
    return bandpower

# Connecting to MW75 Neuro LSL Stream
name = "MW75 Neuro Neurable Stream"
stream = StreamLSL(bufsize=2, name=name).connect()
stream.info

stream.ch_names

# Example plot of the raw data, notice how noisy it is
picks = ("eeg2", "eeg8")  # channel selection
f, ax = plt.subplots(3, 1, sharex=True, constrained_layout=True)
for _ in range(3):  # acquire 3 separate window
    # figure how many new samples are available, in seconds
    winsize = stream.n_new_samples / stream.info["sfreq"]
    # retrieve and plot data
    data, ts = stream.get_data(winsize, picks=picks)
    for k, data_channel in enumerate(data):
        ax[k].plot(ts, data_channel)
    time.sleep(0.5)
for k, ch in enumerate(picks):
    ax[k].set_title(f"EEG {ch}")
ax[-1].set_xlabel("Timestamp (LSL time)")
plt.show()

# Reducing artifacts by filtering from 1 to 30 
stream.pick("eeg").filter(1, 30)
stream.get_data()  # reset the number of new samples after the filter is applied

# extracting alpha bandpower
datapoints, times = [], []
for i in range(10):
    while stream.n_new_samples < stream.n_buffer:
        time.sleep(0.1)  # wait for the buffer to be entirely filled
    if stream.n_new_samples == 0:
        continue  # wait for new samples
    data, ts = stream.get_data()
    bp = bandpower(data, stream.info["sfreq"], "periodogram", band=(8, 13))
    datapoints.append(bp)
    times.append(ts[-1])
    # print(f"stream.n_new_samples: {stream.n_new_samples}")
    # print(f"stream.n_buffer: {stream.n_buffer}")

f, ax = plt.subplots(1, 1, layout="constrained")
ax.plot(times - times[0], [np.average(dp) * 100 for dp in datapoints])
ax.set_xlabel("Time (s)")
ax.set_ylabel("Relative α band power (%)")
plt.title("Relative alpha power")
plt.show()


# stream.disconnect()