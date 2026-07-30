"""
Audio Settings Module - Configures technical DSP parameters for generation output.
"""

from models.schemas import AudioTechnicalSettings
from utils import setup_logger

logger = setup_logger("AudioSettingsEngine")


class AudioSettingsEngine:
    """Manages spatial and technical audio rendering directives based on scene parameters."""

    @staticmethod
    def derive_settings(mood: str, energy_level: float) -> AudioTechnicalSettings:
        """Dynamically builds DSP parameters based on psychological context."""
        # Acoustic space scaling: darker/colder scenes get long wet reverbs
        if mood.lower() in ["dark", "cold", "isolation", "frozen", "mystery"]:
            decay = 3.8 + (1.0 - energy_level) * 1.5
            lufs = -16.0  # Dynamic range breathing room
        elif mood.lower() in ["epic", "adventure", "war documentary"]:
            decay = 2.0
            lufs = -12.0  # Louder, denser mix target
        else:
            decay = 2.4
            lufs = -14.0  # EBU R128 Standard

        logger.debug(f"Audio DSP derived: Reverb Decay={decay:.1f}s, Target LUFS={lufs}")
        return AudioTechnicalSettings(
            sample_rate_hz=48000,
            bit_depth=24,
            channels="Stereo",
            target_loudness_lufs=lufs,
            reverb_decay_sec=round(decay, 2)
        )
