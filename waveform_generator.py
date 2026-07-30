"""
Waveform, Frequency Spectrum, and Loudness Analyzer Visualization Engine.
Generates production preview graphics for exported soundtrack assets.
"""

import matplotlib
matplotlib.use('Agg')  # Headless backend rendering
import matplotlib.pyplot as plt
import numpy as np
import torch

class WaveformGenerator:
    """Generates professional visual diagnostic plots."""

    def generate_all_plots(self, audio: torch.Tensor, sample_rate: int, output_image_path: str) -> None:
        """Renders combined waveform preview, frequency spectrum, and loudness profile graphics."""
        numpy_data = audio.cpu().numpy()
        mono_signal = np.mean(numpy_data, axis=0)
        time_axis = np.linspace(0, len(mono_signal) / sample_rate, num=len(mono_signal))

        fig, axes = plt.subplots(3, 1, figsize=(12, 10))
        fig.tight_layout(pad=4.0)

        # Plot 1: Audio Waveform Preview
        axes[0].plot(time_axis, mono_signal, color='#1DB954', alpha=0.8)
        axes[0].set_title("Audio Waveform Preview")
        axes[0].set_xlabel("Time (seconds)")
        axes[0].set_ylabel("Amplitude")
        axes[0].grid(True, linestyle="--", alpha=0.5)

        # Plot 2: Frequency Spectrum Analysis (FFT)
        fft_spectrum = np.abs(np.fft.rfft(mono_signal))
        freq_axis = np.fft.rfftfreq(len(mono_signal), d=1.0/sample_rate)
        axes[1].semilogx(freq_axis, 20 * np.log10(fft_spectrum + 1e-8), color='#BB86FC')
        axes[1].set_title("Frequency Spectrum (FFT)")
        axes[1].set_xlabel("Frequency (Hz)")
        axes[1].set_ylabel("Magnitude (dB)")
        axes[1].grid(True, which="both", linestyle="--", alpha=0.5)

        # Plot 3: Dynamic RMS Loudness Curve
        frame_size = int(sample_rate * 0.1) # 100ms window
        rms_env = [
            np.sqrt(np.mean(mono_signal[i:i+frame_size]**2))
            for i in range(0, len(mono_signal) - frame_size, frame_size)
        ]
        rms_db = 20 * np.log10(np.array(rms_env) + 1e-8)
        rms_time = np.linspace(0, len(mono_signal) / sample_rate, num=len(rms_db))

        axes[2].plot(rms_time, rms_db, color='#FF4081')
        axes[2].set_title("Loudness Graph (RMS Envelope)")
        axes[2].set_xlabel("Time (seconds)")
        axes[2].set_ylabel("Loudness (dB)")
        axes[2].grid(True, linestyle="--", alpha=0.5)

        plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
        plt.close()
