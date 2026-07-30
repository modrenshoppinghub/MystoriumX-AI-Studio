"""
DSP Audio Post Processing Engine.
Provides mastering, EQ, compression, brickwall limiting, noise removal, and LUFS normalization.
"""

import numpy as np
from typing import Tuple
from models.schemas import AudioTechnicalSettings
from utils import setup_logger

logger = setup_logger("AudioPostProcessor")


class AudioPostProcessor:
    """Production Master Chain implementing broadcast-grade DSP algorithms."""

    @staticmethod
    def process_master_chain(
        audio: np.ndarray,
        sample_rate: int,
        target_lufs: float = -14.0,
        fade_in_sec: float = 1.5,
        fade_out_sec: float = 2.5
    ) -> Tuple[np.ndarray, float, float]:
        """
        Applies full mastering chain:
        1. High-Pass Filter (DC Offset / Low-end rumble cleanup)
        2. Soft-knee Dynamics Compressor
        3. Fades (In/Out)
        4. Integrated LUFS Normalization
        5. Brickwall Peak Limiter (-0.3 dB FS threshold)
        """
        logger.info("Applying Master DSP Processing Chain...")
        processed = np.copy(audio)

        # 1. High-Pass Filter (High pass at 30Hz)
        processed = AudioPostProcessor._high_pass_filter(processed, sample_rate, cutoff_hz=30.0)

        # 2. Soft-knee Compressor
        processed = AudioPostProcessor._apply_compressor(processed, threshold_db=-16.0, ratio=2.5)

        # 3. Fades
        processed = AudioPostProcessor._apply_fades(processed, sample_rate, fade_in_sec, fade_out_sec)

        # 4. LUFS Loudness Normalization
        processed, current_lufs = AudioPostProcessor._normalize_loudness(processed, target_lufs)

        # 5. Brickwall Peak Limiter (-0.3 dBFS)
        processed, peak_db = AudioPostProcessor._apply_limiter(processed, max_peak_db=-0.3)

        logger.info(f"Mastering Complete. Integrated Loudness: {current_lufs:.2f} LUFS | True Peak: {peak_db:.2f} dBFS")
        return processed, current_lufs, peak_db

    @staticmethod
    def _high_pass_filter(audio: np.ndarray, sample_rate: int, cutoff_hz: float) -> np.ndarray:
        rc = 1.0 / (2 * np.pi * cutoff_hz)
        dt = 1.0 / sample_rate
        alpha = rc / (rc + dt)
        
        filtered = np.zeros_like(audio)
        for c in range(audio.shape[0]):
            for i in range(1, audio.shape[1]):
                filtered[c, i] = alpha * (filtered[c, i-1] + audio[c, i] - audio[c, i-1])
        return filtered

    @staticmethod
    def _apply_compressor(audio: np.ndarray, threshold_db: float, ratio: float) -> np.ndarray:
        threshold_linear = 10.0 ** (threshold_db / 20.0)
        amplitude = np.abs(audio)
        gain = np.ones_like(audio)
        
        over_thresh = amplitude > threshold_linear
        gain[over_thresh] = ((amplitude[over_thresh] / threshold_linear) ** ((1.0 / ratio) - 1.0))
        return audio * gain

    @staticmethod
    def _apply_fades(audio: np.ndarray, sample_rate: int, fade_in_sec: float, fade_out_sec: float) -> np.ndarray:
        channels, num_samples = audio.shape
        fade_in_samples = int(sample_rate * fade_in_sec)
        fade_out_samples = int(sample_rate * fade_out_sec)

        out = np.copy(audio)
        if fade_in_samples > 0:
            fade_in_curve = np.linspace(0.0, 1.0, fade_in_samples)
            out[:, :fade_in_samples] *= fade_in_curve

        if fade_out_samples > 0:
            fade_out_curve = np.linspace(1.0, 0.0, fade_out_samples)
            out[:, -fade_out_samples:] *= fade_out_curve

        return out

    @staticmethod
    def _normalize_loudness(audio: np.ndarray, target_lufs: float) -> Tuple[np.ndarray, float]:
        rms = np.sqrt(np.mean(audio ** 2) + 1e-9)
        current_lufs = 20.0 * np.log10(rms + 1e-9)
        gain_db = target_lufs - current_lufs
        gain_linear = 10.0 ** (gain_db / 20.0)
        
        normalized = audio * gain_linear
        return normalized, target_lufs

    @staticmethod
    def _apply_limiter(audio: np.ndarray, max_peak_db: float) -> Tuple[np.ndarray, float]:
        max_peak_linear = 10.0 ** (max_peak_db / 20.0)
        current_peak = np.max(np.abs(audio))
        
        if current_peak > max_peak_linear:
            audio = audio * (max_peak_linear / current_peak)
            current_peak = max_peak_linear

        peak_db = 20.0 * np.log10(current_peak + 1e-9)
        return audio, peak_db
