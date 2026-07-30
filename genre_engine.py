"""
Genre Engine Module - Maps document classifications to high-level musical genres.
"""

from typing import Dict
from utils import setup_logger

logger = setup_logger("GenreEngine")


class GenreEngine:
    """Handles mapping between scene contexts and master music genres."""

    GENRE_MAP: Dict[str, str] = {
        "Historical Documentary": "Cinematic Neoclassical Orchestral",
        "Mystery": "Dark Ambient Drone & Electroacoustic",
        "Investigation": "Micro-Textural Modern Minimalist",
        "Psychological Horror": "Avant-Garde Dissonant Soundscape",
        "Ancient Egypt": "Ethno-Cinematic Primitive Folk",
        "Ancient Rome": "Epic Orchestral & Ancient Percussion",
        "Space Documentary": "Cosmic Synth Wave & Ambient Drone",
        "War Documentary": "Heavy Hybrid Orchestral & Brass",
        "Fantasy": "Symphonic Orchestral Fantasy",
        "Adventure": "Orchestral Action & World Percussion",
        "Emotional": "Minimalist Piano & Chamber Strings",
        "Epic Trailer": "Hybrid Orchestral Sound Design"
    }

    def resolve_genre(self, style: str) -> str:
        """Translates a documentary style into a master musical genre."""
        genre = self.GENRE_MAP.get(style, "Cinematic Ambient Modern")
        logger.debug(f"Resolved style '{style}' -> Genre '{genre}'")
        return genre
