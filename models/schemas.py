"""
MystoriumX AI Studio - Core Data Models and Pydantic Schemas

Defines type-checked data structures, parameters, and telemetry contracts 
used across video scene detection, prompt enhancement, music synthesis, 
multitrack assembly, and studio script rendering pipelines.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, validator


# =============================================================================
# 1. Enums & Base Utility Types
# =============================================================================

class ExportFormat(str, Enum):
    """Supported export audio container formats."""
    WAV = "wav"
    MP3 = "mp3"
    FLAC = "flac"
    OGG = "ogg"


class MasteringPreset(str, Enum):
    """Pre-configured target loudness standards."""
    STREAMING = "streaming"    # -14 LUFS, Peak -1.0 dB
    BROADCAST = "broadcast"    # -24 LUFS, Peak -2.0 dB
    CLUB = "club"              # -9 LUFS, Peak -0.3 dB
    CINEMATIC = "cinematic"    # -20 LUFS, Peak -2.0 dB


# =============================================================================
# 2. Low-Level Audio & Generation Schemas
# =============================================================================

class AudioTechnicalSettings(BaseModel):
    """Technical audio specifications and target mastering constraints."""
    sample_rate: int = Field(default=48000, ge=8000, le=192000, description="Audio sample rate in Hz")
    target_lufs: float = Field(default=-14.0, ge=-60.0, le=0.0, description="Target integrated loudness in LUFS")
    ceiling_db: float = Field(default=-1.0, ge=-20.0, le=0.0, description="True peak ceiling threshold in dB")
    channels: int = Field(default=2, ge=1, le=8, description="Number of audio channels (1=Mono, 2=Stereo, 6=5.1)")
    bit_depth: int = Field(default=24, ge=16, le=32, description="Target bit depth for output render")


class MusicGenerationParams(BaseModel):
    """Execution parameters controlling AI synthesis and DSP post-processing."""
    prompt: str = Field(..., min_length=1, description="Textual description or prompt for music generation")
    duration: float = Field(default=30.0, ge=1.0, le=600.0, description="Duration of generated audio in seconds")
    duration_sec: float = Field(default=30.0, ge=1.0, le=600.0, description="Alias for duration parameter")
    genre: Optional[str] = Field(default="Cinematic", description="Primary musical genre")
    tempo: Optional[int] = Field(default=90, ge=30, le=300, description="BPM tempo target")
    seed: int = Field(default=-1, description="Random seed (-1 for random non-deterministic generation)")
    temperature: float = Field(default=1.0, ge=0.1, le=2.0, description="Sampling randomness scale")
    top_p: float = Field(default=0.95, ge=0.0, le=1.0, description="Nucleus sampling threshold")
    top_k: int = Field(default=250, ge=0, description="Top-k tokens considered")
    guidance_scale: float = Field(default=3.0, ge=1.0, le=20.0, description="Classifier-free guidance scale")
    sample_rate_hz: int = Field(default=48000, ge=8000, le=192000, description="Target output sample rate in Hz")
    stereo: bool = Field(default=True, description="Stereo output toggle")
    fade_in_sec: float = Field(default=1.5, ge=0.0, description="Fade in duration in seconds")
    fade_out_sec: float = Field(default=2.5, ge=0.0, description="Fade out duration in seconds")
    loop_mode: bool = Field(default=False, description="Seamless loop synthesis tag")

    @validator("duration_sec", always=True)
    def sync_duration_sec(cls, v: float, values: Dict[str, Any]) -> float:
        """Keeps duration and duration_sec fields perfectly synchronized."""
        if "duration" in values and values["duration"] != 30.0 and v == 30.0:
            return values["duration"]
        return v


class AIMusicPromptOutput(BaseModel):
    """Structured output returned from AI prompt enhancement/generation engines."""
    raw_prompt: str = Field(..., description="Original user or scene prompt")
    enhanced_prompt: str = Field(..., description="Optimized prompt for audio foundation models")
    genre_tags: List[str] = Field(default_factory=list, description="Extracted genre and mood tags")
    estimated_bpm: int = Field(default=90, ge=30, le=300, description="Estimated tempo for output composition")
    technical_settings: AudioTechnicalSettings = Field(default_factory=AudioTechnicalSettings)


class UserPrompt(BaseModel):
    """User input wrapper containing contextual directives for script generation."""
    prompt_text: str = Field(..., min_length=1, description="Raw input prompt provided by user")
    style_preference: Optional[str] = Field(default="Cinematic", description="Preferred artistic or musical style")
    intensity: float = Field(default=0.5, ge=0.0, le=1.0, description="Emotional intensity scale")
    target_duration: Optional[float] = Field(default=None, ge=1.0, description="Requested total duration in seconds")
    additional_notes: Optional[str] = Field(default=None, description="Custom directives or workflow notes")


# =============================================================================
# 3. Media Assets & Timeline Segments
# =============================================================================

class AudioSegment(BaseModel):
    """Base timeline element representing a generic audio block."""
    segment_id: str = Field(..., description="Unique identifier for the segment")
    start_time: float = Field(..., ge=0.0, description="Start time on the main timeline in seconds")
    end_time: float = Field(..., ge=0.0, description="End time on the main timeline in seconds")
    file_path: Optional[str] = Field(default=None, description="Local path to audio source file")
    volume_db: float = Field(default=0.0, ge=-60.0, le=12.0, description="Gain adjustment in dB")
    fade_in: float = Field(default=0.0, ge=0.0, description="Fade-in duration in seconds")
    fade_out: float = Field(default=0.0, ge=0.0, description="Fade-out duration in seconds")

    @validator("end_time")
    def end_time_must_be_after_start(cls, v: float, values: Dict[str, Any]) -> float:
        if "start_time" in values and v <= values["start_time"]:
            raise ValueError("end_time must be strictly greater than start_time")
        return v


class MusicSegment(AudioSegment):
    """Timeline audio block tailored for background score/music stems."""
    prompt_used: Optional[str] = Field(default=None, description="Generation prompt used for this segment")
    bpm: Optional[int] = Field(default=None, ge=30, le=300, description="BPM of the audio segment")
    key: Optional[str] = Field(default=None, description="Musical key signature (e.g., C minor)")
    ducking_enabled: bool = Field(default=True, description="Enable sidechain ducking under narration")


class VoiceSegment(AudioSegment):
    """Timeline audio block tailored for voiceover or narration dialogue."""
    speaker_id: str = Field(default="Narrator", description="Identifier for speaker/voice model")
    transcript: str = Field(..., description="Speech transcript text for the segment")
    language: str = Field(default="en", description="ISO language code of narration")


class MusicTrack(BaseModel):
    """Composition track containing layered audio segments."""
    track_id: str = Field(..., description="Unique identifier for the track")
    name: str = Field(default="Audio Track", description="Display name for the track")
    segments: List[MusicSegment] = Field(default_factory=list, description="Ordered segments in track")
    is_muted: bool = Field(default=False, description="Mute state toggle")
    is_solo: bool = Field(default=False, description="Solo state toggle")
    master_gain_db: float = Field(default=0.0, ge=-60.0, le=12.0, description="Track-level master gain in dB")


# =============================================================================
# 4. Scene Detection & Timeline Schemas
# =============================================================================

class SceneRaw(BaseModel):
    """Raw scene metadata extracted during video visual parsing."""
    scene_id: int = Field(..., ge=0, description="Sequential index of detected scene")
    start_time: float = Field(..., ge=0.0, description="Scene start timestamp in seconds")
    end_time: float = Field(..., ge=0.0, description="Scene end timestamp in seconds")
    description: str = Field(default="", description="Visual description of scene content")
    intensity_score: float = Field(default=0.5, ge=0.0, le=1.0, description="Mood/intensity score (0.0 to 1.0)")
    dominant_mood: Optional[str] = Field(default="Neutral", description="Primary mood tag for scene")

    @validator("end_time")
    def end_time_must_be_after_start(cls, v: float, values: Dict[str, Any]) -> float:
        if "start_time" in values and v <= values["start_time"]:
            raise ValueError("end_time must be strictly greater than start_time")
        return v


class SceneAnalysis(BaseModel):
    """Detailed cognitive analysis of an individual video scene."""
    scene: SceneRaw = Field(..., description="Underlying raw scene bounds")
    tags: List[str] = Field(default_factory=list, description="Descriptive semantic tags")
    recommended_genre: str = Field(default="Ambient", description="Suggested musical genre")
    key_objects: List[str] = Field(default_factory=list, description="Detected visual elements/objects")
    suggested_prompt: str = Field(default="", description="Auto-generated music synthesis prompt")


class SceneAnalysisOutput(BaseModel):
    """Aggregated output from video scene detection modules."""
    video_path: str = Field(..., description="Path to analyzed video file")
    total_scenes: int = Field(..., ge=0, description="Total count of identified scenes")
    duration: float = Field(..., ge=0.0, description="Total video duration in seconds")
    scenes: List[SceneRaw] = Field(default_factory=list, description="Parsed scene records")


class SceneTimeline(BaseModel):
    """Arrangement of scene timing blocks along a project master clock."""
    total_duration: float = Field(..., ge=0.0, description="Total timeline duration in seconds")
    scenes: List[SceneRaw] = Field(default_factory=list, description="Sequential scene boundaries")
    markers: Dict[str, float] = Field(default_factory=dict, description="Named cue points and timestamps")


# =============================================================================
# 5. Script & Documentary Schemas
# =============================================================================

class ScriptScene(BaseModel):
    """Scene definition derived from written script analysis."""
    scene_number: int = Field(..., ge=1, description="Script scene number")
    heading: str = Field(..., description="Scene heading (e.g., INT. STUDIO - DAY)")
    action_description: str = Field(..., description="Visual action narrative")
    dialogue_lines: List[Dict[str, str]] = Field(default_factory=list, description="Character dialogue mappings")
    estimated_duration: float = Field(default=10.0, ge=1.0, description="Estimated scene duration in seconds")
    suggested_audio_mood: Optional[str] = Field(default="Dramatic", description="Target audio atmosphere")


class ScriptAnalysis(BaseModel):
    """Complete parsed output from screenplays or script files."""
    title: str = Field(default="Untitled Script", description="Project script title")
    total_scenes: int = Field(..., ge=0, description="Count of parsed script scenes")
    estimated_runtime: float = Field(..., ge=0.0, description="Calculated total runtime in seconds")
    scenes: List[ScriptScene] = Field(default_factory=list, description="Parsed script scene models")
    themes: List[str] = Field(default_factory=list, description="Key story themes identified")


class DocumentaryAnalysis(BaseModel):
    """Specialized structural analysis for documentary video projects."""
    project_title: str = Field(..., description="Documentary title")
    narrative_arcs: List[str] = Field(default_factory=list, description="Identified story arc phases")
    interview_segments: List[VoiceSegment] = Field(default_factory=list, description="Extracted interview cuts")
    b_roll_scenes: List[SceneRaw] = Field(default_factory=list, description="B-Roll background footage scenes")
    overall_pacing: str = Field(default="Moderate", description="Pacing profile (Slow, Moderate, Fast)")


# =============================================================================
# 6. Global Settings & Metadata
# =============================================================================

class ExportSettings(BaseModel):
    """Configuration options governing project rendering and file exports."""
    export_format: ExportFormat = Field(default=ExportFormat.WAV, description="Audio container file format")
    mastering_preset: MasteringPreset = Field(default=MasteringPreset.STREAMING, description="Target mastering profile")
    export_directory: str = Field(default="./exports", description="Destination directory for output files")
    normalize_audio: bool = Field(default=True, description="Apply integrated loudness normalization")
    include_stems: bool = Field(default=False, description="Export individual unmixed stems")


class GenerationSettings(BaseModel):
    """Global configuration governing AI synthesis models and backend selection."""
    provider: str = Field(default="musicgen", description="AI audio synthesis engine provider")
    model_name: str = Field(default="facebook/musicgen-medium", description="Specific model checkpoint name")
    use_gpu: bool = Field(default=True, description="Enable GPU hardware acceleration")
    max_memory_gb: float = Field(default=8.0, ge=1.0, description="VRAM threshold for model memory allocation")


class TimelineSettings(BaseModel):
    """System configuration for multi-track timeline processing."""
    bpm: int = Field(default=120, ge=30, le=300, description="Project master tempo in BPM")
    time_signature: str = Field(default="4/4", description="Master time signature string")
    snap_to_grid: bool = Field(default=True, description="Enforce timeline grid snapping")
    grid_resolution: str = Field(default="1/16", description="Grid division (e.g., 1/4, 1/8, 1/16)")


class VideoMetadata(BaseModel):
    """Technical metadata describing an ingested video file."""
    file_path: str = Field(..., description="Absolute path to source video file")
    resolution: str = Field(default="1920x1080", description="Video dimensions (Width x Height)")
    frame_rate: float = Field(default=29.97, ge=1.0, le=240.0, description="Video frame rate in FPS")
    duration: float = Field(..., ge=0.0, description="Total video runtime in seconds")
    has_audio: bool = Field(default=True, description="Whether original audio track exists")


class ProjectMetadata(BaseModel):
    """High-level metadata tracking project history and provenance."""
    project_id: str = Field(..., description="Unique identifier for the studio project")
    name: str = Field(..., description="Human-readable project name")
    author: str = Field(default="MystoriumX User", description="Project creator name")
    created_at: str = Field(..., description="ISO 8601 timestamp of creation")
    updated_at: str = Field(..., description="ISO 8601 timestamp of last edit")
    version: str = Field(default="1.0.0", description="Schema/project version tag")


class AIProject(BaseModel):
    """Root container representing a full MystoriumX AI Studio workspace."""
    metadata: ProjectMetadata = Field(..., description="Project identity and metadata")
    video_info: Optional[VideoMetadata] = Field(default=None, description="Ingested video file specifications")
    timeline: SceneTimeline = Field(..., description="Master timeline and scene arrangement")
    tracks: List[MusicTrack] = Field(default_factory=list, description="Audio tracks and layers")
    generation_settings: GenerationSettings = Field(default_factory=GenerationSettings)
    export_settings: ExportSettings = Field(default_factory=ExportSettings)


# =============================================================================
# 7. Reports & Generation Results
# =============================================================================

class GenerationExportResult(BaseModel):
    """Complete metadata record for rendered scene audio exports."""
    scene_number: int = Field(..., ge=0, description="Index of rendered scene")
    provider_used: str = Field(..., description="Synthesis backend provider name")
    prompt_used: str = Field(..., description="Exact prompt passed to synthesis model")
    wav_path: str = Field(..., description="Path to uncompressed WAV render")
    mp3_path: str = Field(..., description="Path to compressed MP3 render")
    waveform_png_path: str = Field(..., description="Path to visual waveform preview image")
    metadata_json_path: str = Field(..., description="Path to exported sidecar metadata JSON")
    actual_duration_sec: float = Field(..., ge=0.0, description="Duration of rendered clip in seconds")
    sample_rate_hz: int = Field(default=48000, ge=8000, description="Sample rate of rendered asset")
    bit_depth: int = Field(default=24, ge=16, description="Bit depth of rendered asset")
    channels: int = Field(default=2, ge=1, description="Number of channels in rendered asset")
    peak_db: float = Field(..., description="Peak amplitude in dB")
    integrated_lufs: float = Field(..., description="Measured integrated loudness in LUFS")
    generation_time_sec: float = Field(..., ge=0.0, description="Wall-clock time taken for synthesis in seconds")


class StudioScriptReport(BaseModel):
    """Consolidated orchestration report for full soundtrack mastering runs."""
    project_name: str = Field(..., description="Name of the studio project")
    total_duration: float = Field(..., ge=0.0, description="Total runtime of processed soundtrack in seconds")
    detected_scenes: List[SceneRaw] = Field(default_factory=list, description="List of analyzed video scenes")
    generation_parameters: MusicGenerationParams = Field(..., description="Parameters used during generation")
    export_paths: Dict[str, str] = Field(default_factory=dict, description="Map of exported file formats to paths")
    mastering_status: str = Field(default="SUCCESS", description="Execution status code")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional telemetric metadata")
