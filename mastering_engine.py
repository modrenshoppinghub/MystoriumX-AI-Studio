"""
Master Mastering Engine Pipeline Coordinator.
Chains EQ, Compression, Reverb, Ducking, Loudness Normalization, and Peak Limiting.
"""

from .audio_processor import BaseAudioProcessor, AudioBuffer
from .eq_engine import EqualizerEngine
from .compressor_engine import CompressorEngine
from .normalizer_engine import NormalizerEngine
from .limiter_engine import LimiterEngine
from .stereo_engine import StereoEngine
from .reverb_engine import ReverbEngine
from .ducking_engine import DuckingEngine
import torch

class MasteringEngine:
    """Unified Professional Mastering Chain for Documentary Soundtracks."""

    def __init__(self, sample_rate: int = 48000, prefer_gpu: bool = True):
        self.sample_rate = sample_rate
        self.base_proc = BaseAudioProcessor(sample_rate=sample_rate, prefer_gpu=prefer_gpu)
        self.eq = EqualizerEngine(sample_rate=sample_rate)
        self.compressor = CompressorEngine(sample_rate=sample_rate)
        self.normalizer = NormalizerEngine(sample_rate=sample_rate)
        self.limiter = LimiterEngine(sample_rate=sample_rate)
        self.stereo = StereoEngine()
        self.reverb = ReverbEngine(sample_rate=sample_rate)
        self.ducking = DuckingEngine(sample_rate=sample_rate)

    def master_soundtrack(
        self, 
        music_buffer: AudioBuffer, 
        narration_buffer: Optional[AudioBuffer] = None,
        target_lufs: float = -14.0,
        ceiling_db: float = -1.0
    ) -> AudioBuffer:
        """Executes full mastering pipeline across input audio buffers."""
        audio = music_buffer.data.to(self.base_proc.device)

        # Step 1: Voice Ducking (if narration present)
        if narration_buffer is not None:
            narration_data = narration_buffer.data.to(self.base_proc.device)
            audio = self.ducking.apply_ducking(audio, narration_data)

        # Step 2: Cinematic Parametric Equalization
        eq_bands = [
            {'freq': 80, 'gain': -2.0, 'q': 0.707},   # Sub rumble cleanup
            {'freq': 2500, 'gain': 1.5, 'q': 1.0},    # Presence push
            {'freq': 10000, 'gain': 2.0, 'q': 0.707}  # Air shelf
        ]
        audio = self.eq.apply_eq(audio, eq_bands)

        # Step 3: Dynamic Compression
        audio = self.compressor.process(audio, threshold_db=-20.0, ratio=3.0)

        # Step 4: Stereo Widening
        audio = self.stereo.adjust_width(audio, width_factor=1.2)

        # Step 5: Loudness Normalization (LUFS)
        audio = self.normalizer.normalize(audio, target_lufs=target_lufs)

        # Step 6: True Peak Brickwall Limiter
        audio = self.limiter.process(audio, ceiling_db=ceiling_db)

        return AudioBuffer(data=audio, sample_rate=self.sample_rate)
