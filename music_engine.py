"""
Music Engine Core Orchestrator - Main Phase 2 entry pipeline.
Translates Phase 1 analysis into production-ready AI music generation directives.
"""

from typing import List, Union, Dict, Any
from pathlib import Path

from models.schemas import (
    StudioScriptReport,
    SceneAnalysisOutput,
    AIMusicPromptOutput,
    Phase2StudioReport
)
from style_engine import StyleEngine
from genre_engine import GenreEngine
from tempo_engine import TempoEngine
from instrument_engine import InstrumentEngine
from audio_settings import AudioSettingsEngine
from music_prompt_builder import MusicPromptBuilder
from utils import setup_logger

logger = setup_logger("AIMusicEngine")


class AIMusicEngine:
    """Core Phase 2 Engine translating script analysis into optimized AI music plans."""

    SUPPORTED_MOODS: List[str] = [
        "Dark", "Cold", "Fear", "Mystery", "Hope", "Adventure",
        "Isolation", "Frozen", "Ancient", "Epic", "Investigation", "Tragic"
    ]

    def __init__(self, default_network_preset: str = "Netflix Documentary"):
        self.style_engine = StyleEngine()
        self.genre_engine = GenreEngine()
        self.tempo_engine = TempoEngine()
        self.instrument_engine = InstrumentEngine()
        self.audio_settings_engine = AudioSettingsEngine()
        self.prompt_builder = MusicPromptBuilder()
        self.default_network_preset = default_network_preset

    def map_emotion_to_mood(self, primary_emotion: str, suspense_level: float) -> str:
        """Maps Phase 1 emotional traits to supported Phase 2 mood categories."""
        emotion = primary_emotion.lower()
        if suspense_level > 0.6:
            return "Fear" if suspense_level > 0.8 else "Mystery"
        
        mapping = {
            "suspense": "Mystery",
            "awe": "Epic",
            "sorrow": "Tragic",
            "action": "Adventure",
            "curiosity": "Investigation"
        }
        return mapping.get(emotion, "Dark")

    def derive_qualitative_energy(self, energy_level: float) -> str:
        """Converts float energy to qualitative descriptor."""
        if energy_level >= 0.8:
            return "Extreme"
        elif energy_level >= 0.5:
            return "High"
        elif energy_level >= 0.3:
            return "Medium"
        else:
            return "Low"

    def process_scene(self, scene_output: SceneAnalysisOutput, network_preset: Optional[str] = None) -> AIMusicPromptOutput:
        """Generates complete AI music output for a single scene."""
        network = network_preset or self.default_network_preset
        
        # 1. Resolve Style & Genre
        style = self.style_engine.validate_or_fall_back(scene_output.music_plan.music_style)
        genre = self.genre_engine.resolve_genre(style)

        # 2. Derive Mood & Energy
        mood = self.map_emotion_to_mood(
            scene_output.emotion.primary_emotion,
            scene_output.emotion.suspense_level
        )
        qualitative_energy = self.derive_qualitative_energy(scene_output.emotion.energy_level)

        # 3. Determine Tonality & Structure
        key, scale = self.tempo_engine.determine_tonality(mood)
        buildup, ending = self.tempo_engine.determine_structure(
            scene_output.emotion.energy_level,
            scene_output.emotion.suspense_level
        )

        # 4. Assemble Orchestration
        instruments = self.instrument_engine.assemble_orchestration(
            mood=mood,
            style=style,
            base_instruments=scene_output.music_plan.recommended_instruments
        )

        # 5. Build & Optimize Prompt
        prompt = self.prompt_builder.build_prompt(
            scene_num=scene_output.scene_number,
            style=style,
            mood=mood,
            tempo=scene_output.music_plan.tempo_bpm,
            key=key,
            instruments=instruments,
            buildup=buildup,
            ending=ending,
            network=network
        )

        # 6. Technical Audio Settings
        audio_dsp = self.audio_settings_engine.derive_settings(mood, scene_output.emotion.energy_level)

        return AIMusicPromptOutput(
            scene=scene_output.scene_number,
            prompt=prompt,
            tempo=scene_output.music_plan.tempo_bpm,
            key=key,
            style=style,
            genre=genre,
            mood=mood,
            energy=qualitative_energy,
            intensity=scene_output.emotion.energy_level,
            atmosphere=f"{mood} soundscape with {scene_output.emotion.suspense_level} tension rating",
            buildup_structure=buildup,
            ending_style=ending,
            instruments=instruments,
            network_preset=network,
            audio_settings=audio_dsp
        )

    def generate_phase2_report(self, phase1_report: StudioScriptReport, network_preset: Optional[str] = None) -> Phase2StudioReport:
        """Processes entire script analysis report into Phase 2 music generation output."""
        logger.info(f"Starting Phase 2 AI Music Generation Plan for '{phase1_report.title}'...")
        prompts: List[AIMusicPromptOutput] = []

        for scene in phase1_report.scenes:
            prompts.append(self.process_scene(scene, network_preset=network_preset))

        logger.info(f"Phase 2 processing complete. Generated {len(prompts)} music directives.")
        return Phase2StudioReport(
            project_title=phase1_report.title,
            total_scenes_processed=len(prompts),
            prompts=prompts
        )
