# Naruto–Hinata Manga Profile Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace Aryan Kumar's galaxy-themed GitHub profile with a responsive Naruto–Hinata manga chapter that preserves clear project discovery and live telemetry.

**Architecture:** The README remains a single GitHub-safe document backed entirely by repository-owned assets. ImageGen supplies original fan-art PNG panels; `scripts/build_manga_assets.py` generates optimized decorative GIF/SVG elements, while the existing telemetry updater is restyled without changing its data contract.

**Tech Stack:** GitHub Markdown/HTML, PNG/GIF/SVG, Python 3 + Pillow, GitHub Actions

**Spec:** `docs/superpowers/specs/2026-10-27-naruto-hinata-manga-profile-design.md`

## Global Constraints

- No JavaScript, remote widget services, copied screenshots, manga scans, official logos, or studio watermarks.
- All full-width art uses a 900px design canvas and renders with `width="100%"`.
- Motion is decorative, non-flashing, and never required to understand content.
- Every informative image has useful alt text; decorative dividers have empty alt text.
- Preserve the four featured projects, their links, and the existing daily telemetry workflow.
- Include the approved unofficial fan-art rights note in the footer.

## Review Focus

- GitHub image proxy behavior: every referenced asset must render without scripts, external resources, or unsupported SVG features.
- Mobile cropping: character faces, Aryan's name, and the primary CTA remain visible at narrow widths.
- Accessibility: meaningful alt text and readable Markdown preserve the profile when images or animation are unavailable.
- Repository weight: generated artwork and GIF dividers remain practical to clone and load.
- Workflow stability: scheduled telemetry regeneration changes only intended SVG files and remains idempotent.

---

### Task 1: Final Fan-Art Asset Set

**Files:**
- Create: `assets/manga/hero.png`
- Create: `assets/manga/journey.png`
- Create: `assets/manga/training.png`
- Create: `assets/manga/finale.png`

**Interfaces:**
- Consumes: approved visual direction and ImageGen outputs
- Produces: four repository-owned 900px-wide PNG panels referenced by `README.md`

- [ ] **Step 1: Generate four original compositions**

Use built-in ImageGen for the approved Naruto–Hinata opening, journey, training, and finale scenes; preserve character recognition, manga framing, palette, and negative space for README copy.

- [ ] **Step 2: Validate the generated images**

Inspect every image for recognizable adult characters, clean hands/faces, no added characters, no copied frames, no logos, and no generated text.

- [ ] **Step 3: Place and optimize the selected assets**

Copy the selected files into `assets/manga/` and optimize them without changing aspect ratio or visible quality.

- [ ] **Step 4: Verify dimensions and file sizes**

Run: `python scripts/verify_profile.py`

Expected: all required PNGs exist, are at least 900px wide, and each is below the configured size ceiling.

- [ ] **Step 5: Commit**

Commit message: `feat: add manga profile artwork`

### Task 2: GitHub-Safe Manga Motion and Validation

**Files:**
- Create: `scripts/build_manga_assets.py`
- Create: `scripts/verify_profile.py`
- Create: `assets/manga/ink-transition.gif`
- Create: `assets/manga/chapter-divider.svg`
- Create: `.gitignore`

**Interfaces:**
- Consumes: Pillow and the palette from the design spec
- Produces: `build_assets() -> None` and a validation CLI returning exit code `0` only for a complete profile asset set

- [ ] **Step 1: Write validation checks**

`scripts/verify_profile.py` checks required assets, README references, local-link targets, PNG width, per-file size ceilings, GIF frame count, alt text, and the fan-art footer note.

- [ ] **Step 2: Run validation to verify it fails**

Run: `python scripts/verify_profile.py`

Expected: FAIL because manga motion assets and README references are not complete.

- [ ] **Step 3: Implement deterministic motion generation**

`scripts/build_manga_assets.py` creates a non-flashing monochrome ink-swipe GIF and static chapter divider using only local drawing primitives.

