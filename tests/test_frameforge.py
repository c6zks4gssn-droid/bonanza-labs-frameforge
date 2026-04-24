"""Tests for FrameForge."""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestSceneGeneration:
    """Test script generation."""

    def test_generate_script_viral(self):
        from frameforge import generate_script
        scenes = generate_script("Test Topic", "viral")
        assert len(scenes) > 0
        assert scenes[0]["type"] == "title"
        assert "Test Topic" in scenes[0]["title"]

    def test_generate_script_all_styles(self):
        from frameforge import generate_script
        for style in ["viral", "corporate", "product", "explainer"]:
            scenes = generate_script("Topic", style)
            assert len(scenes) > 0

    def test_script_has_expected_scenes(self):
        from frameforge import generate_script
        scenes = generate_script("AI Tools", "product")
        types = [s["type"] for s in scenes]
        assert "title" in types
        assert "cta" in types


class TestVoiceoverGeneration:
    """Test voiceover text generation."""

    def test_narration_parts(self):
        from frameforge import generate_script
        scenes = generate_script("Test", "viral")
        # Verify scenes have narration-compatible data
        for s in scenes:
            assert "type" in s
            assert "duration" in s


class TestFormats:
    """Test video format definitions."""

    def test_formats_defined(self):
        from frameforge import FORMATS
        assert "16:9" in FORMATS
        assert "9:16" in FORMATS
        assert "1:1" in FORMATS

    def test_format_dimensions(self):
        from frameforge import FORMATS
        assert FORMATS["16:9"] == (1920, 1080)
        assert FORMATS["9:16"] == (1080, 1920)
        assert FORMATS["1:1"] == (1080, 1080)


class TestManimRenderer:
    """Test Manim scene generation."""

    def test_import(self):
        from frameforge.manim_renderer import render_manim
        assert callable(render_manim)

    def test_scene_template_exists(self):
        from frameforge.manim_renderer import MANIM_SCENE_TEMPLATE
        assert "FrameForgeScene" in MANIM_SCENE_TEMPLATE
        assert "construct" in MANIM_SCENE_TEMPLATE


class TestVoicebox:
    """Test voicebox module."""

    def test_edge_voices(self):
        from frameforge.voicebox import EDGE_VOICES
        assert "af_heart" in EDGE_VOICES
        assert "af_nicole" in EDGE_VOICES
        assert "am_adam" in EDGE_VOICES

    def test_list_voices(self):
        from frameforge.voicebox import list_voices
        voices = list_voices()
        assert isinstance(voices, dict)
        assert len(voices) > 0
