# Bonanza Labs ✦ FrameForge

🎬 AI Video Generator. Script → Voiceover → Video.

Powered by HyperFrames + Manim + Edge-TTS. By [Bonanza Labs](https://github.com/c6zks4gssn-droid).

## Features

- AI script writer — generate multi-scene scripts from a topic
- 4 style presets (viral, corporate, product, explainer)
- 3 formats (16:9, 9:16, 1:1)
- Edge-TTS voiceover with 100+ voices
- HyperFrames + Manim video rendering

## Install

```bash
pip install bonanza-labs[video]
```

## Quick Start

```bash
bonanza video "My Topic" --style viral --format 9:16
```

## Architecture

- `frameforge.py` — CLI entry point
- `src/` — Remotion components + compositions
- `remotion.config.ts` — Remotion bundler config

## License

Apache License 2.0
