"""
Pydantic Schemas for MystoriumX AI Studio Data Models (Phase 1 & Phase 2)
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class SceneRaw(BaseModel):
    """Raw scene extracted from document source."""
    scene_number: int
    raw_text: str
    word_count: int


class EmotionAnalysis(BaseModel):
    """Multi-dimensional emotional and psychological profiling of a scene."""
    primary_emotion: str = Field(..., description="Dominant emotion (e.g., Fear, Mystery, Hope)")
    energy_level: float = Field(..., ge=0.0, le=1.0, description="Normalized energy scale 0.0 to 1.0")
    suspense_level: float = Field(..., ge=0.0, le=1.0, description="Normalized suspense scale 0.0 to 1.0")


class MusicPlan(BaseModel):
    """Cinematic music score directive for a specific scene."""
    music_style: str = Field(..., description="Genre/Style directive")
    tempo_bpm: int = Field(..., ge=40, le=220, description="Recommended BPM")
    recommended_instruments: List[str] = Field(default_factory=list, description="Target instruments")


class SceneAnalysisOutput(BaseModel):
    """Full aggregated output schema for a single scene in Phase 1."""
    scene_number: int
    duration_estimate_sec: float
    text_excerpt: str
    emotion: EmotionAnalysis
    music_plan: MusicPlan


class StudioScriptReport(BaseModel):
    """Final JSON serializable studio report for Phase 1."""
    title: str
    total_scenes: int
    total_estimated_duration_sec: float
    scenes: List[SceneAnalysisOutput]


# =====================================================================
# PHASE 2 SCHEMAS
# =====================================================================

class AudioTechnicalSettings(BaseModel):
    """Audio DSP parameters for music generation targets."""
    sample_rate_hz: int = Field(default=48000, description="Sampling rate in Hz")
    bit_depth: int = Field(default=24, description="Audio bit depth")
    channels: str = Field(default="Stereo", description="Audio channel configuration")
    target_loudness_lufs: float = Field(default=-14.0, description="Integrated loudness standard")
    reverb_decay_sec: float = Field(default=2.5, description="Acoustic space decay time in seconds")


class AIMusicPromptOutput(BaseModel):
    """Structured AI Music Generation Output for Phase 2."""
    scene: int
    prompt: str = Field(..., description="Fully engineered and optimized prompt string")
    tempo: int = Field(..., ge=40, le=220, description="BPM tempo")
    key: str = Field(..., description="Musical Key and Scale (e.g., D Minor)")
    style: str = Field(..., description="Documentary style descriptor")
    genre: str = Field(..., description="Broad music classification")
    mood: str = Field(..., description="Primary atmosphere/mood")
    energy: str = Field(..., description="Qualitative energy descriptor (Low, Medium, High, Extreme)")
    intensity: float = Field(..., ge=0.0, le=1.0, description="Normalized intensity level")
    atmosphere: str = Field(..., description="Acoustic space or soundscape environment")
    buildup_structure: str = Field(..., description="Dynamic progression type")
    ending_style: str = Field(..., description="Musical resolution style")
    instruments: List[str] = Field(default_factory=list, description="Selected orchestration array")
    network_preset: str = Field(..., description="Target network aesthetic template applied")
    audio_settings: AudioTechnicalSettings = Field(default_factory=AudioTechnicalSettings)


class Phase2StudioReport(BaseModel):
    """Complete aggregated Phase 2 production output."""
    project_title: str
    total_scenes_processed: int
    prompts: List[AIMusicPromptOutput]
