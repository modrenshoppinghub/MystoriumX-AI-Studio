"""
Global Pytest Configuration & Automated Fixture Suite for MystoriumX AI Studio.

Handles zero-config root path injection, hardware auto-detection (CPU/CUDA),
dynamic signal generator factories, schema fixtures, and temporary filesystem isolation.
"""

import os
import sys
import tempfile
from pathlib import Path
from typing import Callable, Generator

import numpy as np
import pytest
import torch

# -----------------------------------------------------------------------------
# 1. Project Root & Subprocess Path Resolution
# -----------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent.parent.resolve()

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Enforce environment variable for subprocesses and parallel pytest workers
os.environ["PYTHONPATH"] = str(PROJECT_ROOT)


# -----------------------------------------------------------------------------
# 2. Pytest Execution Hooks & GPU Auto-Skip
# -----------------------------------------------------------------------------
def pytest_configure(config: pytest.Config) -> None:
    """Registers custom markers for test suite execution filtering."""
    config.addinivalue_line(
        "markers", "gpu: mark test as requiring CUDA GPU hardware acceleration"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as an intensive DSP dynamic processing benchmark"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an end-to-end multi-engine integration test"
    )


def pytest_runtest_setup(item: pytest.Item) -> None:
    """Auto-skips GPU tests when running on CPU-only runners (e.g., standard CI runners)."""
    for marker in item.iter_markers(name="gpu"):
        if not torch.cuda.is_available():
            pytest.skip("CUDA hardware unavailable — skipping GPU-accelerated test.")


# -----------------------------------------------------------------------------
# 3. Environment & Target Hardware Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture(scope="session")
def sample_rate() -> int:
    """Default high-fidelity sample rate (48000 Hz)."""
    return 48000


@pytest.fixture(scope="session")
def cd_sample_rate() -> int:
    """Standard CD audio sample rate (44100 Hz)."""
    return 44100


@pytest.fixture(scope="session")
def compute_device() -> torch.device:
    """Returns CUDA device if available, falling back to CPU."""
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


# -----------------------------------------------------------------------------
# 4. Dynamic Audio Signal Generators (Factories & Tensors)
# -----------------------------------------------------------------------------
@pytest.fixture
def make_sine_wave() -> Callable[[float, float, int, int], torch.Tensor]:
    """
    Factory fixture to generate arbitrary multi-channel sine wave tensors.
    Usage: `tensor = make_sine_wave(freq=880.0, duration=2.5, channels=2, sr=48000)`
    """
    def _generator(
        freq: float = 440.0,
        duration: float = 1.0,
        channels: int = 2,
        sr: int = 48000
    ) -> torch.Tensor:
        num_samples = int(sr * duration)
        t = torch.linspace(0, duration, num_samples)
        mono = torch.sin(2 * np.pi * freq * t)
        return mono.repeat(channels, 1)

    return _generator


@pytest.fixture
def dummy_mono_signal(sample_rate: int, make_sine_wave) -> torch.Tensor:
    """Generates 1 second of a 440 Hz monophonic sine wave (1, N)."""
    return make_sine_wave(freq=440.0, duration=1.0, channels=1, sr=sample_rate)


@pytest.fixture
def dummy_stereo_signal(sample_rate: int, make_sine_wave) -> torch.Tensor:
    """Generates 2 seconds of a 440 Hz stereo sine wave (2, N)."""
    return make_sine_wave(freq=440.0, duration=2.0, channels=2, sr=sample_rate)


@pytest.fixture
def dummy_narration_signal(sample_rate: int) -> torch.Tensor:
    """
    Generates a 3-second audio track containing speech-range sine bursts (200 Hz)
    surrounded by zero-amplitude silence for sidechain ducking validation.
    """
    duration = 3.0
    num_samples = int(sample_rate * duration)
    signal = torch.zeros((1, num_samples))
    
    # Active voice burst between 1.0s and 2.0s
    start_idx = int(1.0 * sample_rate)
    end_idx = int(2.0 * sample_rate)
    t = torch.linspace(0, 1.0, end_idx - start_idx)
    speech_tone = torch.sin(2 * np.pi * 200.0 * t) * 0.8
    
    signal[0, start_idx:end_idx] = speech_tone
    return signal.repeat(2, 1)  # Stereo output (2, N)


@pytest.fixture
def dummy_white_noise(sample_rate: int) -> torch.Tensor:
    """Generates 1 second of stereo uniform white noise for spectrum analysis and EQ tests."""
    duration = 1.0
    num_samples = int(sample_rate * duration)
    return torch.rand((2, num_samples)) * 2.0 - 1.0


# -----------------------------------------------------------------------------
# 5. AudioBuffer Container Fixtures with Safe Imports
# -----------------------------------------------------------------------------
@pytest.fixture
def mock_audio_buffer(dummy_stereo_signal: torch.Tensor, sample_rate: int):
    """Instantiates a standard AudioBuffer object."""
    try:
        from audio_processor import AudioBuffer
        return AudioBuffer(data=dummy_stereo_signal, sample_rate=sample_rate)
    except ImportError:
        from audio import AudioBuffer
        return AudioBuffer(data=dummy_stereo_signal, sample_rate=sample_rate)


@pytest.fixture
def mock_narration_buffer(dummy_narration_signal: torch.Tensor, sample_rate: int):
    """Instantiates an AudioBuffer populated with speech narration audio."""
    try:
        from audio_processor import AudioBuffer
        return AudioBuffer(data=dummy_narration_signal, sample_rate=sample_rate)
    except ImportError:
        from audio import AudioBuffer
        return AudioBuffer(data=dummy_narration_signal, sample_rate=sample_rate)


# -----------------------------------------------------------------------------
# 6. Schema & Mock Parameter Payload Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture
def sample_generation_params() -> dict:
    """Provides standard prompt and parameters for AI Music Generation testing."""
    return {
        "prompt": "Cinematic dark thriller soundtrack, intense low brass and swelling strings",
        "duration": 10.0,
        "genre": "Cinematic",
        "tempo": 90,
        "target_lufs": -14.0
    }


# -----------------------------------------------------------------------------
# 7. Filesystem & Temporary Workplace Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture
def temp_output_dir() -> Generator[Path, None, None]:
    """
    Yields a temporary directory as a `Path` object that automatically 
    cleans up all generated files upon test completion.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)
