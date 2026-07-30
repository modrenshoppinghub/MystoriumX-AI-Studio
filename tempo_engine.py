"""
Tempo Engine Module - Determines exact BPM, key signature, scale, and musical structure.
"""

import random
from typing import Tuple
from utils import setup_logger

logger = setup_logger("TempoEngine")


class TempoEngine:
    """Calculates musical keys, scales, tempo adjustments, and structural progression."""

    KEY_SCALE_MAP = {
        "Dark": ["D Minor", "C Minor", "F# Minor", "Phrygian Dominant"],
        "Cold": ["A Minor", "E Minor", "B Locrian", "C Natural Minor"],
        "Fear": ["D# Minor", "C# Minor", "D Phrygian", "Dissonant Chromatic"],
        "Mystery": ["G Minor", "F Minor", "D Dorian", "Harmonic Minor"],
        "Hope": ["D Major", "G Major", "A Major", "Lydian Mode"],
        "Adventure": ["C Major", "E Minor", "D Mixolydian", "A Minor"],
        "Isolation": ["B Minor", "F# Minor", "A Pentatonic Minor"],
        "Frozen": ["A Minor", "D Minor", "Aeolian Mode"],
        "Ancient": ["D Dorian", "E Phrygian", "Phrygian Dominant", "A Aeolian"],
        "Epic": ["D Minor", "C Minor", "E Minor", "Bb Major"],
        "Investigation": ["A Minor", "E Minor", "G Minor", "D Mixolydian"],
        "Tragic": ["C Minor", "F Minor", "G Minor", "B Minor"]
    }

    def determine_tonality(self, mood: str) -> Tuple[str, str]:
        """Selects appropriate key signature and scale based on mood context."""
        options = self.KEY_SCALE_MAP.get(mood, ["D Minor", "A Minor", "C Minor"])
        selected_key = options[0]  # Deterministic primary choice
        scale = "Minor" if "Minor" in selected_key else ("Major" if "Major" in selected_key else "Modal")
        logger.debug(f"Determined key '{selected_key}' (Scale: {scale}) for mood '{mood}'")
        return selected_key, scale

    def determine_structure(self, energy_level: float, suspense_level: float) -> Tuple[str, str]:
        """Calculates dynamic build-up structure and scene ending style."""
        if suspense_level > 0.7:
            buildup = "Slow exponential crescendo with rising ostinato"
            ending = "Sudden abrupt cut on high-tension dissonance"
        elif energy_level > 0.7:
            buildup = "Driving rhythmic acceleration with full orchestral swelling"
            ending = "Massive ringing brass impact with long reverb tail"
        elif energy_level < 0.3:
            buildup = "Static atmospheric drift with subtle textural modulation"
            ending = "Fading quiet sub-bass decay into complete silence"
        else:
            buildup = "Linear thematic expansion with layered counter-melodies"
            ending = "Sustained resolution chord fading slowly"

        return buildup, ending
