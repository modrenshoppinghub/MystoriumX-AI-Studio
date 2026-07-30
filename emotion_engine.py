"""
Emotion Engine Module - Analyzes emotional trajectory and psychological tension.
"""

from models.schemas import SceneRaw, EmotionAnalysis
from prompts.script_prompts import EMOTION_KEYWORDS
from utils import setup_logger

logger = setup_logger("EmotionEngine")

class EmotionEngine:
    """Extracts emotional traits, energy levels, and suspense ratings from scene text."""
    
    def analyze_scene(self, scene: SceneRaw) -> EmotionAnalysis:
        text_lower = scene.raw_text.lower()
        word_count = max(scene.word_count, 1)

        scores = {emotion: 0 for emotion in EMOTION_KEYWORDS}
        for emotion, keywords in EMOTION_KEYWORDS.items():
            for kw in keywords:
                scores[emotion] += text_lower.count(kw)

        # Determine Primary Emotion
        primary_emotion = max(scores, key=scores.get)
        if scores[primary_emotion] == 0:
            primary_emotion = "curiosity"  # Default fallback for documentary narrative

        # Compute normalized Energy and Suspense
        suspense_count = scores["suspense"]
        action_count = scores["action"]
        
        energy_level = min(1.0, round((action_count * 2.5 + scores["awe"] * 1.5 + 1.0) / (word_count * 0.1 + 2), 2))
        suspense_level = min(1.0, round((suspense_count * 3.0 + 0.5) / (word_count * 0.1 + 2), 2))

        logger.debug(f"Scene {scene.scene_number} analyzed: {primary_emotion} (Energy: {energy_level}, Suspense: {suspense_level})")
        
        return EmotionAnalysis(
            primary_emotion=primary_emotion,
            energy_level=energy_level,
            suspense_level=suspense_level
        )
