"""
Pydantic Schemas Extension for MystoriumX AI Studio (Phase 3 Engine)
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class MusicGenerationParams(BaseModel):
    """Execution parameters controlling synthesis and DSP generation."""
    duration_sec: float = Field(default=30.0, ge=1.0, le=600.0, description="Target clip duration")
    seed: int = Field(default=-1, description="Random seed (-1 for random non-deterministic)")
    temperature: float = Field(default=1.0, ge=0.1, le=2.0, description="Sampling randomness scale")
    top_p: float = Field(default=0.95, ge=0.0, le=1.0, description="Nucleus sampling threshold")
    top_k: int = Field(default=250, ge=0, description="Top-k tokens considered")
    guidance_scale: float = Field(default=3.0, ge=1.0, le=20.0, description="Classifier-free guidance scale")
    sample_rate_hz: int = Field(default=48000, description="Target output sample rate in Hz")
    stereo: bool = Field(default=True, description="Stereo output toggle")
    fade_in_sec: float = Field(default=1.5, ge=0.0, description="Fade in duration")
    fade_out_sec: float = Field(default=2.5, ge=0.0, description="Fade out duration")
    loop_mode: bool = Field(default=False, description="Seamless loop synthesis tag")


class GenerationExportResult(BaseModel):
    """Complete metadata record for rendered scene audio exports."""
    scene_number: int
    provider_used: str
    prompt_used: str
    wav_path: str
    mp3_path: str
    waveform_png_path: str
    metadata_json_path: str
    actual_duration_sec: float
    sample_rate_hz: int
    bit_depth: int
    channels: int
    peak_db: float
    integrated_lufs: float
    generation_time_sec: float
