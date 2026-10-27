"""Generate self-hosted manga profile telemetry from public GitHub data."""

from __future__ import annotations

import html
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen


USERNAME = "Aryan170911"
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
PAPER = "#f4e9d8"
INK = "#111111"
ORANGE = "#f47a1f"
LAVENDER = "#8c73c7"


def github_json(path: str):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{USERNAME}-profile-builder",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"https://api.github.com{path}", headers=headers)
    with urlopen(request, timeout=20) as response:
        return json.load(response)


def svg_escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def card_cell(x: int, label: str, value: str, accent: str) -> str:
    return f'''
      <g transform="translate({x} 98)">
        <rect width="258" height="108" rx="4" fill="#fffaf0" stroke="{INK}" stroke-width="3"/>
        <path d="M0 12 L12 0 M246 108 L258 96" stroke="{accent}" stroke-width="5"/>
        <circle cx="24" cy="25" r="5" fill="{accent}"/>
        <text x="39" y="31" class="label">{svg_escape(label)}</text>
        <text x="22" y="77" class="value" fill="{INK}">{svg_escape(value)}</text>
      </g>'''


def mobile_card_cell(x: int, y: int, label: str, value: str, accent: str) -> str:
    return f'''
      <g transform="translate({x} {y})">
        <rect width="258" height="140" rx="4" fill="#fffaf0" stroke="{INK}" stroke-width="3"/>
        <path d="M0 12 L12 0 M246 140 L258 128" stroke="{accent}" stroke-width="5"/>
        <circle cx="22" cy="27" r="5" fill="{accent}"/>
        <text x="37" y="33" class="label">{svg_escape(label)}</text>
        <text x="20" y="91" class="value" fill="{INK}">{svg_escape(value)}</text>
      </g>'''


def write_mission_control(repos: list[dict]) -> None:
    originals = [repo for repo in repos if not repo.get("fork") and repo["name"] != USERNAME]
    languages = sorted({repo["language"] for repo in originals if repo.get("language")})
    latest = next((repo for repo in originals if repo.get("pushed_at")), None)
    latest_name = (latest["name"].replace("-", " ") if latest else "IN TRAINING")[:18].upper()

    cells = "".join(
        (
            card_cell(42, "PUBLIC MISSIONS", str(len(originals)), ORANGE),
            card_cell(328, "CORE TECHNIQUES", str(len(languages)), LAVENDER),
            card_cell(614, "LATEST SCROLL", latest_name, ORANGE),
            card_cell(900, "S-RANK FLAGSHIP", "DIPC", LAVENDER),
        )
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="245" viewBox="0 0 1200 245" role="img" aria-labelledby="title desc">
  <title id="title">Aryan Kumar manga training record</title>
  <desc id="desc">Live summary of public missions, core techniques, latest scroll, and flagship project.</desc>
  <defs>
    <pattern id="dots" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="{INK}" opacity=".13"/></pattern>
  </defs>
  <style>
    .eyebrow {{ font: 800 13px Arial,sans-serif; letter-spacing:4px; fill:{LAVENDER} }}
    .heading {{ font: 900 27px 'Arial Black',Impact,sans-serif; letter-spacing:1px; fill:{INK} }}
    .label {{ font: 700 12px Consolas,monospace; letter-spacing:1.2px; fill:#5a5148 }}
    .value {{ font: 900 22px 'Arial Black',Arial,sans-serif; letter-spacing:.3px }}
  </style>
  <rect x="1" y="1" width="1198" height="243" rx="12" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>
  <rect x="1" y="1" width="1198" height="243" rx="12" fill="url(#dots)"/>
  <path d="M24 68 H1176" stroke="{INK}" stroke-width="4"/><path d="M24 75 H1176" stroke="{ORANGE}" stroke-width="2"/>
  <text x="42" y="31" class="eyebrow">LIVE FROM GITHUB</text>
  <text x="42" y="61" class="heading">TRAINING RECORD</text>
  <text x="1160" y="52" text-anchor="end" font-family="Georgia,serif" font-size="44" font-weight="700" fill="{INK}" opacity=".18">忍</text>
  {cells}
</svg>'''
    (ASSETS / "mission-control.svg").write_text(svg, encoding="utf-8")

    mobile_cells = "".join(
        (
            mobile_card_cell(28, 104, "PUBLIC MISSIONS", str(len(originals)), ORANGE),
            mobile_card_cell(314, 104, "CORE TECHNIQUES", str(len(languages)), LAVENDER),
            mobile_card_cell(28, 272, "LATEST SCROLL", latest_name, ORANGE),
            mobile_card_cell(314, 272, "S-RANK FLAGSHIP", "DIPC", LAVENDER),
        )
    )
    mobile_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="455" viewBox="0 0 600 455" role="img" aria-labelledby="title desc">
  <title id="title">Aryan Kumar manga training record</title>
  <desc id="desc">Mobile summary of public missions, core techniques, latest scroll, and flagship project.</desc>
  <defs><pattern id="dots" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="{INK}" opacity=".13"/></pattern></defs>
  <style>
    .eyebrow {{ font:800 12px Arial,sans-serif; letter-spacing:3px; fill:{LAVENDER} }}
    .heading {{ font:900 25px 'Arial Black',Impact,sans-serif; fill:{INK} }}
    .label {{ font:700 12px Consolas,monospace; letter-spacing:1px; fill:#5a5148 }}
    .value {{ font:900 22px 'Arial Black',Arial,sans-serif }}
  </style>
  <rect x="1" y="1" width="598" height="453" rx="12" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>
  <rect x="1" y="1" width="598" height="453" rx="12" fill="url(#dots)"/>
  <path d="M24 78 H576" stroke="{INK}" stroke-width="4"/><path d="M24 85 H576" stroke="{ORANGE}" stroke-width="2"/>
  <text x="28" y="34" class="eyebrow">LIVE FROM GITHUB</text>
  <text x="28" y="68" class="heading">TRAINING RECORD</text>
  {mobile_cells}
</svg>'''
    (ASSETS / "mission-control-mobile.svg").write_text(mobile_svg, encoding="utf-8")


def write_button(filename: str, label: str, width: int, accent: str) -> None:
    safe = svg_escape(label)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="46" viewBox="0 0 {width} 46" role="img" aria-label="{safe}">
  <rect x="2" y="2" width="{width - 4}" height="42" rx="5" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>
  <path d="M2 12 L12 2 M{width - 12} 44 L{width - 2} 34" stroke="{accent}" stroke-width="5"/>
  <circle cx="22" cy="23" r="5" fill="{accent}"/>
  <text x="{width / 2 + 8}" y="29" text-anchor="middle" font-family="Arial Black,Arial,sans-serif" font-size="13" font-weight="900" letter-spacing=".8" fill="{INK}">{safe}</text>
</svg>'''
    (ASSETS / filename).write_text(svg, encoding="utf-8")


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    repos = github_json(f"/users/{USERNAME}/repos?per_page=100&type=owner&sort=pushed")
    write_mission_control(repos)
    write_button("cta-dipc.svg", "LAUNCH DIPC  ↗", 190, ORANGE)
    write_button("cta-work.svg", "EXPLORE MY WORK  ↗", 220, LAVENDER)
    write_button("cta-dev.svg", "FOLLOW ON DEV  ↗", 190, ORANGE)
    write_button("cta-build.svg", "BUILD WITH DIPC  ↗", 220, LAVENDER)


if __name__ == "__main__":
    main()

