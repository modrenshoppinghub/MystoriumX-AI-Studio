# MystoriumX AI Studio (v1.0 Production Release)

**MystoriumX AI Studio** is an audio processing engine designed to transform raw AI-generated music tracks into cinematic documentary soundtracks.

---

## Key Features

- **Automated Loudness Normalization**: Target specific broadcast standards (e.g., -14.0 LUFS for streaming).
- **Voice Ducking Engine**: Dynamically attenuates background audio whenever speech is detected.
- **Parametric Equalization & Dynamic Compression**: High-pass, low-pass, peaking filters, and dynamic compression.
- **Lookahead True Peak Limiter**: Prevents clipping with a configurable dB ceiling (default: -1.0 dB).
- **Multi-Format Audio Exporter**: Generates broadcast-ready 24-bit WAV, 320kbps MP3, and FLAC formats alongside metadata manifests.
- **Visual Analytics**: Generates combined waveform graphs, FFT frequency spectra, and RMS loudness profiles.

---

## Quick Start

### Local Setup
```bash
# 1. Clone & Setup virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Process an audio asset
python main.py -m raw_music.wav -n narration.wav -o ./mastered_output
