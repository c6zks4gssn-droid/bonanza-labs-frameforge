#!/usr/bin/env python3
"""
🎙️ Voicebox Integration for FrameForge
Uses Voicebox (Kokoro engine) for high-quality TTS and voice cloning.
Falls back to Edge-TTS when Voicebox is unavailable.
"""

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# Voicebox paths
VOICEBOX_DIR = Path.home() / ".openclaw/workspace/skills/voice-os"
VOICEBOX_PY = VOICEBOX_DIR / "voice.py"
KOKORO_MODEL = Path.home() / ".openclaw/workspace/voicebox/models/kokoro-v1.0.pth"

# Edge-TTS fallback voices
EDGE_VOICES = {
    "af_heart": "en-US-AriaNeural",
    "af_nicole": "en-US-JennyNeural",
    "am_adam": "en-US-GuyNeural",
    "am_michael": "en-US-ChristopherNeural",
    "bf_emma": "en-GB-SoniaNeural",
    "bm_george": "en-GB-ThomasNeural",
}

# Kokoro voice presets
KOKORO_VOICES = {
    "af_heart": "af_heart",
    "af_nicole": "af_nicole",
    "af_sky": "af_sky",
    "am_adam": "am_adam",
    "am_michael": "am_michael",
    "bf_emma": "bf_emma",
    "bm_george": "bm_george",
}


def is_voicebox_available() -> bool:
    """Check if Voicebox/Kokoro is available."""
    if VOICEBOX_PY.exists():
        return True
    # Check if voicebox is installed as a command
    result = subprocess.run(["which", "voicebox"], capture_output=True)
    return result.returncode == 0


def generate_with_voicebox(
    text: str,
    voice: str = "af_nicole",
    output_path: str = None,
    clone_ref: str = None,
    speed: float = 1.0,
) -> str | None:
    """
    Generate voiceover using Voicebox (Kokoro engine).
    
    Args:
        text: Text to speak
        voice: Voice preset name
        output_path: Output audio file path
        clone_ref: Path to reference audio for voice cloning
        speed: Speech speed multiplier
    
    Returns:
        Path to generated audio file, or None on failure
    """
    if not output_path:
        output_path = str(tempfile.mktemp(suffix=".wav", prefix="voicebox_"))

    cmd = [
        sys.executable, str(VOICEBOX_PY), "speak",
        "--text", text,
        "--voice", voice,
        "--output", output_path,
    ]
    
    if clone_ref:
        cmd.extend(["--clone-voice", clone_ref])
    
    if speed != 1.0:
        cmd.extend(["--speed", str(speed)])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0 and os.path.exists(output_path):
            return output_path
        else:
            print(f"⚠️ Voicebox failed: {result.stderr[-200:] if result.stderr else 'unknown error'}")
            return None
    except subprocess.TimeoutExpired:
        print("⚠️ Voicebox timed out")
        return None
    except FileNotFoundError:
        print("⚠️ Voicebox not found")
        return None


def generate_with_kokoro_direct(
    text: str,
    voice: str = "af_nicole",
    output_path: str = None,
    speed: float = 1.0,
) -> str | None:
    """
    Generate voiceover using Kokoro directly (via soundfile pipeline).
    Higher quality than Edge-TTS, runs locally.
    """
    try:
        import soundfile as sf
        from kokoro import KPipeline
        
        if not output_path:
            output_path = str(tempfile.mktemp(suffix=".wav", prefix="kokoro_"))
        
        pipeline = KPipeline(lang_code='a')  # American English
        
        # Map voice preset to Kokoro voice pack
        kokoro_voice = KOKORO_VOICES.get(voice, "af_nicole")
        
        generator = pipeline(text, voice=kokoro_voice, speed=speed)
        
        # Collect all audio chunks
        audio_chunks = []
        for _, _, audio in generator:
            audio_chunks.append(audio)
        
        if audio_chunks:
            import numpy as np
            full_audio = np.concatenate(audio_chunks)
            sf.write(output_path, full_audio, 24000)
            return output_path
        
        return None
    except ImportError:
        print("⚠️ Kokoro not installed, falling back to Edge-TTS")
        return None
    except Exception as e:
        print(f"⚠️ Kokoro error: {e}")
        return None


