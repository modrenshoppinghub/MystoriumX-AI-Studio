"""
Global Pytest Configuration & Test Fixtures for MystoriumX AI Studio.

Handles root module path resolution and provides reusable audio, system,
and tensor fixtures across all test modules.
"""

import sys
import os
from pathlib import Path
import tempfile
import pytest
import torch
import numpy as np

# -----------------------------------------------------------------------------
# 1. System Path Resolution
# -----------------------------------------------------------------------------
# Resolve absolute path to the project root directory (parent of tests/)
PROJECT_ROOT = Path(__file__).parent.parent.resolve()

# Prepend project root to sys.path to guarantee import discovery
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Set environment variable for child subprocesses or runner tools
os.environ["PYTHONPATH"] = str(PROJECT_ROOT)


# -----------------------------------------------------------------------------
# 2. Pytest Hooks & Environment Setup
# -----------------------------------------------------------------------------
def pytest_configure(config):
    """Registers custom markers for targeted test execution."""
    config.addinivalue_line(
        "markers", "gpu: mark test as requiring CUDA GPU availability"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running dynamic DSP benchmark"
    )


# -----------------------------------------------------------------------------
# 3. Core Engine Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture(scope="session")
def sample_rate() -> int:
    """Standard broadcast sample rate (48000 Hz)."""
    return 48000


@pytest.fixture(scope="session")
def cd_sample_rate() -> int:
    """CD quality sample rate (44100 Hz)."""
    return 44100


@pytest.fixture(scope="session")
def device() -> torch.device:
    """Determines PyTorch execution device for tests."""
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


# -----------------------------------------------------------------------------
# 4. Audio Tensor Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture
def dummy_mono_signal(sample_rate: int) -> torch.Tensor:
    """Generates 1 second of 440Hz sine wave (1 channel, N samples)."""
    duration = 1.0
    num_samples = int(sample_rate * duration)
    t = torch.linspace(0, duration, num_samples)
    signal = torch.sin(2 * np.pi * 440.0 * t)
    return signal.unsqueeze(0)  # Shape: (1, num_samples)


@pytest.fixture
def dummy_stereo_signal(sample_rate: int) -> torch.Tensor:
    """Generates 2 seconds of 440Hz stereo sine wave (2 channels, N samples)."""
    duration = 2.0
    num_samples = int(sample_rate * duration)
    t = torch.linspace(0, duration, num_samples)
    signal = torch.sin(2 * np.pi * 440.0 * t)
    return torch.stack([signal, signal], dim=0)  # Shape: (2, num_samples)


@pytest.fixture
def dummy_narration_signal(sample_rate: int) -> torch.Tensor:
    """
    Generates a synthetic narration signal containing active speech segments
    and silence intervals for sidechain ducking tests.
    """
    duration = 3.0
    num_samples = int(sample_rate * duration)
    signal = torch.zeros((1, num_samples))
    
    # Simulate speech voice burst between 1.0s and 2.0s
    start_idx = int(1.0 * sample_rate)
    end_idx = int(2.0 * sample_rate)
    t = torch.linspace(0, 1.0, end_idx - start_idx)
    speech_tone = torch.sin(2 * np.pi * 200.0 * t) * 0.8  # Fundamental human voice frequency
    
    signal[0, start_idx:end_idx] = speech_tone
    return signal.repeat(2, 1)  # Convert to stereo (2, num_samples)


# -----------------------------------------------------------------------------
# 5. Audio Buffer Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture
def mock_audio_buffer(dummy_stereo_signal: torch.Tensor, sample_rate: int):
    """Provides a instantiated AudioBuffer object using the primary processor."""
    from audio_processor import AudioBuffer
    return AudioBuffer(data=dummy_stereo_signal, sample_rate=sample_rate)


@pytest.fixture
def mock_narration_buffer(dummy_narration_signal: torch.Tensor, sample_rate: int):
    """Provides an AudioBuffer object containing narration audio."""
    from audio_processor import AudioBuffer
    return AudioBuffer(data=dummy_narration_signal, sample_rate=sample_rate)


# -----------------------------------------------------------------------------
# 6. File & Directory System Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture
def temp_output_dir():
    """Provides a temporary workspace directory cleaned up after test completion."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir
