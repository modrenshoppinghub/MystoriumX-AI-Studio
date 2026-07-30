"""
Instrument Engine Module - Orchestrates acoustic instruments, synths, and sound design.
"""

from typing import List, Dict
from utils import setup_logger

logger = setup_logger("InstrumentEngine")


class InstrumentEngine:
    """Provides orchestrations tailored to specific moods, styles, and atmospheres."""

    ATMOSPHERE_INSTRUMENT_MAP: Dict[str, List[str]] = {
        "Dark": ["Deep Sub-Bass Drones", "Dark Low Strings", "Cold Wind Ambience", "Low Brass Swells"],
        "Cold": ["Frozen Ice Texture Percussion", "Glass Harmonica", "Solo Cello", "Subtle Reverb Trails"],
        "Fear": ["Prepared Piano", "Dissonant String Cluster", "Waterphone", "Distorted Sub-Synth"],
        "Mystery": ["Pizzicato Violins", "Analog Arpeggiator", "Hollow Wooden Flute", "Sub-Bass Pulse"],
        "Hope": ["Warm Concert Grand Piano", "Full Orchestral String Swells", "French Horns", "Acoustic Guitar"],
        "Adventure": ["Spiccato Violins", "Taiko Drums", "Heroic Brass Ensemble", "Cinematic Percussion"],
        "Isolation": ["Solo Viola", "Sparse Drone Synth", "Distant Echoing Piano", "Granular Wind Ambience"],
        "Frozen": ["Crystal Chimes", "Bowd Metal Textures", "Cold Synth Pad", "Solo Low Clarinet"],
        "Ancient": ["Duduk", "Frame Drum", "Ancient Bone Flute", "Primitive Horns", "Lyre"],
        "Epic": ["Massive Orchestral Drums", "Full Brass Section", "Staccato Choir", "Hybrid Synth Bass"],
        "Investigation": ["Ticking Clockwork Percussion", "Upright Bass Pulse", "Marimba", "Muted Piano"],
        "Tragic": ["Solo Cello", "Sad String Quartet", "Soft Melancholy Piano", "Low Double Bass"]
    }

    def assemble_orchestration(self, mood: str, style: str, base_instruments: List[str]) -> List[str]:
        """Combines Phase 1 recommendations with Phase 2 palette extensions."""
        mood_palette = self.ATMOSPHERE_INSTRUMENT_MAP.get(mood, ["Orchestral Strings", "Piano", "Sub-Bass"])
        
        # Merge unique elements
        combined = list(dict.fromkeys(base_instruments + mood_palette))
        logger.debug(f"Assembled {len(combined)} instruments for mood '{mood}' and style '{style}'")
        return combined[:6]  # Top 6 optimal instrumentation choices
