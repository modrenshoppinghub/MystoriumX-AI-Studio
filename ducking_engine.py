"""
Documentary Voice Ducking Engine.
Automatically attenuates background music tracks when narration is present.
"""

import torch

class DuckingEngine:
    """Sidechain voice ducking for clear narration clarity over music."""

    def __init__(self, sample_rate: int = 48000):
        self.sample_rate = sample_rate

    def apply_ducking(
        self, 
        music: torch.Tensor, 
        narration: torch.Tensor, 
        threshold_db: float = -30.0, 
        attenuation_db: float = -12.0,
        attack_ms: float = 20.0,
        release_ms: float = 300.0
    ) -> torch.Tensor:
        """Ducks background music based on narration presence."""
        # Align track lengths
        max_len = max(music.shape[1], narration.shape[1])
        if music.shape[1] < max_len:
            music = torch.nn.functional.pad(music, (0, max_len - music.shape[1]))
        if narration.shape[1] < max_len:
            narration = torch.nn.functional.pad(narration, (0, max_len - narration.shape[1]))

        # Voice activity threshold detection
        narration_mono = torch.mean(torch.abs(narration), dim=0)
        threshold_linear = 10.0 ** (threshold_db / 20.0)
        is_speech = (narration_mono > threshold_linear).float()

        # Smooth envelope (Attack / Release filters)
        alpha_att = torch.exp(torch.tensor(-1.0 / (self.sample_rate * (attack_ms / 1000.0))))
        alpha_rel = torch.exp(torch.tensor(-1.0 / (self.sample_rate * (release_ms / 1000.0))))

        control_env = torch.zeros_like(is_speech)
        curr = 0.0
        for i in range(is_speech.shape[0]):
            target = is_speech[i]
            if target > curr:
                curr = alpha_att * curr + (1.0 - alpha_att) * target
            else:
                curr = alpha_rel * curr + (1.0 - alpha_rel) * target
            control_env[i] = curr

        # Gain reduction calculation
        attenuation_linear = 10.0 ** (attenuation_db / 20.0)
        gain_curve = 1.0 - (control_env * (1.0 - attenuation_linear))

        return music * gain_curve.to(music.device)
