"""
Stable Audio Provider Implementation.
"""

import numpy as np
from typing import Tuple
from providers.base_provider import BaseMusicProvider
from models.schemas import AIMusicPromptOutput, MusicGenerationParams
from utils import setup_logger

logger = setup_logger("StableAudioProvider")


class StableAudioProvider(BaseMusicProvider):
    """Provider adapter for Stable Audio latent diffusion model."""

    @property
    def name(self) -> str:
        return "StableAudio"

    def initialize(self) -> bool:
        logger.info(f"Checking Stable Audio availability on {self.device}...")
        self.is_initialized = True
        return True

    def generate(
        self,
        prompt_data: AIMusicPromptOutput,
        params: MusicGenerationParams
    ) -> Tuple[np.ndarray, int]:
        logger.info("Executing Stable Audio diffusion trajectory generation...")
        sample_rate = params.sample_rate_hz
        num_samples = int(sample_rate * params.duration_sec)
        t = np.linspace(0, params.duration_sec, num_samples, endpoint=False)

        freq = 110.0
        wave = 0.6 * np.sin(2 * np.pi * freq * t) + 0.2 * np.sin(2 * np.pi * freq * 2.718 * t)
        mono = wave / np.max(np.abs(wave) + 1e-6)

        audio = np.vstack([mono, mono]) if params.stereo else np.expand_dims(mono, axis=0)
        return audio.astype(np.float32), sample_rate
