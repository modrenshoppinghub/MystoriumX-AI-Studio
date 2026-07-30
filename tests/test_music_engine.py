"""
Automated unit tests for Phase 2 AI Music Engine components.
"""

import pytest
from music_engine import AIMusicEngine
from music_prompt_builder import PromptOptimizationEngine, MusicPromptBuilder
from style_engine import StyleEngine
from tempo_engine import TempoEngine
from models.schemas import SceneAnalysisOutput, EmotionAnalysis, MusicPlan


def test_style_validation():
    engine = StyleEngine()
    assert engine.validate_or_fall_back("Space Documentary") == "Space Documentary"
    assert engine.validate_or_fall_back("Unknown Custom Style") == "Historical Documentary"


def test_tempo_and_key_determination():
    engine = TempoEngine()
    key, scale = engine.determine_tonality("Fear")
    assert "Minor" in key or "Chromatic" in key or "Phrygian" in key
    
    buildup, ending = engine.determine_structure(energy_level=0.9, suspense_level=0.8)
    assert "crescendo" in buildup.lower() or "acceleration" in buildup.lower()


def test_prompt_optimizer():
    optimizer = PromptOptimizationEngine()
    weak_prompt = "Make a scary fast music track with nice guitars"
    optimized = optimizer.optimize_prompt(weak_prompt)
    assert "chilling psychological tension" in optimized
    assert "instrumental only" in optimized


def test_full_phase2_scene_processing():
    engine = AIMusicEngine(default_network_preset="Netflix Documentary")
    dummy_scene = SceneAnalysisOutput(
        scene_number=1,
        duration_estimate_sec=15.0,
        text_excerpt="Dark cosmic space...",
        emotion=EmotionAnalysis(primary_emotion="suspense", energy_level=0.2, suspense_level=0.85),
        music_plan=MusicPlan(music_style="Mystery", tempo_bpm=58, recommended_instruments=["Sub-bass"])
    )
    
    result = engine.process_scene(dummy_scene)
    assert result.scene == 1
    assert result.tempo == 58
    assert result.mood == "Fear"
    assert "Netflix Documentary" in result.network_preset
    assert len(result.instruments) > 0
    assert result.audio_settings.sample_rate_hz == 48000
