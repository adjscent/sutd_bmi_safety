import pandas as pd
import numpy as np
import argparse
import glob
import os
import matplotlib.pyplot as plt

def analyze_fft(file_path):
    df = pd.read_csv(file_path)
    act_channels = [col for col in df.columns if "Act" in col and "Action" not in col]

    sampling_rate = 500  # Fixed sampling rate
    results = {}

    for channel in act_channels:
        signal = pd.to_numeric(df[channel], errors='raise').fillna(0).values.astype(float)
        N = len(signal)

        fft_values = np.fft.fft(signal)
        frequencies = np.fft.fftfreq(N, 1 / sampling_rate)
        magnitude = np.abs(fft_values)

        mask = (frequencies > 0)  # Only positive frequencies
        frequencies = frequencies[mask]
        magnitude = magnitude[mask]

        # Get top 5 frequencies
        top_indices = np.argsort(magnitude)[::-1][:5]
        top_freqs = [(frequencies[i], magnitude[i]) for i in top_indices]

        results[channel] = {
            "frequencies": frequencies,
            "magnitude": magnitude,
            "top_freqs": top_freqs
        }
    
    return sampling_rate, results


def plot_and_save(results, action, attack_type, base_filename):
    output_dir = "graphs"
    os.makedirs(output_dir, exist_ok=True)

    for channel, data in results.items():
        frequencies = data["frequencies"]
        magnitude = data["magnitude"]
        top_freqs = data["top_freqs"]

        plt.figure(figsize=(10, 6))
        plt.plot(frequencies, magnitude, label=channel, linewidth=1)
        plt.title(f"FFT Spectrum - {channel}\nAction: {action}, Attack/Baseline: {attack_type}")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Magnitude")
        plt.grid(True)

        # Draw vertical lines for top 5 frequencies
        for freq, _ in top_freqs:
            plt.axvline(x=freq, color='r', linestyle='--', alpha=0.7)

        # Create a small table with top 5 frequencies & magnitudes
        cell_text = [[f"{freq:.2f}", f"{mag:.2f}"] for freq, mag in top_freqs]
        table = plt.table(
            cellText=cell_text,
            colLabels=["Frequency (Hz)", "Magnitude"],
            cellLoc="center",
            loc="upper right",
            colWidths=[0.2, 0.2]
        )
        table.scale(1, 1.2)  # Adjust table size

        plt.tight_layout()

        # Save plot
        save_path = os.path.join(output_dir, f"{base_filename}_{channel}.png")
        plt.savefig(save_path, dpi=300)
        plt.close()


def main():
    parser = argparse.ArgumentParser(description="FFT Frequency Analysis with Plotting")
    parser.add_argument("-p", "--pattern", help="File pattern for CSVs (e.g., './data/*.csv')", required=True)
    args = parser.parse_args()

    for file_path in glob.glob(args.pattern):
        filename = os.path.basename(file_path).replace(".csv", "")
        parts = filename.split("_")
        action = parts[1] if len(parts) > 1 else "unknown"
        attack_type = parts[2] if len(parts) > 2 else "unknown"

        sampling_rate, results = analyze_fft(file_path)
        plot_and_save(results, action, attack_type, filename)


if __name__ == "__main__":
    main()
