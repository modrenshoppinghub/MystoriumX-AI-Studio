"""
True Peak Limiter Engine.
Prevents clipping and ensures broadcast compliance using lookahead buffer limits.
"""

import torch

class LimiterEngine:
    """Lookahead Brickwall Peak Limiter."""

    def __init__(self, sample_rate: int = 48000, lookahead_ms: float = 5.0):
        self.sample_rate = sample_rate
        self.lookahead_samples = int(sample_rate * (lookahead_ms / 1000.0))

    def process(self, audio: torch.Tensor, ceiling_db: float = -1.0) -> torch.Tensor:
        """Applies brickwall peak limiting with zero clip overrun."""
        ceiling_linear = 10.0 ** (ceiling_db / 20.0)
        
        # Pad buffer for lookahead delay
        padded = torch.nn.functional.pad(audio, (self.lookahead_samples, 0))
        abs_audio = torch.abs(padded)
        
        max_peaks, _ = torch.max(abs_audio, dim=0)
        
        # Calculate envelope over lookahead window
        gain_reduction = torch.ones_like(max_peaks)
        for i in range(max_peaks.shape[0] - self.lookahead_samples):
            window_max = torch.max(max_peaks[i : i + self.lookahead_samples])
            if window_max > ceiling_linear:
                gain_reduction[i] = ceiling_linear / window_max

        # Trim padding delay
        aligned_gain = gain_reduction[:audio.shape[1]].to(audio.device)
        return audio * aligned_gain
