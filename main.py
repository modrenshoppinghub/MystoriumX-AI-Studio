"""
Main Execution Script for MystoriumX AI Studio.
"""

import sys
from pathlib import Path
from script_analyzer import ScriptAnalyzer
from utils import setup_logger

logger = setup_logger("Main")

def create_sample_script(target_path: Path):
    """Generates a sample script for demonstration if none exists."""
    sample_content = """SCENE 1
INT. DEEP SPACE RESEARCH LAB - NIGHT
The endless darkness of the cosmic abyss stretches out beyond the glass. Silence heavy as lead fills the station. Dr. Aris stares into the dark monitor, watching a shadow move across the stars. Danger approaches unseen.

SCENE 2
EXT. ANCIENT PYRAMID RUINS - DAY
Glorious rays of sunlight break through the ancient clouds, illuminating the magnificent golden apex. The vast architecture speaks of ancient cosmic secrets unlocked after thousands of years.

SCENE 3
INT. EXCAVATION TUNNEL - NIGHT
Tears fall in the cold mud. The artifact lies shattered—a tragedy of lost history. Centuries of human effort collapsed into dust in a single swift second.
"""
    target_path.write_text(sample_content, encoding="utf-8")

def main():
    print("==================================================")
    print("      MystoriumX AI Studio - Phase 1 Engine       ")
    print("==================================================")

    sample_file = Path("sample_documentary.txt")
    if not sample_file.exists():
        logger.info("Generating sample script file for execution test...")
        create_sample_script(sample_file)

    analyzer = ScriptAnalyzer()
    try:
        report = analyzer.analyze_script(sample_file, project_title="Deep Space & Lost Empires")
        
        # Serialize report to JSON
        json_output = report.model_dump_json(indent=2)
        
        print("\n--- GENERATED MUSIC GENERATION PLAN (JSON) ---")
        print(json_output)
        
        # Write report to disk
        out_path = Path("studio_music_plan.json")
        out_path.write_text(json_output, encoding="utf-8")
        logger.info(f"Saved complete music plan to {out_path.resolve()}")
        
    except Exception as e:
        logger.error(f"Execution failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
