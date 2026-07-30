"""
Global Pytest Configuration & Fixture Suite for MystoriumX AI Studio.

Ensures zero-config module resolution across environments and provides
hardware auto-detection, signal generators, mock schemas, and temporary filesystem context.
"""

import os
import sys
import tempfile
from pathlib import Path
from typing import Generator

import numpy as np
import pytest
import torch

# -----------------------------------------------------------------------------
# 1. Core Module Resolution & Path Injection
# -----------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent.parent.resolve()

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ["PYTHONPATH"] = str(PROJECT_ROOT)


# -----------------------------------------------------------------------------
# 2. Pytest Configuration & Hardware Detection
# -----------------------------------------------------------------------------
def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers for targeted test execution."""
    config.addinivalue_line(
        "markers", "gpu: mark test as requiring CUDA GPU acceleration"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as a long-running DSP benchmark"
    )


def pytest_runtest_setup(item: pytest.Item) -> None:
    """Automatically skip tests marked with @pytest.mark.gpu if CUDA is unavailable."""
    for marker in item.iter_markers(name="gpu"):
        if not torch.cuda.is_available():
            pytest.skip("CUDA device unavailable; skipping GPU-accelerated test.")


# -----------------------------------------------------------------------------
# 3. Environment & Hardware Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture(scope="session")
def sample_rate() -> int:
    """Default broadcast audio sample rate (48000 Hz)."""
    return 48000


@pytest.fixture(scope="session")
def cd_sample_rate() -> int:
    """Standard CD audio sample rate (44100 Hz)."""
    return 44100


@pytest.fixture(scope="session")
def device() -> torch.device:
    """Returns CUDA device if available, falling back to CPU."""
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


# -----------------------------------------------------------------------------
# 4. Audio Tensor & Signal Generators
# -----------------------------------------------------------------------------
@pytest.fixture
def dummy_mono_signal(sample_rate: int) -> torch.Tensor:
    """Generates 1 second of a 440 Hz pure sine wave (1 channel, N samples)."""
    duration = 1.0
    num_samples = int(sample_rate * duration)
    t = torch.linspace(0, duration, num_samples)
    signal = torch.sin(2 * np.pi * 440.0 * t)
    return signal.unsqueeze(0)  # Shape: (1, num_samples)


@pytest.fixture
def dummy_stereo_signal(sample_rate: int) -> torch.Tensor:
    """Generates 2 seconds of a 440 Hz stereo sine wave (2 channels, N samples)."""
    duration = 2.0
    num_samples = int(sample_rate * duration)
    t = torch.linspace(0, duration, num_samples)
    signal = torch.sin(2 * np.pi * 440.0 * t)
    return torch.stack([signal, signal], dim=0)  # Shape: (2, num_samples)


@pytest.fixture
def dummy_narration_signal(sample_rate: int) -> torch.Tensor:
    """
    Generates a 3-second audio track containing periodic speech tones
    interspersed with silence for sidechain ducking testing.
    """
    duration = 3.0
    num_samples = int(sample_rate * duration)
    signal = torch.zeros((1, num_samples))
    
    # Active voice burst between 1.0s and 2.0s
    start_idx = int(1.0 * sample_rate)
    end_idx = int(2.0 * sample_rate)
    t = torch.linspace(0, 1.0, end_idx - start_idx)
    speech_tone = torch.sin(2 * np.pi * 220.0 * t) * 0.75  # Vocal frequency range
    
    signal[0, start_idx:end_idx] = speech_tone
    return signal.repeat(2, 1)  # Shape: (2, num_samples)


@pytest.fixture
def dummy_white_noise(sample_rate: int) -> torch.Tensor:
    """Generates 1 second of stereo uniform white noise for spectrum and EQ testing."""
    duration = 1.0
    num_samples = int(sample_rate * duration)
    noise = torch.rand((2, num_samples)) * 2.0 - 1.0
    return noise


# -----------------------------------------------------------------------------
# 5. Audio Buffer Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture
def mock_audio_buffer(dummy_stereo_signal: torch.Tensor, sample_rate: int):
    """Instantiates a primary AudioBuffer container."""
    from audio_processor import AudioBuffer
    return AudioBuffer(data=dummy_stereo_signal, sample_rate=sample_rate)


@pytest.fixture
def mock_narration_buffer(dummy_narration_signal: torch.Tensor, sample_rate: int):
    """Instantiates an AudioBuffer container populated with narration content."""
    from audio_processor import AudioBuffer
    return AudioBuffer(data=dummy_narration_signal, sample_rate=sample_rate)


# -----------------------------------------------------------------------------
# 6. Schema & Mock Data Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture
def sample_music_params():
    """Provides valid parameters for AI Music Generation testing."""
    return {
        "prompt": "Cinematic dark orchestral tension with heavy sub bass and strings",
        "duration": 15.0,
        "genre": "Cinematic",
        "tempo": 90,
        "lufs_target": -14.0
    }


# -----------------------------------------------------------------------------
# 7. Filesystem & Output Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture
def temp_output_dir() -> Generator[Path, None, None]:
    """Provides a clean temporary output directory that self-cleans post-test."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)
