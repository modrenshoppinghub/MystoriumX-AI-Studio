"""
Script Analyzer Orchestrator - Main entry pipeline for MystoriumX AI Studio.
"""

import json
from pathlib import Path
from typing import List, Union

from config import DEFAULT_WORDS_PER_MINUTE, MIN_SCENE_DURATION_SEC
from models.schemas import SceneAnalysisOutput, StudioScriptReport
from utils import DocumentLoader, setup_logger
from scene_detector import SceneDetector
from emotion_engine import EmotionEngine
from music_planner import MusicPlanner

logger = setup_logger("ScriptAnalyzer")

class ScriptAnalyzer:
    """High-level Orchestrator binding loader, detector, emotion engine, and planner."""

    def __init__(self, words_per_minute: float = DEFAULT_WORDS_PER_MINUTE):
        self.wpm = words_per_minute
        self.scene_detector = SceneDetector()
        self.emotion_engine = EmotionEngine()
        self.music_planner = MusicPlanner()

    def analyze_script(self, file_path: Union[str, Path], project_title: str = "Documentary Project") -> StudioScriptReport:
        """Executes full analysis pipeline on a given script file."""
        logger.info(f"Processing script: {file_path}")
        raw_text = DocumentLoader.load_document(Path(file_path))
        raw_scenes = self.scene_detector.parse_scenes(raw_text)

        analyzed_scenes: List[SceneAnalysisOutput] = []
        total_duration = 0.0

        for scene in raw_scenes:
            # Calculate Duration
            estimated_duration = max(
                MIN_SCENE_DURATION_SEC,
                round((scene.word_count / self.wpm) * 60.0, 2)
            )
            total_duration += estimated_duration

            # Pipeline execution
            emotion_res = self.emotion_engine.analyze_scene(scene)
            music_res = self.music_planner.create_plan(emotion_res)

            excerpt = scene.raw_text[:120] + "..." if len(scene.raw_text) > 120 else scene.raw_text

            analyzed_scenes.append(
                SceneAnalysisOutput(
                    scene_number=scene.scene_number,
                    duration_estimate_sec=estimated_duration,
                    text_excerpt=excerpt,
                    emotion=emotion_res,
                    music_plan=music_res
                )
            )

        report = StudioScriptReport(
            title=project_title,
            total_scenes=len(analyzed_scenes),
            total_estimated_duration_sec=round(total_duration, 2),
            scenes=analyzed_scenes
        )
        logger.info("Script processing complete.")
        return report
