## Phase 4: Professional Audio Processing Engine

Phase 4 introduces a full-featured mastering and DSP engine for raw AI-generated audio assets.

### Features
* **Broadcast LUFS Normalization**: Integrated EBU R128 loudness targeting (-14 LUFS default).
* **True Peak Brickwall Limiter**: Zero-clipping lookahead limiting (-1.0 dB ceiling).
* **Parametric Equalizer**: Low-shelf, high-shelf, and multi-band peaking biquad filters.
* **Smart Voice Ducking**: Automatic dynamic sidechain music ducking when speech narration is active.
* **Multiformat Exporter**: Export mastering suites directly to 24-bit WAV, FLAC, and MP3 along with metadata manifests and visual waveform diagnostic plots.

### Usage Example
```python
from audio_processor import BaseAudioProcessor
from mastering_engine import MasteringEngine
from export_engine import ExportEngine
from waveform_generator import WaveformGenerator

# Initialize
sample_rate = 48000
mastering_sys = MasteringEngine(sample_rate=sample_rate)

# Load Audio
music_buf = mastering_sys.base_proc.load_audio("raw_music.wav")
narration_buf = mastering_sys.base_proc.load_audio("narration.wav")

# Master
mastered_buf = mastering_sys.master_soundtrack(music_buf, narration_buf, target_lufs=-14.0)

# Export Package
exporter = ExportEngine(sample_rate=sample_rate)
export_files = exporter.export_all(mastered_buf.data, output_dir="./output")

# Generate Waveform Plots
wf = WaveformGenerator()
wf.generate_all_plots(mastered_buf.data, sample_rate, "./output/waveform.png")