- [ ] **Step 4: Ignore brainstorming artifacts**

Create `.gitignore` with `.superpowers/brainstorm/` so private mockups cannot be committed.

- [ ] **Step 5: Generate and inspect the assets**

Run: `python scripts/build_manga_assets.py`

Expected: both outputs are created deterministically under `assets/manga/`.

- [ ] **Step 6: Commit**

Commit message: `feat: add manga transition assets`

### Task 3: Manga Chapter README

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: all Task 1 and Task 2 assets plus existing project URLs
- Produces: the complete public profile narrative and CTA hierarchy

- [ ] **Step 1: Replace the hero and opening copy**

Use `assets/manga/hero.png`, Aryan's approved positioning line, and direct DIPC/repository/DEV actions above the first transition.

- [ ] **Step 2: Build the vertical chapter sequence**

Add Journey, Training Record, Missions, and Together sections with manga chapter labels, generated panels, decorative transition GIFs, and concise accessible Markdown fallbacks.

- [ ] **Step 3: Preserve project substance**

Keep DIPC, The Dentist, Mathrubhumi Enterprises, and Portfolio Demos with accurate outcome-focused descriptions, stacks, and direct links.

- [ ] **Step 4: Add the rights note and collaboration ending**

Close with the DIPC CTA and the exact unofficial fan-art note from the spec.

- [ ] **Step 5: Run validation**

Run: `python scripts/verify_profile.py`

Expected: PASS for links, assets, dimensions, file sizes, animation, alt text, and footer note.

- [ ] **Step 6: Commit**

Commit message: `feat: transform profile into manga chapter`

### Task 4: Restyled Live Telemetry

**Files:**
- Modify: `scripts/update_profile_assets.py`
- Modify: `assets/mission-control.svg`
- Modify: `assets/mission-control-mobile.svg`

**Interfaces:**
- Consumes: the existing GitHub API response contract and scheduled workflow
- Produces: manga-styled desktop/mobile training-record SVGs at the existing paths

- [ ] **Step 1: Preserve the telemetry data contract**

Keep API endpoints, repository aggregation, output paths, and fallback behavior unchanged while replacing only visual markup and copy.

- [ ] **Step 2: Generate both variants locally**

Run: `python scripts/update_profile_assets.py`

Expected: desktop and mobile SVGs are regenerated without exceptions.

- [ ] **Step 3: Validate static SVG compatibility**

Run: `python scripts/verify_profile.py`

Expected: PASS with no scripts, external images, foreign objects, unsupported animations, or missing fallback text.

- [ ] **Step 4: Run generation twice**

Run the updater twice with unchanged inputs.

Expected: the second run produces no unintended structural diff beyond permitted timestamp/data changes.

- [ ] **Step 5: Commit**

Commit message: `feat: restyle telemetry as training record`

### Task 5: Publish and Public Verification

**Files:**
- Verify: `.github/workflows/update-profile.yml`
- Verify: all README-linked assets

**Interfaces:**
- Consumes: Tasks 1–4 committed on the profile repository's default branch
- Produces: a publicly rendered GitHub profile and a successful scheduled workflow run

- [ ] **Step 1: Run repository checks**

Run: `python scripts/verify_profile.py` and `git diff --check`

Expected: both exit successfully and `git status --short` lists only intended changes before commit.

- [ ] **Step 2: Push the committed profile**

Push the default branch to `Aryan170911/Aryan170911`.

- [ ] **Step 3: Verify the public desktop profile**

Open `https://github.com/Aryan170911` and confirm the hero, chapter flow, links, telemetry, and finale render.

- [ ] **Step 4: Verify the narrow layout**

Inspect the profile at a mobile-sized viewport and confirm no critical crop or unreadable copy.

- [ ] **Step 5: Trigger and verify the telemetry workflow**

Run the workflow manually and confirm the completed job succeeds without changing unrelated files.

