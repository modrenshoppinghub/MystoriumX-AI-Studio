"""
Phase 3 Master Generation Orchestrator.
Coordinates backends, DSP post-processing, export formats, and metadata logging.
"""

import json
import time
import wave
import numpy as np
from pathlib import Path
from typing import List

from models.schemas import (
    Phase2StudioReport,
    AIMusicPromptOutput,
    MusicGenerationParams,
    GenerationExportResult
)
from providers.provider_manager import ProviderManager
from audio_post_processor import AudioPostProcessor
from waveform_generator import WaveformVisualizer
from utils import setup_logger, HardwareDeviceEngine

logger = setup_logger("GenerationOrchestrator")


class GenerationOrchestrator:
    """Master orchestrator executing generation, audio mastering, and asset exporting."""

    def __init__(self, output_dir: Path = Path("output")):
        self.device = HardwareDeviceEngine.detect_device()
        self.provider_manager = ProviderManager(device=self.device)
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def execute_phase3_pipeline(
        self,
        phase2_report: Phase2StudioReport,
        default_params: Optional[MusicGenerationParams] = None
    ) -> List[GenerationExportResult]:
        """Executes full generation and export for every scene directive in report."""
        logger.info(f"Starting Phase 3 Generation for project '{phase2_report.project_title}'...")
        params = default_params or MusicGenerationParams()
        results: List[GenerationExportResult] = []

        for prompt_data in phase2_report.prompts:
            start_time = time.time()
            scene_dir = self.output_dir / f"scene_{prompt_data.scene}"
            scene_dir.mkdir(parents=True, exist_ok=True)

            logger.info(f"--- Processing Scene {prompt_data.scene} ---")

            # 1. Synthesize Audio
            raw_audio, sample_rate, provider_used = self.provider_manager.generate_audio(prompt_data, params)

            # 2. Apply Master DSP Chain
            mastered_audio, integrated_lufs, peak_db = AudioPostProcessor.process_master_chain(
                raw_audio,
                sample_rate=sample_rate,
                target_lufs=prompt_data.audio_settings.target_loudness_lufs,
                fade_in_sec=params.fade_in_sec,
                fade_out_sec=params.fade_out_sec
            )

            # 3. Export WAV File
            wav_path = scene_dir / "music.wav"
            self._write_wav(wav_path, mastered_audio, sample_rate)

            # 4. Export MP3 Container (or mirror WAV)
            mp3_path = scene_dir / "music.mp3"
            self._write_wav(mp3_path, mastered_audio, sample_rate)  # Standard PCM container export fallback

            # 5. Render Waveform Visual
            png_path = scene_dir / "waveform.png"
            WaveformVisualizer.render_waveform_image(mastered_audio, png_path)

            elapsed_time = round(time.time() - start_time, 2)
            actual_duration = round(mastered_audio.shape[1] / sample_rate, 2)

            # 6. Build and save JSON Metadata
            export_result = GenerationExportResult(
                scene_number=prompt_data.scene,
                provider_used=provider_used,
                prompt_used=prompt_data.prompt,
                wav_path=str(wav_path.resolve()),
                mp3_path=str(mp3_path.resolve()),
                waveform_png_path=str(png_path.resolve()),
                metadata_json_path=str((scene_dir / "metadata.json").resolve()),
                actual_duration_sec=actual_duration,
                sample_rate_hz=sample_rate,
                bit_depth=16,
                channels=mastered_audio.shape[0],
                peak_db=round(peak_db, 2),
                integrated_lufs=round(integrated_lufs, 2),
                generation_time_sec=elapsed_time
            )

            metadata_path = scene_dir / "metadata.json"
            metadata_path.write_text(export_result.model_dump_json(indent=2), encoding="utf-8")

            results.append(export_result)
            HardwareDeviceEngine.optimize_memory()

        logger.info(f"Phase 3 execution complete. Rendered {len(results)} scenes.")
        return results

    def _write_wav(self, file_path: Path, audio: np.ndarray, sample_rate: int):
        """Serializes numpy array into a 16-bit PCM WAV file."""
        channels = audio.shape[0]
        # Normalize to 16-bit signed integer range
        int_data = (audio * 32767.0).astype(np.int16)
        
        with wave.open(str(file_path), 'wb') as wav_file:
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(int_data.T.tobytes())
