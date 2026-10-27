"""Validate local profile assets and GitHub-safe README references."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
MANGA = ROOT / "assets" / "manga"
PANELS = ("hero.png", "journey.png", "training.png", "finale.png")
REQUIRED = (*PANELS, "ink-transition.gif", "chapter-divider.svg")
RIGHTS_NOTE = "Unofficial fan-made profile artwork"
MAX_PANEL_BYTES = 3_000_000
MAX_GIF_BYTES = 1_500_000


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    text = README.read_text(encoding="utf-8") if README.exists() else ""

    for name in REQUIRED:
        path = MANGA / name
        if not path.exists():
            fail(f"missing asset: {path.relative_to(ROOT)}", errors)
            continue
        if f"./assets/manga/{name}" not in text:
            fail(f"README does not reference assets/manga/{name}", errors)

    for name in PANELS:
        path = MANGA / name
        if not path.exists():
            continue
        with Image.open(path) as image:
            if image.width != 900:
                fail(f"{name} must be exactly 900px wide, got {image.width}", errors)
        if path.stat().st_size > MAX_PANEL_BYTES:
            fail(f"{name} exceeds {MAX_PANEL_BYTES} bytes", errors)

    gif_path = MANGA / "ink-transition.gif"
    if gif_path.exists():
        with Image.open(gif_path) as gif:
            if getattr(gif, "n_frames", 1) < 8:
                fail("ink-transition.gif must contain at least 8 frames", errors)
        if gif_path.stat().st_size > MAX_GIF_BYTES:
            fail(f"ink-transition.gif exceeds {MAX_GIF_BYTES} bytes", errors)

    local_sources = re.findall(r'src="\.?/?([^"#?]+)"', text)
    for source in local_sources:
        if source.startswith(("http://", "https://")):
            continue
        path = ROOT / source
        if not path.exists():
            fail(f"broken local README asset: {source}", errors)

    informative_images = re.findall(r'<img\s+[^>]*src="[^"]+"[^>]*>', text)
    for tag in informative_images:
        if re.search(r'alt="([^"]*)"', tag) is None:
            fail(f"image lacks alt attribute: {tag[:80]}", errors)

    if RIGHTS_NOTE not in text:
        fail("fan-art rights note is missing", errors)

    for svg in list((ROOT / "assets").glob("*.svg")) + list(MANGA.glob("*.svg")):
        body = svg.read_text(encoding="utf-8")
        for forbidden in ("<script", "<foreignObject", "<animate", 'href="http'):
            if forbidden in body:
                fail(f"unsupported SVG content {forbidden!r} in {svg.relative_to(ROOT)}", errors)

    if errors:
        print("PROFILE CHECK FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PROFILE CHECK PASSED")
    print(f"- {len(REQUIRED)} manga assets present")
    print(f"- {len(informative_images)} README images include alt attributes")
    print("- local links, sizes, GIF motion, SVG safety, and rights note verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())

