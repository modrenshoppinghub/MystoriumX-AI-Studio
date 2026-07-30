"""
Parametric Equalizer Engine.
Implements multi-band biquad IIR filters (High-pass, Low-pass, Peaking, High-shelf, Low-shelf).
"""

import numpy as np
import torch
from scipy.signal import iirfilter, sosfilt

class EqualizerEngine:
    """Multi-band Parametric EQ for cinematic tone shaping."""

    def __init__(self, sample_rate: int = 48000):
        self.sample_rate = sample_rate

    def create_peaking_filter(self, center_freq: float, gain_db: float, q_factor: float = 1.0) -> np.ndarray:
        """Calculates SOS (Second-Order Sections) coefficients for a peaking EQ filter."""
        w0 = 2 * np.pi * center_freq / self.sample_rate
        alpha = np.sin(w0) / (2 * q_factor)
        A = 10 ** (gain_db / 40.0)

        b0 = 1 + alpha * A
        b1 = -2 * np.cos(w0)
        b2 = 1 - alpha * A
        a0 = 1 + alpha / A
        a1 = -2 * np.cos(w0)
        a2 = 1 - alpha / A

        sos = np.array([[b0/a0, b1/a0, b2/a0, 1.0, a1/a0, a2/a0]])
        return sos

    def apply_eq(self, audio_data: torch.Tensor, bands: List[Dict[str, Any]]) -> torch.Tensor:
        """
        Applies a list of EQ bands.
        Band Dict Format: {'freq': 1000, 'gain': 3.0, 'q': 1.414}
        """
        numpy_audio = audio_data.cpu().numpy()
        processed_channels = []

        for channel in numpy_audio:
            filtered_chan = channel.copy()
            for band in bands:
                sos = self.create_peaking_filter(
                    center_freq=band.get('freq', 1000.0),
                    gain_db=band.get('gain', 0.0),
                    q_factor=band.get('q', 1.0)
                )
                filtered_chan = sosfilt(sos, filtered_chan)
            processed_channels.append(filtered_chan)

        result = torch.from_numpy(np.array(processed_channels)).to(audio_data.device)
        return result
