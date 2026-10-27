# Naruto–Hinata Manga Profile Design

## Intent

Transform Aryan Kumar's GitHub profile from the existing galaxy theme into a vertically scrolling manga chapter built around Naruto and Hinata's relationship. The profile must still work first as a developer storefront: visitors should understand who Aryan is, see his strongest projects, and reach a live project within seconds.

## Experience

The README reads from top to bottom like a compact manga chapter:

1. **Opening panel — Welcome:** Adult Naruto reaches toward the visitor while Hinata welcomes them into Aryan's developer workspace. The hero carries Aryan's name, one-line positioning, and the primary DIPC action.
2. **Chapter one — The journey:** A black-and-white manga panel frames Aryan's identity around perseverance, thoughtful building, and turning ideas into useful experiences.
3. **Chapter two — Training record:** Skills appear as disciplined areas of practice, not a badge wall. Naruto represents drive; Hinata represents craft and care.
4. **Chapter three — Missions:** DIPC, The Dentist, Mathrubhumi Enterprises, and Portfolio Demos remain the substantive center of the profile. Each receives a short outcome-focused pitch and direct link.
5. **Final panel — Together:** Naruto and Hinata close the chapter beside a collaboration invitation and DIPC call to action.

Animated ink-swipe/page-turn GIF dividers connect the chapters so the page feels like a panel transition while scrolling. The motion is decorative and must not carry essential information.

## Visual Direction

- Recognizable adult Naruto Uzumaki and Hinata Hyuga in newly generated fan art.
- Original compositions only; no copied screenshots, manga scans, official logos, or studio watermarks.
- Palette: manga paper `#F4E9D8`, ink `#111111`, Naruto orange `#F47A1F`, Hinata lavender `#8C73C7`, and restrained crimson accents.
- Full-width assets share one consistent 900px design canvas and responsive `width="100%"` rendering.
- Manga conventions: panel borders, halftone dots, speed lines, torn edges, sound-effect typography, chapter labels, and speech bubbles.
- The theme should feel romantic and cinematic without turning Aryan's developer profile into a plot summary or fan wiki.

## Content

- Primary identity: **Aryan Kumar — Builder of interactive web experiences, AI automation, bots, and games.**
- Primary CTA: DIPC live experience.
- Secondary CTA: repositories and DEV profile.
- Existing four featured projects and their accurate stacks remain present.
- Existing automated GitHub telemetry remains functional but is restyled as a manga training record.
- Include a small footer note: “Unofficial fan-made profile artwork. Naruto and related characters belong to their respective rights holders.”

## GitHub Constraints

- README content is Markdown plus GitHub-safe HTML only.
- No JavaScript, interactive scrolling, external image APIs, or animation required for comprehension.
- Use repository-owned PNG, GIF, and static SVG assets so the profile does not depend on third-party uptime.
- Every image has useful alt text; decorative transitions use empty alt text.
- Desktop and mobile layouts must both be legible, with a dedicated mobile telemetry asset where needed.
- GIFs must be optimized for reasonable repository weight and should avoid rapid flashing.

## Non-goals

- Recreating the full Naruto–Hinata canon story.
- Copying official anime frames or manga panels.
- Hiding project substance behind decorative art.
- Adding new external services or dependencies.

## Success Criteria

- The public profile immediately reads as a manga/anime experience.
- Aryan's name, craft, and primary CTA are visible above the fold.
- All four featured projects remain easy to scan and open.
- Artwork and transitions render on GitHub desktop and mobile.
- The daily telemetry workflow still succeeds.

