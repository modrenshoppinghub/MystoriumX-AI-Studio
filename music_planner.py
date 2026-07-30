"""
Music Planner Module - Formulates score direction, tempo, and instrumentation choices.
"""

import random
from models.schemas import EmotionAnalysis, MusicPlan
from prompts.script_prompts import MUSIC_STYLE_MAP
from utils import setup_logger

logger = setup_logger("MusicPlanner")

class MusicPlanner:
    """Maps emotional analysis to concrete musical scoring blueprints."""

    def create_plan(self, emotion_data: EmotionAnalysis) -> MusicPlan:
        emotion = emotion_data.primary_emotion
        style_info = MUSIC_STYLE_MAP.get(emotion, MUSIC_STYLE_MAP["curiosity"])
        
        style_name, (bpm_min, bpm_max), instruments = style_info
        
        # Adjust BPM dynamically using Energy Level
        bpm_range = bpm_max - bpm_min
        dynamic_bpm = int(bpm_min + (bpm_range * emotion_data.energy_level))
        
        return MusicPlan(
            music_style=style_name,
            tempo_bpm=dynamic_bpm,
            recommended_instruments=instruments
        )
