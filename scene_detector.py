"""
Scene Detector Module - Segments script into logically structured scenes.
"""

import re
from typing import List
from models.schemas import SceneRaw
from utils import setup_logger

logger = setup_logger("SceneDetector")

class SceneDetector:
    """Analyzes raw script text and parses it into distinct cinematic scenes."""
    
    SCENE_MARKERS = [
        r"SCENE\s+\d+",
        r"INT\.",
        r"EXT\.",
        r"ACT\s+[I|V|X|\d]+",
        r"\[SCENE\s+\d+\]"
    ]

    def parse_scenes(self, script_text: str) -> List[SceneRaw]:
        """Splits raw text based on scene headers or block-level heuristics."""
        logger.info("Initiating scene detection...")
        pattern = "|".join(self.SCENE_MARKERS)
        split_positions = [m.start() for m in re.finditer(pattern, script_text, re.IGNORECASE)]
        
        scenes: List[SceneRaw] = []
        
        if split_positions:
            for i in range(len(split_positions)):
                start = split_positions[i]
                end = split_positions[i + 1] if i + 1 < len(split_positions) else len(script_text)
                content = script_text[start:end].strip()
                words = len(content.split())
                if words > 0:
                    scenes.append(SceneRaw(scene_number=len(scenes) + 1, raw_text=content, word_count=words))
        else:
            # Fallback: Split by double newlines into paragraphs if no explicit scene tags exist
            logger.warning("No standard script headers detected. Falling back to paragraph block segmentation.")
            blocks = [b.strip() for b in script_text.split("\n\n") if b.strip()]
            for block in blocks:
                words = len(block.split())
                scenes.append(SceneRaw(scene_number=len(scenes) + 1, raw_text=block, word_count=words))

        logger.info(f"Detected {len(scenes)} distinct scenes.")
        return scenes
