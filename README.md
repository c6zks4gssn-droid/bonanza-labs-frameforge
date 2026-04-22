# Bonanza Labs ✦ FrameForge

🎬 AI Video Generator. Script → Voiceover → Video.

Powered by HyperFrames + Manim + Edge-TTS + Voicebox (Kokoro). By [Bonanza Labs](https://github.com/c6zks4gssn-droid).

## Features

- AI script writer — generate multi-scene scripts from a topic
- 4 style presets (viral, corporate, product, explainer)
- 3 formats (16:9, 9:16, 1:1)
- Multiple TTS engines:
  - **Voicebox/Kokoro** — highest quality, local, voice cloning
  - **Edge-TTS** — fast fallback, 100+ voices
- Voice cloning — clone any voice from a 10-30s audio sample
- Remotion video rendering

## Install

```bash
pip install bonanza-labs-frameforge
```

## Quick Start

```bash
# Create a video (auto-selects best TTS engine)
frameforge create "AI Agents Are the Future" --style viral --format 9:16

# Use specific TTS engine
frameforge create "My Topic" --engine kokoro --voice af_nicole

# Clone a voice
frameforge create "Product Demo" --clone-voice my_voice.wav --engine voicebox

# List available voices
frameforge voices

# List available TTS engines
frameforge engines

# Start Remotion Studio for live preview
frameforge serve
```

## TTS Engines

| Engine | Quality | Speed | Voice Cloning | Local |
|--------|---------|-------|---------------|-------|
| Voicebox | ⭐⭐⭐⭐⭐ | Medium | ✅ | ✅ |
| Kokoro | ⭐⭐⭐⭐ | Fast | ❌ | ✅ |
| Edge-TTS | ⭐⭐⭐ | Fast | ❌ | ❌ (API) |

Use `--engine auto` (default) to automatically select the best available engine.

## Architecture

- `frameforge.py` — CLI entry point
- `src/frameforge/voicebox.py` — Voicebox/Kokoro integration
- `src/` — Remotion components + compositions
- `remotion.config.ts` — Remotion bundler config

## License

Apache License 2.0
