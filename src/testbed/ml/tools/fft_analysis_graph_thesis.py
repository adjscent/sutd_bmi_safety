import pandas as pd
import numpy as np
import argparse
import glob
import os
import matplotlib.pyplot as plt
from collections import defaultdict

def analyze_fft_per_action(file_paths, sampling_rate=500, interp_points=1024):
    """
    Compute average FFT magnitude per channel for a list of files of the same action.
    Resamples all FFTs to a fixed number of frequency bins for averaging.
    """
    fft_sums = defaultdict(lambda: None)
    count = 0

    # Define a common frequency axis (0 to Nyquist)
    nyquist = sampling_rate / 2
    common_freqs = np.linspace(0, nyquist, interp_points)

    for file_path in file_paths:
        df = pd.read_csv(file_path)
        act_channels = [col for col in df.columns if "Act" in col and "Action" not in col]

        for channel in act_channels:
            signal = pd.to_numeric(df[channel], errors='coerce').fillna(0).values.astype(float)
            N = len(signal)

            fft_values = np.fft.fft(signal)
            frequencies = np.fft.fftfreq(N, 1 / sampling_rate)
            magnitude = np.abs(fft_values)
            mask = frequencies > 0
            frequencies = frequencies[mask]
            magnitude = magnitude[mask]

            # Interpolate magnitude to common frequency axis
            interp_mag = np.interp(common_freqs, frequencies, magnitude)

            if fft_sums[channel] is None:
                fft_sums[channel] = interp_mag
            else:
                fft_sums[channel] += interp_mag

        count += 1

    # Average magnitudes
    averaged_results = {
        channel: (common_freqs, summed_mag / count)
        for channel, summed_mag in fft_sums.items()
    }

    return averaged_results


def plot_all_channels(actions_data):
    """
    actions_data: {action_name: {channel: (frequencies, magnitude)}}
    Generates 1 plot per channel with 9 curves (one per action).
    """
    output_dir = "graphs_avg"
    os.makedirs(output_dir, exist_ok=True)

    # Get all unique channels
    all_channels = set()
    for action_data in actions_data.values():
        all_channels.update(action_data.keys())

    for channel in sorted(all_channels):
        plt.figure(figsize=(12, 6))

        for action, channel_data in actions_data.items():
            if channel not in channel_data:
                continue
            frequencies, magnitude = channel_data[channel]
            plt.plot(frequencies, magnitude, label=action, linewidth=1)

        plt.title(f"Average FFT per Action - {channel}")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Magnitude")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"FFT_{channel}_all_actions.png"), dpi=300)
        plt.close()


def main():
    parser = argparse.ArgumentParser(description="Average FFT per Action across files")
    parser.add_argument("-p", "--pattern", help="File pattern for CSVs (e.g., './data/*.csv')", required=True)
    args = parser.parse_args()

    files = glob.glob(args.pattern)
    if not files:
        print("No files found for pattern:", args.pattern)
        return

    # Group files by action
    action_groups = defaultdict(list)
    for file_path in files:
        filename = os.path.basename(file_path).replace(".csv", "")
        parts = filename.split("_")
        action = parts[1] if len(parts) > 1 else "unknown"
        action_groups[action].append(file_path)

    # Compute average FFT per action
    actions_data = {}
    for action, file_list in action_groups.items():
        actions_data[action] = analyze_fft_per_action(file_list)

    # Plot per channel across all actions
    plot_all_channels(actions_data)


if __name__ == "__main__":
    main()
