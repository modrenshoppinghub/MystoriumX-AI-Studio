"""
MystoriumX AI Studio - Pydantic Data Models and Schemas
Defines core data structures for audio parameters, AI music prompts, scene analysis, and studio reporting.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class AudioTechnicalSettings(BaseModel):
    """Technical audio settings for export and processing."""
    sample_rate: int = Field(default=48000, description="Audio sample rate in Hz")
    target_lufs: float = Field(default=-14.0, description="Target integrated loudness in LUFS")
    ceiling_db: float = Field(default=-1.0, description="True peak ceiling threshold in dB")
    channels: int = Field(default=2, description="Number of audio channels (1=Mono, 2=Stereo)")


class MusicGenerationParams(BaseModel):
    """Parameters passed to the AI music generation engine."""
    prompt: str = Field(..., description="Textual description or prompt for music generation")
    duration: float = Field(default=30.0, description="Duration of generated audio in seconds")
    genre: Optional[str] = Field(default="Cinematic", description="Primary musical genre")
    tempo: Optional[int] = Field(default=90, description="BPM tempo target")
    temperature: float = Field(default=1.0, description="Sampling temperature for AI generation model")


class AIMusicPromptOutput(BaseModel):
    """Structured output returned from AI prompt enhancement/generation engines."""
    raw_prompt: str = Field(..., description="Original user or scene prompt")
    enhanced_prompt: str = Field(..., description="Optimized prompt for audio foundation models")
    genre_tags: List[str] = Field(default_factory=list, description="Extracted genre and mood tags")
    estimated_bpm: int = Field(default=90, description="Estimated tempo for output composition")
    technical_settings: AudioTechnicalSettings = Field(default_factory=AudioTechnicalSettings)


class SceneRaw(BaseModel):
    """Raw scene description and timestamp metadata extracted during video analysis."""
    scene_id: int = Field(..., description="Sequential index of detected scene")
    start_time: float = Field(..., description="Scene start timestamp in seconds")
    end_time: float = Field(..., description="Scene end timestamp in seconds")
    description: str = Field(default="", description="Visual or textual description of scene content")
    intensity_score: float = Field(default=0.5, description="Relative mood/intensity rating (0.0 to 1.0)")
    dominant_mood: Optional[str] = Field(default="Neutral", description="Primary mood tag for scene")


class StudioScriptReport(BaseModel):
    """Consolidated orchestration report for full soundtrack mastering runs."""
    project_name: str = Field(..., description="Name of the studio project")
    total_duration: float = Field(..., description="Total runtime of processed soundtrack in seconds")
    detected_scenes: List[SceneRaw] = Field(default_factory=list, description="List of analyzed video scenes")
    generation_parameters: MusicGenerationParams = Field(...)
    export_paths: Dict[str, str] = Field(default_factory=dict, description="Map of exported file formats to paths")
    mastering_status: str = Field(default="SUCCESS", description="Execution status code")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional telemetric metadata")
