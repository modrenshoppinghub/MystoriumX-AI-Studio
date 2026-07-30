"""
Pydantic Schemas for MystoriumX AI Studio Data Models
"""

from typing import List, Optional
from pydantic import BaseModel, Field

class SceneRaw(BaseModel):
    """Raw scene extracted from document source."""
    scene_number: int
    raw_text: str
    word_count: int

class EmotionAnalysis(BaseModel):
    """Multi-dimensional emotional and psychological profiling of a scene."""
    primary_emotion: str = Field(..., description="Dominant emotion (e.g., Awe, Tension, Sorrow)")
    energy_level: float = Field(..., ge=0.0, le=1.0, description="Normalized energy scale 0.0 to 1.0")
    suspense_level: float = Field(..., ge=0.0, le=1.0, description="Normalized suspense scale 0.0 to 1.0")

class MusicPlan(BaseModel):
    """Cinematic music score directive for a specific scene."""
    music_style: str = Field(..., description="Genre/Style directive (e.g., Ambient Minimalist, Orchestral Hybrid)")
    tempo_bpm: int = Field(..., ge=40, le=220, description="Recommended BPM")
    recommended_instruments: List[str] = Field(default_factory=list, description="Target instruments")

class SceneAnalysisOutput(BaseModel):
    """Full aggregated output schema for a single scene."""
    scene_number: int
    duration_estimate_sec: float
    text_excerpt: str
    emotion: EmotionAnalysis
    music_plan: MusicPlan

class StudioScriptReport(BaseModel):
    """Final JSON serializable studio report."""
    title: str
    total_scenes: int
    total_estimated_duration_sec: float
    scenes: List[SceneAnalysisOutput]
