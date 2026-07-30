"""
Fade and Crossfade Engines.
Applies smooth linear, logarithmic, or exponential fade transitions.
"""

import torch
import numpy as np

class FadeEngine:
    """Applies fade-in and fade-out envelopes."""

    def process_fade_in(self, audio: torch.Tensor, duration_sec: float, sample_rate: int = 48000, curve: str = "exponential") -> torch.Tensor:
        fade_samples = int(duration_sec * sample_rate)
        if fade_samples <= 0 or fade_samples > audio.shape[1]:
            return audio

        out = audio.clone()
        if curve == "linear":
            envelope = torch.linspace(0.0, 1.0, fade_samples, device=audio.device)
        else: # Exponential default
            envelope = torch.logspace(-2, 0, fade_samples, device=audio.device)
            envelope = (envelope - envelope.min()) / (envelope.max() - envelope.min())

        out[:, :fade_samples] *= envelope
        return out

    def process_fade_out(self, audio: torch.Tensor, duration_sec: float, sample_rate: int = 48000, curve: str = "exponential") -> torch.Tensor:
        fade_samples = int(duration_sec * sample_rate)
        if fade_samples <= 0 or fade_samples > audio.shape[1]:
            return audio

        out = audio.clone()
        if curve == "linear":
            envelope = torch.linspace(1.0, 0.0, fade_samples, device=audio.device)
        else: # Exponential default
            envelope = torch.logspace(0, -2, fade_samples, device=audio.device)
            envelope = (envelope - envelope.min()) / (envelope.max() - envelope.min())

        out[:, -fade_samples:] *= envelope
        return out


class CrossfadeEngine:
    """Crossfades between two distinct audio streams."""

    def crossfade(self, track1: torch.Tensor, track2: torch.Tensor, duration_sec: float, sample_rate: int = 48000) -> torch.Tensor:
        cf_samples = int(duration_sec * sample_rate)
        min_len = min(track1.shape[1], track2.shape[1])
        if cf_samples > min_len:
            cf_samples = min_len

        # Slice overlap regions
        t1_fade = track1[:, -cf_samples:]
        t2_fade = track2[:, :cf_samples]

        fade_out = torch.linspace(1.0, 0.0, cf_samples, device=track1.device)
        fade_in = torch.linspace(0.0, 1.0, cf_samples, device=track2.device)

        blended = (t1_fade * fade_out) + (t2_fade * fade_in)

        combined = torch.cat([track1[:, :-cf_samples], blended, track2[:, cf_samples:]], dim=1)
        return combined
