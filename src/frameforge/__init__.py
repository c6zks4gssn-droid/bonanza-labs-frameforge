#!/usr/bin/env python3
"""
🎬 FrameForge Pro v0.2.0 — AI Video Studio
Script → Voice (VibeVoice) → Video (Remotion)

Usage:
  frameforge create "Topic" --style viral --format 9:16 --voice af_nicole
  frameforge create "Topic" --clone-voice ref.wav
  frameforge serve
  frameforge batch topics.txt
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

# voicebox imported lazily in functions
# manim_renderer imported lazily

WORKSPACE = Path.home() / ".openclaw/workspace"
REMONDIR = WORKSPACE / "frameforge-remotion"
OUTPUT_DIR = WORKSPACE / "frameforge" / "output"
VOICE_DIR = WORKSPACE / "voice-messages"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
VOICE_DIR.mkdir(parents=True, exist_ok=True)

STYLES = ["viral", "corporate", "product", "explainer"]
FORMATS = {"16:9": (1920, 1080), "9:16": (1080, 1920), "1:1": (1080, 1080)}
ENGINES = ["auto", "voicebox", "kokoro", "edge", "manim"]


def run(cmd, timeout=300):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout + r.stderr).strip()


def generate_script(topic, style="viral"):
    """Generate video script from topic (uses fallback template)."""
    style_config = {
        "viral": {"vibe": "punchy, high-energy"},
        "corporate": {"vibe": "professional, trustworthy"},
        "product": {"vibe": "clean, feature-focused"},
        "explainer": {"vibe": "educational, clear"},
    }.get(style, {"vibe": "professional"})

    scenes = [
        {"type": "title", "title": topic, "subtitle": "Introducing the future", "duration": 60},
        {"type": "bullets", "title": "Why It Matters", "items": ["Fast and reliable", "Easy to use", "Built for everyone"], "duration": 60},
        {"type": "comparison", "title": "How It Compares", "left": {"label": "Before", "items": ["Slow", "Expensive", "Complex"]}, "right": {"label": topic, "items": ["Lightning fast", "Free & open", "Simple"]}, "duration": 60},
        {"type": "counter", "title": "The Numbers", "values": [{"label": "Speed", "end": 10, "suffix": "x"}, {"label": "Savings", "end": 50, "suffix": "%"}, {"label": "Uptime", "end": 99, "suffix": ".9%"}], "duration": 60},
        {"type": "cta", "title": "Get Started", "subtitle": "Bonanza Labs", "duration": 60},
    ]
    return scenes


def generate_voiceover(scenes, voice_preset="af_nicole", output_path=None, clone_ref=None, engine="auto", speed=1.0):
    from frameforge.voicebox import generate_voiceover as vb_generate_voiceover, is_voicebox_available, list_voices
    """Generate voiceover using Voicebox/Kokoro with Edge-TTS fallback."""
    if not output_path:
        output_path = str(VOICE_DIR / f"voiceover_{int(time.time())}.mp3")

    narration_parts = []
    for s in scenes:
        if s["type"] == "title":
            narration_parts.append(f"{s['title']}. {s['subtitle']}.")
        elif s["type"] == "bullets":
            narration_parts.append(f"{s['title']}. " + ". ".join(s["items"]))
        elif s["type"] == "comparison":
            narration_parts.append(f"{s['title']}. {s['left']['label']}: " + ", ".join(s["left"]["items"]) + f". {s['right']['label']}: " + ", ".join(s["right"]["items"]))
        elif s["type"] == "counter":
            vals = ", ".join(f"{v['end']}{v.get('suffix', '')} {v['label']}" for v in s["values"])
            narration_parts.append(f"{s['title']}. {vals}")
        elif s["type"] == "cta":
            narration_parts.append(f"{s['title']}. {s['subtitle']}.")

    narration = " ... ".join(narration_parts)
    
    engine_label = {"auto": "auto (Voicebox → Kokoro → Edge)", "voicebox": "Voicebox", "kokoro": "Kokoro", "edge": "Edge-TTS"}.get(engine, engine)
    print(f"   Engine: {engine_label}")
    
    result = vb_generate_voiceover(
        text=narration,
        voice=voice_preset,
        output_path=output_path,
        clone_ref=clone_ref,
        engine=engine,
        speed=speed,
    )
    return result


def render_remotion(scenes, style, fmt, voiceover_path=None, output_path=None):
    """Render video using Remotion CLI."""
    if not output_path:
        output_path = str(OUTPUT_DIR / f"frameforge_{int(time.time())}.mp4")

    w, h = FORMATS.get(fmt, (1920, 1080))

    # Write scenes as props JSON
    props = {
        "topic": scenes[0]["title"] if scenes else "Untitled",
        "style": style,
        "scenes": scenes,
        "voicePreset": "af_nicole",
        "format": fmt,
    }
    props_path = str(OUTPUT_DIR / "props.json")
    with open(props_path, "w") as f:
        json.dump(props, f)

    total_frames = sum(s["duration"] for s in scenes)

    # Render using Remotion CLI
    cmd = f'cd "{REMONDIR}" && npx remotion render FullVideo "{output_path}" --props "{props_path}" --width {w} --height {h} --frames 0-{total_frames}'
    print(f"🎬 Rendering with Remotion...")
    print(f"   Scenes: {len(scenes)} | Style: {style} | Format: {fmt} ({w}x{h})")
    rc, out = run(cmd, timeout=600)

    if rc == 0 and os.path.exists(output_path):
        # Add voiceover if available
        if voiceover_path and os.path.exists(voiceover_path):
            final = output_path.replace(".mp4", "_final.mp4")
            run(f'ffmpeg -y -i "{output_path}" -i "{voiceover_path}" -c:v copy -c:a aac -shortest "{final}"', timeout=60)
            if os.path.exists(final):
                os.replace(final, output_path)
        print(f"✅ Video saved: {output_path}")
        return output_path
    else:
        print(f"❌ Remotion render failed: {out[-500:]}")
        return None


def create_video(topic, style="viral", fmt="16:9", voice="af_nicole", clone_voice=None, engine="auto", speed=1.0):
    """Full pipeline: script → voice → video."""
    print(f"🎬 FrameForge Pro — Creating video")
    print(f"   Topic: {topic}")
    print(f"   Style: {style} | Format: {fmt} | Voice: {voice} | Engine: {engine}")

    # 1. Generate script
    print("\n📝 Generating script...")
    scenes = generate_script(topic, style)
    print(f"   {len(scenes)} scenes created")

    # 2. Generate voiceover
    print("\n🎙️ Generating voiceover...")
    voiceover = generate_voiceover(scenes, voice, clone_ref=clone_voice, engine=engine, speed=speed)
    if voiceover:
        print(f"   ✅ Voiceover: {voiceover}")
    else:
        print(f"   ⚠️ Voiceover failed, continuing without")

    # 3. Render video
    print("\n🎬 Rendering video...")
    result = render_video(scenes, style, fmt, voiceover)
    return result


def serve():
    """Start Remotion Studio for live preview."""
    print("🎬 Starting FrameForge Studio (Remotion)...")
    print("   Open http://localhost:3000 in your browser")
    os.system(f'cd "{REMONDIR}" && npx remotion studio src/index.ts')


def main():
    parser = argparse.ArgumentParser(description="🎬 FrameForge Pro v0.2.0 — AI Video Studio")
    sub = parser.add_subparsers(dest="command")

    # Create
    p_create = sub.add_parser("create", help="Create a video from a topic")
    p_create.add_argument("topic", help="Video topic")
    p_create.add_argument("--style", "-s", default="product", choices=STYLES, help="Video style")
    p_create.add_argument("--format", "-f", default="16:9", choices=FORMATS.keys(), help="Video format")
    p_create.add_argument("--voice", "-v", default="af_nicole", help="Voice preset")
    p_create.add_argument("--clone-voice", help="Reference audio for voice cloning")
    p_create.add_argument("--engine", "-e", default="auto", choices=ENGINES, help="TTS engine (auto/voicebox/kokoro/edge)")
    p_create.add_argument("--speed", type=float, default=1.0, help="Speech speed (1.0 = normal)")
    p_create.add_argument("--output", "-o", help="Output file path")

    # Serve
    sub.add_parser("serve", help="Start Remotion Studio for live preview")

    # Batch
    p_batch = sub.add_parser("batch", help="Create videos from a topics file")
    p_batch.add_argument("file", help="File with one topic per line")
    p_batch.add_argument("--style", "-s", default="product", choices=STYLES)
    p_batch.add_argument("--format", "-f", default="16:9", choices=FORMATS.keys())
    p_batch.add_argument("--voice", "-v", default="af_nicole", help="Voice preset")
    p_batch.add_argument("--engine", "-e", default="auto", choices=ENGINES, help="TTS engine")

    # Voices
    sub.add_parser("voices", help="List available voice presets")

    # Engines
    sub.add_parser("engines", help="List available TTS engines")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "voices":
        print("🎙️ Available Voice Presets:\n")
        voices = list_voices()
        for name, engines in voices.items():
            label = name.replace("_", " ").title()
            engine_str = " | ".join(f"{k}: {v}" for k, v in engines.items())
            print(f"  {name:15} → {label} ({engine_str})")
        return

    if args.command == "engines":
        print("🎙️ Available TTS Engines:\n")
        print(f"  voicebox  → {'✅ Available' if is_voicebox_available() else '❌ Not found'}")
        try:
            import kokoro
            print("  kokoro    → ✅ Available")
        except ImportError:
            print("  kokoro    → ❌ Not installed")
        print("  edge      → ✅ Always available (Edge-TTS)")
        print("\n  Use --engine auto to select best available")
        return

    if args.command == "create":
        create_video(args.topic, args.style, args.format, args.voice, args.clone_voice, args.engine, args.speed)

    elif args.command == "serve":
        serve()

    elif args.command == "batch":
        with open(args.file) as f:
            topics = [line.strip() for line in f if line.strip()]
        print(f"🎬 Batch: {len(topics)} videos")
        for i, topic in enumerate(topics):
            print(f"\n--- Video {i+1}/{len(topics)}: {topic} ---")
            create_video(topic, args.style, args.format, args.voice, engine=args.engine)


if __name__ == "__main__":
    main()
def render_video(scenes, style="product", fmt="16:9", voiceover_path=None, output_path=None):
    from frameforge.manim_renderer import render_manim
    """Render video — tries Manim first, falls back to Remotion."""
    # Try Manim (no Node.js needed)
    result = render_manim(scenes, style, output_path)
    if result:
        return result
    
    # Fall back to Remotion
    return render_remotion(scenes, style, fmt, voiceover_path, output_path)
