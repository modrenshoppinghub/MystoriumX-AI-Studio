"""
Spectral Gating Noise Reduction Module.
Reduces background noise via spectral subtraction.
"""

import numpy as np
import torch
import scipy.signal

class NoiseReductionEngine:
    """Spectral Subtraction Noise Reduction Engine."""

    def __init__(self, sample_rate: int = 48000):
        self.sample_rate = sample_rate

    def reduce_noise(self, audio: torch.Tensor, noise_threshold_db: float = -40.0, reduction_ratio: float = 0.8) -> torch.Tensor:
        """Applies STFT spectral gating to attenuate noise floor."""
        numpy_audio = audio.cpu().numpy()
        output_channels = []

        for channel in numpy_audio:
            f, t, Zxx = scipy.signal.stft(channel, fs=self.sample_rate, nperseg=2048)
            magnitude = np.abs(Zxx)
            phase = np.angle(Zxx)

            threshold_linear = 10.0 ** (noise_threshold_db / 20.0)
            mask = magnitude > threshold_linear
            
            # Apply soft suppression matrix
            suppressed_mag = np.where(mask, magnitude, magnitude * (1.0 - reduction_ratio))
            Zxx_clean = suppressed_mag * np.exp(1j * phase)

            _, clean_audio = scipy.signal.istft(Zxx_clean, fs=self.sample_rate)
            output_channels.append(clean_audio[:channel.shape[0]])

        return torch.from_numpy(np.array(output_channels)).to(audio.device)
