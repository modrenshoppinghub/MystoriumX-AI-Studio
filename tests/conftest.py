"""
Global pytest configuration and fixtures for MystoriumX AI Studio.

Ensures the project root directory is added to sys.path so test suites
can cleanly import internal modules (models, engines, processors, etc.).
"""

import sys
from pathlib import Path
import pytest
import torch

# -----------------------------------------------------------------------------
# Module Path Setup
# -----------------------------------------------------------------------------
# Calculate project root directory (one level up from tests/)
PROJECT_ROOT = Path(__file__).parent.parent.resolve()

# Dynamically prepend root directory to sys.path if not already present
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# -----------------------------------------------------------------------------
# Shared Test Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture(scope="session")
def sample_rate() -> int:
    """Default sample rate fixture for audio tests."""
    return 48000


@pytest.fixture
def dummy_stereo_audio(sample_rate: int) -> torch.Tensor:
    """
    Generates a 2-channel, 1-second synthetic sine wave audio tensor
    formatted for PyTorch audio engines (channels, samples).
    """
    duration_sec = 1.0
    num_samples = int(sample_rate * duration_sec)
    t = torch.linspace(0, duration_sec, num_samples)
    
    # 440 Hz Sine Wave
    mono_signal = torch.sin(2 * 3.141592653589793 * 440.0 * t)
    
    # Stack to create stereo (2, num_samples)
    stereo_tensor = torch.stack([mono_signal, mono_signal], dim=0)
    return stereo_tensor
