"""LLM Script Generator — generates video scripts from topics using GLM 5.1 cloud."""

from __future__ import annotations
import json
import httpx
import os
from typing import Optional

OLLAMA_LOCAL = "http://localhost:11434/api/chat"
OLLAMA_CLOUD = "https://api.ollama.com/v1/chat/completions"
OLLAMA_KEY = os.getenv("OLLAMA_API_KEY", "")


SCRIPT_PROMPT = """You are a video scriptwriter. Generate a JSON array of 5 scenes for a short video about: "{topic}"

Style: {style}

Each scene must be one of these types with these fields:
1. title: {{"type": "title", "title": "...", "subtitle": "...", "duration": 60}}
2. bullets: {{"type": "bullets", "title": "...", "items": ["...", "..."], "duration": 60}}
3. comparison: {{"type": "comparison", "title": "...", "left": {{"label": "...", "items": [...]}}, "right": {{"label": "...", "items": [...]}}, "duration": 60}}
4. counter: {{"type": "counter", "title": "...", "values": [{{"label": "...", "end": N, "suffix": "..."}}], "duration": 60}}
5. cta: {{"type": "cta", "title": "...", "subtitle": "...", "duration": 60}}

Rules:
- Duration is always 60 (frames at 30fps = 2 seconds per scene)
- Content must be specific to the topic, not generic
- Counter values must be realistic numbers
- Keep text short and punchy (max 5 words per bullet)
- Comparison should show before/after or competitor vs us

Return ONLY the JSON array, no markdown, no explanation."""


def generate_script_llm(topic: str, style: str = "product") -> Optional[list[dict]]:
    """Generate video script using GLM 5.1 cloud via local Ollama proxy."""
    return _generate_local(topic, style)


def _generate_local(topic: str, style: str = "product") -> Optional[list[dict]]:
    """Fallback: generate via local Ollama."""
    try:
        resp = httpx.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "glm-5.1:cloud",
                "messages": [{"role": "user", "content": SCRIPT_PROMPT.format(topic=topic, style=style)}],
                "stream": False,
            },
            timeout=60,
        )
        if resp.status_code == 200:
            content = resp.json()["message"]["content"]
            content = content.strip()
            if content.startswith("```"):
                content = content.split("\n", 1)[1].rsplit("```", 1)[0]
            return json.loads(content)
    except Exception as e:
        print(f"Local LLM failed: {e}")

    return None


# Template fallback (always works)
def generate_script_template(topic: str, style: str = "product") -> list[dict]:
    """Generate video script from topic (template fallback)."""
    return [
        {"type": "title", "title": topic, "subtitle": "The future is here", "duration": 60},
        {"type": "bullets", "title": "Why It Matters", "items": ["Lightning fast", "Easy to use", "Built for everyone"], "duration": 60},
        {"type": "comparison", "title": "How It Compares", "left": {"label": "Before", "items": ["Slow", "Expensive", "Complex"]}, "right": {"label": topic, "items": ["10x faster", "Free & open", "Simple"]}, "duration": 60},
        {"type": "counter", "title": "The Numbers", "values": [{"label": "Speed", "end": 10, "suffix": "x"}, {"label": "Savings", "end": 50, "suffix": "%"}, {"label": "Uptime", "end": 99, "suffix": ".9%"}], "duration": 60},
        {"type": "cta", "title": "Get Started", "subtitle": "Bonanza Labs", "duration": 60},
    ]


def generate_script(topic: str, style: str = "product", use_llm: bool = True) -> list[dict]:
    """Generate video script. Tries LLM first, falls back to template."""
    if use_llm:
        result = generate_script_llm(topic, style)
        if result and isinstance(result, list) and len(result) >= 3:
            # Validate scenes have required fields
            for scene in result:
                if "type" not in scene or "duration" not in scene:
                    print(f"Invalid scene: {scene}, using template")
                    return generate_script_template(topic, style)
            print(f"✅ LLM generated {len(result)} scenes")
            return result
        print("LLM output invalid, using template")

    return generate_script_template(topic, style)


if __name__ == "__main__":
    import sys
    topic = sys.argv[1] if len(sys.argv) > 1 else "Bonanza Labs"
    style = sys.argv[2] if len(sys.argv) > 2 else "product"
    scenes = generate_script(topic, style, use_llm=True)
    print(json.dumps(scenes, indent=2))