"""
MystoriumX AI Studio - Configuration Module
"""

from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
LOGS_DIR = BASE_DIR / "logs"
PROMPTS_DIR = BASE_DIR / "prompts"

# Ensure directories exist
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Default Processing Parameters
DEFAULT_WORDS_PER_MINUTE = 130.0  # Standard narrator pace for documentaries
MIN_SCENE_DURATION_SEC = 5.0

# Logging Config
LOG_FILE_PATH = LOGS_DIR / "mystorium_x.log"
LOG_FORMAT = "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
