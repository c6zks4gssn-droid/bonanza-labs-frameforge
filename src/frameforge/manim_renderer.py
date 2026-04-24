"""Manim renderer — generate animated videos using Manim."""

import os
import subprocess
import tempfile
from pathlib import Path


MANIM_SCENE_TEMPLATE = '''
from manim import *

class FrameForgeScene(Scene):
    def construct(self):
        # Scene 1: Title
        title = Text("{title}", font_size=48, color=WHITE)
        subtitle = Text("{subtitle}", font_size=24, color=GREY_A)
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(title), FadeIn(subtitle))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        # Scene 2: Bullets
        bullet_title = Text("{bullet_title}", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(bullet_title))
{bullet_items}
        self.wait(1)
        self.play(FadeOut(bullet_title){fade_bullets})

        # Scene 3: Counter
        counter_title = Text("{counter_title}", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(counter_title))
{counter_items}
        self.wait(1)
        self.play(FadeOut(counter_title){fade_counters})

        # Scene 4: CTA
        cta_title = Text("{cta_title}", font_size=48, color=WHITE)
        cta_sub = Text("{cta_sub}", font_size=28, color=GREEN)
        cta_sub.next_to(cta_title, DOWN, buff=0.5)
        self.play(FadeIn(cta_title), FadeIn(cta_sub))
        self.wait(2)
'''


def render_manim(scenes: list[dict], style: str = "product", output_path: str | None = None) -> str | None:
    """Render a video from scene dicts using Manim."""
    try:
        # Extract data from scenes
        title_data = next((s for s in scenes if s.get("type") == "title"), {})
        bullet_data = next((s for s in scenes if s.get("type") == "bullets"), {})
        counter_data = next((s for s in scenes if s.get("type") == "counter"), {})
        cta_data = next((s for s in scenes if s.get("type") == "cta"), {})

        # Build bullet items
        bullet_items_code = ""
        bullet_fade_list = []
        for i, item in enumerate(bullet_data.get("items", [])[:4]):
            y_pos = 1.5 - i * 0.8
            var_name = f"b{i}"
            bullet_items_code += f'\n        {var_name} = Text("{item}", font_size=28, color=WHITE).shift(DOWN*{y_pos:.1f})'
            bullet_items_code += f'\n        self.play(FadeIn({var_name}, shift=RIGHT*0.5))'
            bullet_fade_list.append(f", FadeOut({var_name})")

        # Build counter items
        counter_items_code = ""
        counter_fade_list = []
        for i, val in enumerate(counter_data.get("values", [])[:3]):
            x_pos = -3.5 + i * 3.5
            var_name = f"c{i}"
            end_val = val.get("end", 0)
            suffix = val.get("suffix", "")
            label = val.get("label", "")
            counter_items_code += f'\n        {var_name}_num = Integer(0, font_size=60, color=GREEN).shift(RIGHT*{x_pos:.1f}+DOWN*0.3)'
            counter_items_code += f'\n        {var_name}_label = Text("{label}", font_size=20, color=GREY_A).next_to({var_name}_num, DOWN)'
            counter_items_code += f'\n        {var_name}_suffix = Text("{suffix}", font_size=30, color=GREEN).next_to({var_name}_num, RIGHT, buff=0.1)'
            counter_items_code += f'\n        self.play(FadeIn({var_name}_num), FadeIn({var_name}_label), FadeIn({var_name}_suffix))'
            counter_items_code += f'\n        self.play({var_name}_num.animate.set_value({end_val}), run_time=1.5)'
            counter_fade_list.append(f", FadeOut({var_name}_num), FadeOut({var_name}_label), FadeOut({var_name}_suffix)")

        # Generate scene code
        scene_code = MANIM_SCENE_TEMPLATE.format(
            title=title_data.get("title", "Untitled"),
            subtitle=title_data.get("subtitle", ""),
            bullet_title=bullet_data.get("title", "Key Points"),
            bullet_items=bullet_items_code,
            fade_bullets="".join(bullet_fade_list),
            counter_title=counter_data.get("title", "The Numbers"),
            counter_items=counter_items_code,
            fade_counters="".join(counter_fade_list),
            cta_title=cta_data.get("title", "Get Started"),
            cta_sub=cta_data.get("subtitle", "Today"),
        )

        # Write to temp file and render
        tmp_dir = tempfile.mkdtemp()
        scene_file = Path(tmp_dir) / "frameforge_scene.py"
        scene_file.write_text(scene_code)

        output_dir = output_path or str(Path.cwd() / "frameforge_output")
        Path(output_dir).parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            "manim", str(scene_file), "FrameForgeScene",
            "-pql",  # preview, low quality for speed
            "--media_dir", tmp_dir,
            "--output_file", str(Path(output_dir) / "output.mp4") if output_path else None,
        ]
        cmd = [c for c in cmd if c is not None]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode == 0:
            # Find the output file
            for mp4 in Path(tmp_dir).rglob("*.mp4"):
                if "FrameForgeScene" in str(mp4):
                    final_path = output_path or str(Path.cwd() / "frameforge_output.mp4")
                    os.rename(str(mp4), final_path)
                    return final_path

        return None

    except FileNotFoundError:
        # manim not installed
        return None
    except Exception:
        return None