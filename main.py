"""
Main Execution Script for MystoriumX AI Studio (Phase 1 + Phase 2 Pipeline).
"""

import sys
from pathlib import Path
from script_analyzer import ScriptAnalyzer
from music_engine import AIMusicEngine
from utils import setup_logger

logger = setup_logger("MainPipeline")


def create_sample_script(target_path: Path):
    """Generates a sample documentary script for execution test."""
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
    print("==================================================================")
    print("      MystoriumX AI Studio - Full Phase 1 & 2 AI Engine           ")
    print("==================================================================")

    sample_file = Path("sample_documentary.txt")
    if not sample_file.exists():
        logger.info("Generating sample script file for execution test...")
        create_sample_script(sample_file)

    # Instantiate Phase 1 and Phase 2 Engines
    script_analyzer = ScriptAnalyzer()
    ai_music_engine = AIMusicEngine(default_network_preset="BBC Documentary")

    try:
        # Phase 1 Execution
        logger.info("Executing Phase 1: Script Analysis & Scene Detection...")
        phase1_report = script_analyzer.analyze_script(sample_file, project_title="Cosmic & Ancient Secrets")

        # Phase 2 Execution
        logger.info("Executing Phase 2: AI Music Engine Directive Planning...")
        phase2_report = ai_music_engine.generate_phase2_report(phase1_report)

        # Output Results
        json_output = phase2_report.model_dump_json(indent=2)
        print("\n--- PHASE 2: GENERATED AI MUSIC ENGINE PLAN (JSON) ---")
        print(json_output)

        # Save to file
        output_file = Path("mystorium_phase2_music_plan.json")
        output_file.write_text(json_output, encoding="utf-8")
        logger.info(f"Successfully exported Phase 2 plan to {output_file.resolve()}")

    except Exception as e:
        logger.error(f"Execution failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
