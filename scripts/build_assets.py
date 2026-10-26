"""Build the animated galaxy assets used by the profile README."""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SOURCE = ASSETS / "galaxy-source.png"
WIDTH, HEIGHT = 1200, 400
FRAMES = 30


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


TITLE_FONT = font("C:/Windows/Fonts/bahnschrift.ttf", 78)
SUBTITLE_FONT = font("C:/Windows/Fonts/segoeuib.ttf", 25)
META_FONT = font("C:/Windows/Fonts/consolab.ttf", 17)


def cover_crop(image: Image.Image, width: int, height: int) -> Image.Image:
    scale = max(width / image.width, height / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - width) // 2
    top = (resized.height - height) // 2
    return resized.crop((left, top, left + width, top + height))


def centered(draw: ImageDraw.ImageDraw, text: str, y: int, used_font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=used_font)
    return (WIDTH - (box[2] - box[0])) // 2, y


def glow_text(canvas: Image.Image, text: str, y: int, used_font: ImageFont.FreeTypeFont) -> None:
    glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    x, _ = centered(glow_draw, text, y, used_font)
    glow_draw.text((x, y), text, font=used_font, fill=(45, 220, 255, 230), stroke_width=2)
    canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(12)))
    canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(4)))
    draw = ImageDraw.Draw(canvas)
    draw.text(
        (x, y),
        text,
        font=used_font,
        fill=(239, 249, 255, 255),
        stroke_width=1,
        stroke_fill=(115, 90, 255, 255),
    )


def make_frame(base: Image.Image, index: int, stars: list[tuple[int, int, int, int]]) -> Image.Image:
    phase = index / FRAMES
    drift_x = round(8 * math.sin(phase * math.tau))
    drift_y = round(3 * math.cos(phase * math.tau))
    enlarged = base.resize((WIDTH + 24, HEIGHT + 12), Image.Resampling.LANCZOS)
    frame = enlarged.crop((12 + drift_x, 6 + drift_y, 12 + drift_x + WIDTH, 6 + drift_y + HEIGHT))
    frame = ImageEnhance.Contrast(frame).enhance(1.08).convert("RGBA")

    shade = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    shade_draw = ImageDraw.Draw(shade)
    for y in range(HEIGHT):
        center_weight = 1 - abs((y / HEIGHT) - 0.46) * 1.25
        alpha = int(max(0, center_weight) * 104)
        shade_draw.line((0, y, WIDTH, y), fill=(1, 5, 20, alpha))
    frame.alpha_composite(shade)

    star_layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    star_draw = ImageDraw.Draw(star_layer)
    for x, y, radius, offset in stars:
        pulse = (math.sin((phase + offset / 100) * math.tau) + 1) / 2
        alpha = int(55 + 190 * pulse)
        r = radius + (1 if pulse > 0.83 else 0)
        star_draw.ellipse((x - r, y - r, x + r, y + r), fill=(195, 239, 255, alpha))
    frame.alpha_composite(star_layer.filter(ImageFilter.GaussianBlur(0.6)))

    orbit = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    orbit_draw = ImageDraw.Draw(orbit)
    orbit_draw.arc((125, 95, 1075, 405), 196, 344, fill=(63, 210, 255, 80), width=2)
    orbit_draw.arc((90, 70, 1110, 430), 198, 342, fill=(143, 92, 246, 70), width=1)
    angle = math.radians(196 + phase * 148)
    dot_x = 600 + math.cos(angle) * 475
    dot_y = 250 + math.sin(angle) * 155
    orbit_draw.ellipse((dot_x - 5, dot_y - 5, dot_x + 5, dot_y + 5), fill=(158, 242, 255, 255))
    frame.alpha_composite(orbit.filter(ImageFilter.GaussianBlur(5)))
    frame.alpha_composite(orbit)

    glow_text(frame, "ARYAN KUMAR", 104, TITLE_FONT)
    draw = ImageDraw.Draw(frame)
    subtitle = "INTERACTIVE WEB  •  AI AUTOMATION  •  BOTS & GAMES"
    sx, _ = centered(draw, subtitle, 211, SUBTITLE_FONT)
    draw.text((sx, 211), subtitle, font=SUBTITLE_FONT, fill=(220, 233, 255, 245))

    label = "NEON FORGE  //  BUILDER BEHIND DIPC"
    label_box = draw.textbbox((0, 0), label, font=META_FONT)
    label_width = label_box[2] - label_box[0]
    left = (WIDTH - label_width) // 2 - 20
    top = 271
    draw.rounded_rectangle(
        (left, top, left + label_width + 40, top + 40),
        radius=20,
        fill=(4, 10, 28, 205),
        outline=(90, 194, 255, 195),
        width=1,
    )
    draw.text((left + 20, top + 10), label, font=META_FONT, fill=(201, 220, 255, 255))

    scan_x = int((phase * (WIDTH + 260)) - 130)
    scan = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    scan_draw = ImageDraw.Draw(scan)
    scan_draw.polygon(
        [(scan_x - 42, 0), (scan_x + 5, 0), (scan_x + 130, HEIGHT), (scan_x + 75, HEIGHT)],
        fill=(87, 202, 255, 20),
    )
    frame.alpha_composite(scan.filter(ImageFilter.GaussianBlur(12)))
    return frame.convert("RGB")


def build() -> None:
    source = Image.open(SOURCE).convert("RGB")
    base = cover_crop(source, WIDTH, HEIGHT)
    randomizer = random.Random(170911)
    stars = [
        (
            randomizer.randint(50, WIDTH - 50),
            randomizer.randint(25, 245),
            randomizer.choice((1, 1, 1, 2)),
            randomizer.randint(0, 99),
        )
        for _ in range(62)
    ]
    frames = [make_frame(base, index, stars) for index in range(FRAMES)]
    frames[0].save(ASSETS / "galaxy-header.png", optimize=True)
    paletted = [frame.quantize(colors=72, method=Image.Quantize.MEDIANCUT) for frame in frames]
    paletted[0].save(
        ASSETS / "galaxy-header.gif",
        save_all=True,
        append_images=paletted[1:],
        duration=130,
        loop=0,
        disposal=2,
        optimize=True,
    )


if __name__ == "__main__":
    build()
