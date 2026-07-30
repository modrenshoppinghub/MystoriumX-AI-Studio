"""
Dynamic Range Compressor Engine.
Implements sidechain-capable dynamics processing with variable threshold, ratio, attack, release, and knee.
"""

import torch

class CompressorEngine:
    """Dynamic Range Compressor for transient control and punch."""

    def __init__(self, sample_rate: int = 48000):
        self.sample_rate = sample_rate

    def process(
        self, 
        audio: torch.Tensor, 
        threshold_db: float = -18.0, 
        ratio: float = 4.0, 
        attack_ms: float = 10.0, 
        release_ms: float = 100.0,
        knee_db: float = 6.0
    ) -> torch.Tensor:
        """Applies dynamic range compression over the input audio tensor."""
        alpha_attack = torch.exp(torch.tensor(-1.0 / (self.sample_rate * (attack_ms / 1000.0))))
        alpha_release = torch.exp(torch.tensor(-1.0 / (self.sample_rate * (release_ms / 1000.0))))

        # Peak detection envelope
        abs_audio = torch.abs(audio)
        envelope = torch.zeros_like(abs_audio)
        
        for c in range(audio.shape[0]):
            curr_env = 0.0
            for s in range(audio.shape[1]):
                val = abs_audio[c, s]
                if val > curr_env:
                    curr_env = alpha_attack * curr_env + (1.0 - alpha_attack) * val
                else:
                    curr_env = alpha_release * curr_env + (1.0 - alpha_release) * val
                envelope[c, s] = curr_env

        # Convert envelope to dB
        env_db = 20.0 * torch.log10(envelope + 1e-8)

        # Gain calculation (Knee curve)
        gain_db = torch.zeros_like(env_db)
        over_thresh = env_db - threshold_db

        mask_knee = (over_thresh > -knee_db / 2.0) & (over_thresh < knee_db / 2.0)
        mask_above = over_thresh >= knee_db / 2.0

        gain_db[mask_knee] = -((1.0 / ratio) - 1.0) * ((over_thresh[mask_knee] + knee_db / 2.0) ** 2) / (2.0 * knee_db)
        gain_db[mask_above] = -((1.0 / ratio) - 1.0) * over_thresh[mask_above]

        # Convert gain back to linear
        gain_linear = 10.0 ** (gain_db / 20.0)
        return audio * gain_linear.to(audio.device)
