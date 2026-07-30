"""
Abstract Base Provider for MystoriumX AI Music Backends.
"""

from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any
import numpy as np

from models.schemas import AIMusicPromptOutput, MusicGenerationParams


class BaseMusicProvider(ABC):
    """Standardized Interface for AI Music Generation Backends."""

    def __init__(self, device: str = "cpu"):
        self.device = device
        self.is_initialized = False

    @abstractmethod
    def initialize(self) -> bool:
        """Loads underlying model checkpoints into hardware memory."""
        pass

    @abstractmethod
    def generate(
        self,
        prompt_data: AIMusicPromptOutput,
        params: MusicGenerationParams
    ) -> Tuple[np.ndarray, int]:
        """
        Executes text-to-audio synthesis.
        Returns tuple of (numpy audio array of shape [channels, samples], sample_rate).
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns provider identification string."""
        pass
