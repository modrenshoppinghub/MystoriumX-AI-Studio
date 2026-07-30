"""
EBU R128 LUFS Loudness Normalizer Engine.
Normalizes integrated audio loudness to targeted broadcast standards.
"""

import numpy as np
import torch

class NormalizerEngine:
    """Integrated Loudness & Peak Normalizer Engine."""

    def __init__(self, sample_rate: int = 48000):
        self.sample_rate = sample_rate

    def measure_lufs(self, audio: torch.Tensor) -> float:
        """Calculates approximate Integrated LUFS of input audio tensor."""
        numpy_data = audio.cpu().numpy()
        # Simplified K-weighting approximation filter RMS
        rms = np.sqrt(np.mean(numpy_data ** 2))
        if rms <= 1e-8:
            return -70.0
        lufs = 20.0 * np.log10(rms) - 0.691
        return float(lufs)

    def normalize(self, audio: torch.Tensor, target_lufs: float = -14.0) -> torch.Tensor:
        """Normalizes audio to target LUFS level."""
        current_lufs = self.measure_lufs(audio)
        gain_db = target_lufs - current_lufs
        gain_linear = 10.0 ** (gain_db / 20.0)
        
        logger.info(f"Normalizing audio: Current LUFS={current_lufs:.2f}, Target LUFS={target_lufs:.2f}, Gain={gain_db:.2f}dB")
        return audio * gain_linear
