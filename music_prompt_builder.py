"""
Music Prompt Builder & Optimization Engine Module.
Formulates, builds, and optimizes AI music prompts.
"""

import re
from typing import List, Dict, Any
from models.schemas import AudioTechnicalSettings
from prompts.network_templates import NETWORK_PRESETS, PROMPT_TEMPLATE_REPOSITORY
from utils import setup_logger

logger = setup_logger("MusicPromptBuilder")


class PromptOptimizationEngine:
    """Analyzes raw prompt strings, detects weaknesses, and applies automated enhancements."""

    WEAK_PATTERNS = {
        r"\b(nice|good|bad|cool|music|song)\b": "cinematic score",
        r"\b(scary)\b": "chilling psychological tension",
        r"\b(fast)\b": "rapid spiccato rhythm",
        r"\b(slow)\b": "spacious atmospheric tempo",
        r"\b(sad)\b": "profound tragic mournfulness"
    }

    QUALITY_BUFFERS = [
        "instrumental only",
        "mastered for broadcast",
        "pristine dynamic range",
        "no vocal noise",
        "48kHz ultra-detailed audio"
    ]

    def optimize_prompt(self, raw_prompt: str) -> str:
        """Transforms basic or weak prompt descriptions into rich cinematic prompts."""
        optimized = raw_prompt

        # Replace weak generic vocabulary
        for weak_regex, strong_replacement in self.WEAK_PATTERNS.items():
            optimized = re.sub(weak_regex, strong_replacement, optimized, flags=re.IGNORECASE)

        # Ensure quality control suffixes are present
        missing_buffers = [buf for buf in self.QUALITY_BUFFERS if buf not in optimized.lower()]
        if missing_buffers:
            optimized += ", " + ", ".join(missing_buffers[:2]) + "."

        # Remove redundant whitespace
        optimized = re.sub(r"\s+", " ", optimized).strip()
        logger.debug("Prompt optimization complete.")
        return optimized


class MusicPromptBuilder:
    """Builds robust AI music generation prompts using templates and optimization engines."""

    def __init__(self):
        self.optimizer = PromptOptimizationEngine()

    def build_prompt(
        self,
        scene_num: int,
        style: str,
        mood: str,
        tempo: int,
        key: str,
        instruments: List[str],
        buildup: str,
        ending: str,
        network: str = "Netflix Documentary"
    ) -> str:
        """Constructs and optimizes a complete prompt for generative music models."""
        network_preset = NETWORK_PRESETS.get(network, NETWORK_PRESETS["Netflix Documentary"])
        inst_str = ", ".join(instruments)

        raw_prompt = (
            f"{style} score for scene {scene_num}. {mood} cinematic atmosphere with {inst_str}. "
            f"Tempo of {tempo} BPM in {key}. {buildup}. Ending: {ending}. {network_preset}."
        )

        # Run through Prompt Optimization Engine
        final_prompt = self.optimizer.optimize_prompt(raw_prompt)
        return final_prompt
