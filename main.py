"""
MystoriumX AI Studio - Unified Main CLI Entry Point
Provides a production-grade interface to run complete end-to-end audio processing pipelines.
"""

import argparse
import sys
import os
import json
import logging
import torch

from audio_processor import BaseAudioProcessor
from mastering_engine import MasteringEngine
from export_engine import ExportEngine
from waveform_generator import WaveformGenerator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("MystoriumX.CLI")


def run_pipeline(args: argparse.Namespace) -> int:
    """Executes the complete MystoriumX audio mastering and output pipeline."""
    try:
        logger.info(f"Initializing MystoriumX AI Studio Engine (Sample Rate: {args.sample_rate}Hz)...")
        
        device_str = "CUDA GPU" if torch.cuda.is_available() and not args.no_gpu else "CPU"
        logger.info(f"Execution Target Context: {device_str}")

        mastering_sys = MasteringEngine(sample_rate=args.sample_rate, prefer_gpu=not args.no_gpu)

        # 1. Load Audio Inputs
        if not os.path.exists(args.input_music):
            raise FileNotFoundError(f"Input music file not found: {args.input_music}")
        
        logger.info(f"Loading music asset: {args.input_music}")
        music_buf = mastering_sys.base_proc.load_audio(args.input_music)

        narration_buf = None
        if args.input_narration:
            if not os.path.exists(args.input_narration):
                raise FileNotFoundError(f"Input narration file not found: {args.input_narration}")
            logger.info(f"Loading narration asset: {args.input_narration}")
            narration_buf = mastering_sys.base_proc.load_audio(args.input_narration)

        # 2. Process Mastering
        logger.info(f"Executing Mastering Pipeline (Target LUFS: {args.lufs}, Ceiling: {args.ceiling}dB)...")
        mastered_buf = mastering_sys.master_soundtrack(
            music_buffer=music_buf,
            narration_buffer=narration_buf,
            target_lufs=args.lufs,
            ceiling_db=args.ceiling
        )

        # 3. Export Formats
        os.makedirs(args.output_dir, exist_ok=True)
        exporter = ExportEngine(sample_rate=args.sample_rate)
        logger.info(f"Exporting broadcast audio packages to: {args.output_dir}")
        export_results = exporter.export_all(
            audio=mastered_buf.data,
            output_dir=args.output_dir,
            base_filename=args.base_name
        )

        # 4. Render Waveform and Diagnostic Plots
        waveform_path = os.path.join(args.output_dir, "waveform.png")
        logger.info(f"Rendering visual analytics to: {waveform_path}")
        wf_gen = WaveformGenerator()
        wf_gen.generate_all_plots(mastered_buf.data, args.sample_rate, waveform_path)
        export_results["waveform"] = waveform_path

        logger.info("Pipeline Execution Completed Successfully.")
        print(json.dumps(export_results, indent=2))
        return 0

    except Exception as e:
        logger.error(f"Fatal Pipeline Error: {e}", exc_info=True)
        return 1


def build_parser() -> argparse.ArgumentParser:
    """Constructs command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="MystoriumX AI Studio v1.0 - Cinematic Audio Mastering Engine"
    )
    parser.add_argument("--input-music", "-m", required=True, help="Path to raw background music file")
    parser.add_argument("--input-narration", "-n", default=None, help="Path to narration track for auto-ducking")
    parser.add_argument("--output-dir", "-o", default="./output", help="Directory to save output files")
    parser.add_argument("--base-name", "-b", default="music", help="Base filename for exported assets")
    parser.add_argument("--sample-rate", "-sr", type=int, default=48000, choices=[44100, 48000], help="Audio sample rate")
    parser.add_argument("--lufs", type=float, default=-14.0, help="Target integrated loudness in LUFS")
    parser.add_argument("--ceiling", type=float, default=-1.0, help="Peak limiter ceiling in dB")
    parser.add_argument("--no-gpu", action="store_true", help="Force CPU processing mode")
    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    sys.exit(run_pipeline(args))
