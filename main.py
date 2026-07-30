"""
Main Entry Point - Executes full MystoriumX AI Studio Pipeline (Phases 1, 2, and 3).
"""

import sys
from pathlib import Path
from script_analyzer import ScriptAnalyzer
from music_engine import AIMusicEngine
from generation_orchestrator import GenerationOrchestrator
from models.schemas import MusicGenerationParams
from utils import setup_logger

logger = setup_logger("MainStudioPipeline")


def create_sample_script(target_path: Path):
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
    print("   MystoriumX AI Studio - End-to-End AI Production Engine        ")
    print("==================================================================")

    sample_file = Path("sample_documentary.txt")
    if not sample_file.exists():
        create_sample_script(sample_file)

    try:
        # Phase 1: Script Analysis
        logger.info("Executing Phase 1: Script Analysis...")
        script_analyzer = ScriptAnalyzer()
        phase1_report = script_analyzer.analyze_script(sample_file, project_title="Cosmic Secrets")

        # Phase 2: Music Plan & Prompt Optimization
        logger.info("Executing Phase 2: AI Music Directive Planning...")
        music_engine = AIMusicEngine(default_network_preset="BBC Documentary")
        phase2_report = music_engine.generate_phase2_report(phase1_report)

        # Phase 3: AI Synthesis & Master Audio Generation
        logger.info("Executing Phase 3: AI Audio Generation & Mastering Engine...")
        orchestrator = GenerationOrchestrator(output_dir=Path("output"))
        
        gen_params = MusicGenerationParams(
            duration_sec=10.0,  # Rapid generation test
            sample_rate_hz=48000,
            stereo=True
        )
        
        results = orchestrator.execute_phase3_pipeline(phase2_report, default_params=gen_params)

        print("\n==================================================================")
        print(f" SUCCESS: Successfully generated and mastered {len(results)} scenes.")
        for r in results:
            print(f" Scene {r.scene_number} | Provider: {r.provider_used} | Output: {r.wav_path}")
        print("==================================================================")

    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
