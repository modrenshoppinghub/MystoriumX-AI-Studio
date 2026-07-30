"""
Unit tests for Phase 3 Audio Generation & DSP Engines.
"""

import pytest
import numpy as np
from pathlib import Path
from models.schemas import AIMusicPromptOutput, MusicGenerationParams, AudioTechnicalSettings
from providers.provider_manager import ProviderManager
from audio_post_processor import AudioPostProcessor


def test_provider_manager_fallback():
    manager = ProviderManager(device="cpu")
    dummy_prompt = AIMusicPromptOutput(
        scene=1,
        prompt="Dark ambient score",
        tempo=60,
        key="D Minor",
        style="Mystery",
        genre="Ambient",
        mood="Dark",
        energy="Low",
        intensity=0.2,
        atmosphere="Cold",
        buildup_structure="Linear",
        ending_style="Fade",
        instruments=["Sub-bass"],
        network_preset="BBC Documentary",
        audio_settings=AudioTechnicalSettings()
    )
    params = MusicGenerationParams(duration_sec=2.0)
    audio, sr, provider_used = manager.generate_audio(dummy_prompt, params)
    
    assert audio.shape[0] == 2  # Stereo
    assert sr == 48000
    assert provider_used in ["MusicGen", "ACE-Step", "StableAudio"]


def test_audio_post_processor_mastering():
    sr = 48000
    duration = 2.0
    t = np.linspace(0, duration, int(sr * duration))
    raw_mono = np.sin(2 * np.pi * 440.0 * t) * 0.8
    raw_stereo = np.vstack([raw_mono, raw_mono])

    mastered, lufs, peak_db = AudioPostProcessor.process_master_chain(
        raw_stereo, sample_rate=sr, target_lufs=-14.0
    )

    assert mastered.shape == raw_stereo.shape
    assert peak_db <= -0.3
    assert not np.isnan(mastered).any()
