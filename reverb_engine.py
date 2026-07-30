"""
Cinematic Room Reverb Engine.
Algorithmic comb and all-pass filter network (Schroeder Reverb Architecture).
"""

import torch
import numpy as np

class ReverbEngine:
    """Algorithmic Schroeder Reverb Generator for room depth."""

    def __init__(self, sample_rate: int = 48000):
        self.sample_rate = sample_rate

    def apply_reverb(self, audio: torch.Tensor, wet_dry_ratio: float = 0.2, room_size: float = 0.5) -> torch.Tensor:
        """Applies spatial reverb tail to audio tensor."""
        numpy_audio = audio.cpu().numpy()
        delay_ms = [29.7, 37.1, 41.1, 43.7] # Comb filter delay constants
        comb_delays = [int(self.sample_rate * (d / 1000.0) * room_size) for d in delay_ms]
        
        reverbed_channels = []
        for channel in numpy_audio:
            comb_outputs = np.zeros_like(channel)
            for delay in comb_delays:
                buffer = np.zeros(len(channel) + delay)
                for i in range(len(channel)):
                    buffer[i + delay] = channel[i] + buffer[i] * 0.7
                comb_outputs += buffer[:len(channel)]

            output = (channel * (1.0 - wet_dry_ratio)) + (comb_outputs * (wet_dry_ratio / len(comb_delays)))
            reverbed_channels.append(output)

        return torch.from_numpy(np.array(reverbed_channels)).to(audio.device)
