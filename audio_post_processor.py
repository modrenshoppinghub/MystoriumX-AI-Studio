"""
Audio Processor Pipeline Orchestrator.
Manages high-level processing pipelines, GPU/CPU execution contexts, and audio streaming.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, Tuple, List
import numpy as np
import torch
import soundfile as sf
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MystoriumX.AudioProcessor")


@dataclass
class AudioBuffer:
    """In-memory representation of multitrack audio tensor."""
    data: torch.Tensor  # Shape: (channels, samples)
    sample_rate: int
    dtype: torch.dtype = torch.float32

    def to_device(self, device: torch.device) -> "AudioBuffer":
        return AudioBuffer(data=self.data.to(device), sample_rate=self.sample_rate, dtype=self.dtype)

    def to_numpy(self) -> np.ndarray:
        return self.data.cpu().numpy()


class BaseAudioProcessor:
    """Core DSP execution engine supporting PyTorch CUDA/CPU hardware acceleration."""

    def __init__(self, sample_rate: int = 48000, prefer_gpu: bool = True):
        self.sample_rate = sample_rate
        self.device = torch.device("cuda" if prefer_gpu and torch.cuda.is_available() else "cpu")
        logger.info(f"Initialized Audio Processing Engine on device: {self.device}")

    def load_audio(self, file_path: str) -> AudioBuffer:
        """Loads audio into GPU/CPU memory tensor."""
        data, sr = sf.read(file_path, dtype="float32", always_2d=True)
        # Convert (samples, channels) to PyTorch convention (channels, samples)
        tensor_data = torch.from_numpy(data.T).to(self.device)
        if sr != self.sample_rate:
            tensor_data = self.resample(tensor_data, sr, self.sample_rate)
        return AudioBuffer(data=tensor_data, sample_rate=self.sample_rate)

    def resample(self, tensor: torch.Tensor, orig_sr: int, target_sr: int) -> torch.Tensor:
        """High-quality polyphase audio resampling."""
        if orig_sr == target_sr:
            return tensor
        import torchaudio.transforms as T
        resampler = T.Resample(orig_sr, target_sr).to(self.device)
        return resampler(tensor)

    def process_stream(self, input_path: str, output_path: str, chunk_size: int = 65536) -> None:
        """Streaming chunk fallback processor for large audio files to manage memory footprint."""
        logger.info(f"Processing streaming file: {input_path}")
        with sf.SoundFile(input_path, 'r') as infile:
            sr = infile.samplerate
            channels = infile.channels
            with sf.SoundFile(output_path, 'w', samplerate=sr, channels=channels, subtype='PCM_24') as outfile:
                while infile.tell() < infile.frames:
                    chunk = infile.read(chunk_size, dtype='float32', always_2d=True)
                    tensor_chunk = torch.from_numpy(chunk.T).to(self.device)
                    # Inline stream safety processing
                    processed_chunk = tensor_chunk.cpu().numpy().T
                    outfile.write(processed_chunk)
