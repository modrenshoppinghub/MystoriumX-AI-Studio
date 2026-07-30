"""
Automated unit tests for MystoriumX AI Studio core pipeline components.
"""

import pytest
from pathlib import Path
from scene_detector import SceneDetector
from emotion_engine import EmotionEngine
from music_planner import MusicPlanner
from models.schemas import SceneRaw

def test_scene_detection():
    detector = SceneDetector()
    script = "SCENE 1\nINT. LAB\nDark space.\n\nSCENE 2\nEXT. MOUNTAIN\nVast views."
    scenes = detector.parse_scenes(script)
    assert len(scenes) == 2
    assert scenes[0].scene_number == 1
    assert scenes[1].scene_number == 2

def test_emotion_engine():
    engine = EmotionEngine()
    scene = SceneRaw(scene_number=1, raw_text="A dark shadow crept quietly in the mystery of the abyss.", word_count=10)
    analysis = engine.analyze_scene(scene)
    assert analysis.primary_emotion == "suspense"
    assert analysis.suspense_level > 0.0

def test_music_planner():
    planner = MusicPlanner()
    engine = EmotionEngine()
    scene = SceneRaw(scene_number=1, raw_text="Ancient glorious cosmos filled with vast wonder.", word_count=7)
    emotion = engine.analyze_scene(scene)
    plan = planner.create_plan(emotion)
    assert len(plan.recommended_instruments) > 0
    assert 40 <= plan.tempo_bpm <= 220