def generate_with_edge_tts(
    text: str,
    voice: str = "af_nicole",
    output_path: str = None,
) -> str | None:
    """
    Generate voiceover using Edge-TTS (fallback).
    Fast but lower quality than Kokoro.
    """
    if not output_path:
        output_path = str(tempfile.mktemp(suffix=".mp3", prefix="edge_"))

    edge_voice = EDGE_VOICES.get(voice, "en-US-JennyNeural")
    
    # Escape text for shell
    escaped_text = text.replace('"', '\\"').replace("'", "\\'")
    
    cmd = f'edge-tts --voice "{edge_voice}" --text "{escaped_text}" --write-media "{output_path}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
    
    if result.returncode == 0 and os.path.exists(output_path):
        # Enhance audio quality
        enhanced = output_path.replace(".mp3", "_hq.m4a")
        enhance_cmd = (
            f'ffmpeg -y -i "{output_path}" '
            f'-af "aresample=48000,highpass=f=100,treble=g=6,volume=1.5" '
            f'-ar 48000 -ac 2 -c:a aac -b:a 128k "{enhanced}"'
        )
        subprocess.run(enhance_cmd, shell=True, capture_output=True, timeout=30)
        if os.path.exists(enhanced):
            os.replace(enhanced, output_path)
        return output_path
    
    return None


def generate_voiceover(
    text: str,
    voice: str = "af_nicole",
    output_path: str = None,
    clone_ref: str = None,
    engine: str = "auto",
    speed: float = 1.0,
) -> str | None:
    """
    Generate voiceover with automatic engine selection.
    
    Args:
        text: Text to speak
        voice: Voice preset (af_nicole, am_adam, etc.)
        output_path: Output file path
        clone_ref: Reference audio for voice cloning (Voicebox only)
        engine: "auto", "voicebox", "kokoro", or "edge"
        speed: Speech speed (1.0 = normal)
    
    Returns:
        Path to generated audio, or None on failure
    
    Engine priority (auto):
        1. Voicebox (if available + clone_ref provided)
        2. Kokoro (if installed)
        3. Edge-TTS (always available as fallback)
    """
    if not output_path:
        ext = ".wav" if engine in ("voicebox", "kokoro") else ".mp3"
        output_path = str(tempfile.mktemp(suffix=ext, prefix="frameforge_"))

    if engine == "auto":
        # Try Voicebox first (especially for cloning)
        if clone_ref and is_voicebox_available():
            result = generate_with_voicebox(text, voice, output_path, clone_ref, speed)
            if result:
                return result
        
        # Try Kokoro directly
        result = generate_with_kokoro_direct(text, voice, output_path, speed)
        if result:
            return result
        
        # Fallback to Edge-TTS
        return generate_with_edge_tts(text, voice, output_path)
    
    elif engine == "voicebox":
        return generate_with_voicebox(text, voice, output_path, clone_ref, speed)
    
    elif engine == "kokoro":
        return generate_with_kokoro_direct(text, voice, output_path, speed)
    
    elif engine == "edge":
        return generate_with_edge_tts(text, voice, output_path)
    
    else:
        print(f"⚠️ Unknown engine: {engine}")
        return generate_with_edge_tts(text, voice, output_path)


def list_voices() -> dict:
    """List all available voice presets and their engines."""
    voices = {}
    for name in set(list(EDGE_VOICES.keys()) + list(KOKORO_VOICES.keys())):
        voices[name] = {
            "edge_tts": EDGE_VOICES.get(name, "N/A"),
            "kokoro": KOKORO_VOICES.get(name, "N/A"),
            "voicebox": "✅" if is_voicebox_available() else "N/A",
        }
    return voices