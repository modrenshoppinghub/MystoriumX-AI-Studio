"""
Provider Manager with Automatic Detection, Priority Routing, and Failover.
"""

from typing import List, Tuple, Optional
import numpy as np

from providers.base_provider import BaseMusicProvider
from providers.musicgen_provider import MusicGenProvider
from providers.ace_provider import ACEProvider
from providers.stableaudio_provider import StableAudioProvider
from models.schemas import AIMusicPromptOutput, MusicGenerationParams
from utils import setup_logger

logger = setup_logger("ProviderManager")


class ProviderManager:
    """Manages backend providers, runtime execution, and dynamic failovers."""

    def __init__(self, device: str = "cpu"):
        self.device = device
        self.providers: List[BaseMusicProvider] = [
            MusicGenProvider(device=device),
            ACEProvider(device=device),
            StableAudioProvider(device=device)
        ]
        self._initialize_providers()

    def _initialize_providers(self):
        """Initializes available providers."""
        for provider in self.providers:
            try:
                provider.initialize()
            except Exception as e:
                logger.warning(f"Provider '{provider.name}' initialization skipped: {e}")

    def generate_audio(
        self,
        prompt_data: AIMusicPromptOutput,
        params: MusicGenerationParams
    ) -> Tuple[np.ndarray, int, str]:
        """
        Attempts generation using priority order.
        Automatically fails over if a backend crashes.
        Returns (audio_data, sample_rate, provider_name_used).
        """
        last_error = None
        for provider in self.providers:
            try:
                logger.info(f"Attempting audio generation via provider '{provider.name}'...")
                audio, sr = provider.generate(prompt_data, params)
                logger.info(f"Successfully generated audio with '{provider.name}'.")
                return audio, sr, provider.name
            except Exception as e:
                logger.error(f"Provider '{provider.name}' failed during generation: {e}. Initiating failover...")
                last_error = e

        raise RuntimeError(f"All AI music providers failed. Final error: {last_error}")
