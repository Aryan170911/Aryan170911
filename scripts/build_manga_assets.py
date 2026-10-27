"""Build deterministic, GitHub-safe manga profile assets."""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
MANGA = ROOT / "assets" / "manga"
PANEL_NAMES = ("hero.png", "journey.png", "training.png", "finale.png")
PAPER = "#f4e9d8"
INK = "#111111"
ORANGE = "#f47a1f"
LAVENDER = "#8c73c7"


def _draw_konoha_mark(image: Image.Image, reveal: float) -> None:
    """Fade and scale a crisp Hidden Leaf-inspired crest into the ink wipe."""
    if reveal <= 0:
        return

    supersample = 4
    badge_size = 72
    canvas_size = badge_size * supersample
    badge = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge)

    inset = 4 * supersample
    draw.ellipse(
        (inset, inset, canvas_size - inset, canvas_size - inset),
        fill=ORANGE,
        outline=INK,
        width=3 * supersample,
    )

    center_x = canvas_size / 2 - 2 * supersample
    center_y = canvas_size / 2 + 2 * supersample
    spiral: list[tuple[float, float]] = []
    steps = 96
    for step in range(steps):
        theta = (step / (steps - 1)) * math.tau * 1.08
        radius = (2.5 + 18.5 * step / (steps - 1)) * supersample
        spiral.append(
            (
                center_x + radius * math.cos(-theta),
                center_y + radius * math.sin(-theta),
            )
        )

    stroke = 4 * supersample
    draw.line(spiral, fill=INK, width=stroke, joint="curve")
    end_x, end_y = spiral[-1]
    draw.line(
        (
            (end_x, end_y),
            (center_x + 27 * supersample, center_y - 2 * supersample),
            (center_x + 31 * supersample, center_y - 7 * supersample),
        ),
        fill=INK,
        width=stroke,
        joint="curve",
    )

    # The pointed upper flick turns the spiral into the familiar leaf silhouette.
    draw.polygon(
        (
            (center_x - 18 * supersample, center_y - 12 * supersample),
            (center_x - 14 * supersample, center_y - 29 * supersample),
            (center_x + 1 * supersample, center_y - 19 * supersample),
        ),
        fill=INK,
    )

    badge = badge.resize((badge_size, badge_size), Image.Resampling.LANCZOS)
    scale = 0.72 + 0.28 * reveal
    rendered_size = max(1, round(badge_size * scale))
    if rendered_size != badge_size:
        badge = badge.resize((rendered_size, rendered_size), Image.Resampling.LANCZOS)

    alpha = badge.getchannel("A").point(lambda value: round(value * reveal))
    badge.putalpha(alpha)
    position = ((image.width - rendered_size) // 2, (image.height - rendered_size) // 2)
    image.paste(badge, position, badge)


def optimize_panels() -> None:
    for filename in PANEL_NAMES:
        path = MANGA / filename
        with Image.open(path) as source:
            image = source.convert("RGB")
            target_height = round(image.height * 900 / image.width)
            image = image.resize((900, target_height), Image.Resampling.LANCZOS)
            image.save(path, format="PNG", optimize=True, compress_level=9)


def build_transition() -> None:
    width, height = 900, 84
    rng = random.Random(170911)
    frames: list[Image.Image] = []

    for index in range(20):
        image = Image.new("RGB", (width, height), PAPER)
        draw = ImageDraw.Draw(image)
        progress = index / 19
        edge = int((width + 180) * progress) - 90

        draw.line((0, height // 2, width, height // 2), fill="#342f2a", width=2)
        for _ in range(48):
            y = rng.randint(5, height - 5)
            length = rng.randint(40, 170)
            start = rng.randint(-80, max(-79, edge))
            thickness = rng.randint(1, 7)
            color = INK if rng.random() > 0.18 else (ORANGE if rng.random() > 0.5 else LAVENDER)
            draw.line((start, y, min(width, start + length), y + rng.randint(-5, 5)), fill=color, width=thickness)

        points = [(0, 0), (max(0, edge - 70), 0)]
        for y in range(0, height + 12, 12):
            points.append((max(0, min(width, edge + rng.randint(-50, 45))), y))
        points.extend([(0, height), (0, 0)])
        draw.polygon(points, fill=INK)

        for _ in range(24):
            low = max(0, min(width - 1, edge - 80))
            high = max(low, min(width - 1, edge + 45))
            x = rng.randint(low, high)
            y = rng.randint(0, height - 1)
            radius = rng.randint(1, 4)
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=INK)

        mark_reveal = max(0.0, min(1.0, (progress - 0.24) / 0.46))
        _draw_konoha_mark(image, mark_reveal)
        frames.append(image)

    frames += list(reversed(frames[1:-1]))
    frames[0].save(
        MANGA / "ink-transition.gif",
        save_all=True,
        append_images=frames[1:],
        duration=70,
        loop=0,
        optimize=True,
        disposal=2,
    )


def build_divider() -> None:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="92" viewBox="0 0 900 92" role="img" aria-labelledby="title desc">
  <title id="title">Next manga chapter</title>
  <desc id="desc">Ink lines and halftone dots introduce the next chapter.</desc>
  <defs>
    <pattern id="dots" width="10" height="10" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.4" fill="{INK}" opacity=".35"/>
    </pattern>
  </defs>
  <rect width="900" height="92" rx="12" fill="{PAPER}"/>
  <path d="M28 45 H356 M544 45 H872" stroke="{INK}" stroke-width="4"/>
  <path d="M28 54 H330 M570 54 H872" stroke="{ORANGE}" stroke-width="2"/>
  <rect x="381" y="16" width="138" height="60" transform="rotate(-2 450 46)" fill="url(#dots)" stroke="{INK}" stroke-width="3"/>
  <text x="450" y="42" text-anchor="middle" font-family="Arial Black,Impact,sans-serif" font-size="12" letter-spacing="3" fill="{INK}">NEXT</text>
  <text x="450" y="59" text-anchor="middle" font-family="Arial Black,Impact,sans-serif" font-size="15" letter-spacing="2" fill="{INK}">CHAPTER</text>
</svg>'''
    (MANGA / "chapter-divider.svg").write_text(svg, encoding="utf-8")


def main() -> None:
    MANGA.mkdir(parents=True, exist_ok=True)
    optimize_panels()
    build_transition()
    build_divider()


if __name__ == "__main__":
    main()

