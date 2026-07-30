"""
Style Engine Module - Resolves stylistic framing and supported documentary aesthetics.
"""

from typing import List
from utils import setup_logger

logger = setup_logger("StyleEngine")


class StyleEngine:
    """Determines exact documentary style framing and supported style definitions."""

    SUPPORTED_STYLES: List[str] = [
        "Historical Documentary",
        "Mystery",
        "Investigation",
        "Psychological Horror",
        "Ancient Egypt",
        "Ancient Rome",
        "Space Documentary",
        "War Documentary",
        "Fantasy",
        "Adventure",
        "Emotional",
        "Epic Trailer"
    ]

    def validate_or_fall_back(self, raw_style: str) -> str:
        """Validates input style against supported domains or selects closest aesthetic match."""
        for supported in self.SUPPORTED_STYLES:
            if supported.lower() in raw_style.lower():
                return supported

        logger.warning(f"Unrecognized style '{raw_style}'. Falling back to 'Historical Documentary'.")
        return "Historical Documentary"
