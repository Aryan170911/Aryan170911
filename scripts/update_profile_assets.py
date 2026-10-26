"""Generate self-hosted profile visuals from public GitHub data.

The script uses only Python's standard library so the scheduled workflow has no
package-install step and no third-party statistics service.
"""

from __future__ import annotations

import html
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen


USERNAME = "Aryan170911"
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


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
    return f"""
      <g transform="translate({x} 92)">
        <rect width="258" height="112" rx="18" fill="#0b1228" stroke="#22325e" />
        <circle cx="24" cy="25" r="5" fill="{accent}" />
        <text x="39" y="31" class="label">{svg_escape(label)}</text>
        <text x="22" y="75" class="value" fill="{accent}">{svg_escape(value)}</text>
      </g>"""


def write_mission_control(repos: list[dict]) -> None:
    originals = [repo for repo in repos if not repo.get("fork") and repo["name"] != USERNAME]
    languages = sorted({repo["language"] for repo in originals if repo.get("language")})
    latest = next((repo for repo in originals if repo.get("pushed_at")), None)
    latest_name = latest["name"].replace("-", " ") if latest else "IN ORBIT"
    latest_name = latest_name[:18].upper()

    cells = "".join(
        (
            card_cell(42, "PUBLIC BUILDS", str(len(originals)), "#22d3ee"),
            card_cell(328, "CORE LANGUAGES", str(len(languages)), "#a78bfa"),
            card_cell(614, "LATEST LAUNCH", latest_name, "#60a5fa"),
            card_cell(900, "FLAGSHIP", "DIPC", "#c084fc"),
        )
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="245" viewBox="0 0 1200 245" role="img" aria-labelledby="title desc">
  <title id="title">Aryan Kumar mission control</title>
  <desc id="desc">Live summary of public builds, core languages, latest launch, and flagship project.</desc>
  <defs>
    <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="#050816"/><stop offset="0.55" stop-color="#0a1025"/><stop offset="1" stop-color="#140b2d"/>
    </linearGradient>
    <linearGradient id="line" x1="0" x2="1"><stop stop-color="#22d3ee"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <style>
    .eyebrow {{ font: 600 14px 'Segoe UI',Arial,sans-serif; letter-spacing: 4px; fill:#8ea3c7 }}
    .heading {{ font: 700 24px 'Segoe UI',Arial,sans-serif; letter-spacing: 1px; fill:#eef7ff }}
    .label {{ font: 600 12px Consolas,monospace; letter-spacing: 1.4px; fill:#8ea3c7 }}
    .value {{ font: 700 22px 'Segoe UI',Arial,sans-serif; letter-spacing:.5px }}
  </style>
  <rect x="1" y="1" width="1198" height="243" rx="24" fill="url(#bg)" stroke="#26345f"/>
  <path d="M28 67 H1172" stroke="url(#line)" opacity=".7"/>
  <circle cx="1147" cy="35" r="4" fill="#22d3ee" filter="url(#glow)"/>
  <text x="42" y="35" class="eyebrow">LIVE TELEMETRY</text>
  <text x="42" y="63" class="heading">MISSION CONTROL</text>
  {cells}
</svg>
"""
    (ASSETS / "mission-control.svg").write_text(svg, encoding="utf-8")

    mobile_cells = "".join(
        (
            mobile_card_cell(28, 104, "PUBLIC BUILDS", str(len(originals)), "#22d3ee"),
            mobile_card_cell(314, 104, "CORE LANGUAGES", str(len(languages)), "#a78bfa"),
            mobile_card_cell(28, 272, "LATEST LAUNCH", latest_name, "#60a5fa"),
            mobile_card_cell(314, 272, "FLAGSHIP", "DIPC", "#c084fc"),
        )
    )
    mobile_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="600" height="455" viewBox="0 0 600 455" role="img" aria-labelledby="title desc">
  <title id="title">Aryan Kumar mission control</title>
  <desc id="desc">Mobile summary of public builds, core languages, latest launch, and flagship project.</desc>
  <defs>
    <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#050816"/><stop offset=".55" stop-color="#0a1025"/><stop offset="1" stop-color="#140b2d"/></linearGradient>
    <linearGradient id="line" x1="0" x2="1"><stop stop-color="#22d3ee"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient>
  </defs>
  <style>
    .eyebrow {{ font: 600 13px 'Segoe UI',Arial,sans-serif; letter-spacing: 3px; fill:#8ea3c7 }}
    .heading {{ font: 700 24px 'Segoe UI',Arial,sans-serif; letter-spacing: 1px; fill:#eef7ff }}
    .label {{ font: 600 12px Consolas,monospace; letter-spacing: 1px; fill:#8ea3c7 }}
    .value {{ font: 700 23px 'Segoe UI',Arial,sans-serif; letter-spacing:.4px }}
  </style>
  <rect x="1" y="1" width="598" height="453" rx="24" fill="url(#bg)" stroke="#26345f"/>
  <path d="M28 78 H572" stroke="url(#line)" opacity=".7"/>
  <circle cx="557" cy="37" r="4" fill="#22d3ee"/>
  <text x="28" y="34" class="eyebrow">LIVE TELEMETRY</text>
  <text x="28" y="67" class="heading">MISSION CONTROL</text>
  {mobile_cells}
</svg>
"""
    (ASSETS / "mission-control-mobile.svg").write_text(mobile_svg, encoding="utf-8")


def mobile_card_cell(x: int, y: int, label: str, value: str, accent: str) -> str:
    return f"""
      <g transform="translate({x} {y})">
        <rect width="258" height="140" rx="18" fill="#0b1228" stroke="#22325e" />
        <circle cx="22" cy="27" r="5" fill="{accent}" />
        <text x="37" y="33" class="label">{svg_escape(label)}</text>
        <text x="20" y="88" class="value" fill="{accent}">{svg_escape(value)}</text>
      </g>"""


def write_button(filename: str, label: str, width: int, color_a: str, color_b: str) -> None:
    safe = svg_escape(label)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="46" viewBox="0 0 {width} 46" role="img" aria-label="{safe}">
  <defs><linearGradient id="g" x1="0" x2="1"><stop stop-color="{color_a}"/><stop offset="1" stop-color="{color_b}"/></linearGradient></defs>
  <rect x="1" y="1" width="{width - 2}" height="44" rx="12" fill="#070b1b" stroke="url(#g)" stroke-width="2"/>
  <circle cx="23" cy="23" r="5" fill="{color_a}"/>
  <text x="{width / 2 + 7}" y="29" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="14" font-weight="700" letter-spacing="1.1" fill="#f4f8ff">{safe}</text>
</svg>
"""
    (ASSETS / filename).write_text(svg, encoding="utf-8")


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    repos = github_json(f"/users/{USERNAME}/repos?per_page=100&type=owner&sort=pushed")
    write_mission_control(repos)
    write_button("cta-dipc.svg", "LAUNCH DIPC  ↗", 190, "#22d3ee", "#3b82f6")
    write_button("cta-work.svg", "EXPLORE MY WORK  ↗", 220, "#60a5fa", "#8b5cf6")
    write_button("cta-dev.svg", "FOLLOW ON DEV  ↗", 190, "#8b5cf6", "#c084fc")
    write_button("cta-build.svg", "BUILD WITH DIPC  ↗", 220, "#22d3ee", "#8b5cf6")


if __name__ == "__main__":
    main()
