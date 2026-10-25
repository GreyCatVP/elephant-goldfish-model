# Shared skill icons

Status: Draft implementation proposal. Maintainer scope approval is pending.
Author: @n3wth. Date: 2026-10-25.

## Purpose and scope

Use the same seven skill marks in plugin pickers, the README, and egm.dev.
The approved artwork uses familiar silhouettes with two color facets. This
change replaces the existing skill artwork; it does not change skill behavior,
reviewer permissions, installation, or the Elephant-Goldfish logo.

## Source and geometry

Each `skills/egm_*/assets/icon.svg` is the canonical asset. Keep the SVGs
self-contained, with a title and a 24 by 24 viewBox. Visible ink stays inside
the 20 px keyline. Optical size and positioning corrections are part of the
artwork; do not normalize individual bounding boxes or stroke widths.

| Skill | Mark | Base / facet |
| --- | --- | --- |
| Bootstrap | Rounded plus: initialize project documentation | `#1b6ef3` / `#7cacf8` |
| Brainstorm | Lightbulb: explore ideas | `#1b6ef3` / `#7cacf8` |
| Draft | Pencil: write the design | `#1b6ef3` / `#7cacf8` |
| Resolve | Check: address review findings | `#1b6ef3` / `#7cacf8` |
| Drift report | Touching, offset halves: document and code diverge | `#e86e00` / `#ff8d41` |
| Review | Magnifier: inspect the document | `#e86e00` / `#ff8d41` |
| Review loop | Circular arrow: repeat review | `#e86e00` / `#ff8d41` |

## Consumers

- Codex metadata continues to point both icon fields at `./assets/icon.svg`.
  Its `brand_color` matches the icon's base color. Host rendering is controlled
  by the host; metadata validation does not verify its picker UI.
- Both runtime bundles include the canonical files through the existing
  [package builder](../../scripts/pack_plugin.py). Regenerate
  `distributions/claude`; do not edit its copies independently. Claude's
  reviewer color keywords and the plugin-level logo stay unchanged.
- The root README references the canonical paths directly. These relative
  paths also resolve inside generated runtime packages.
- The site imports the canonical SVGs at build time. A shared `SkillIcon`
  component renders a 28 px glyph in a 40 px neutral circle using the site's
  surface tokens. Circles are presentation, not baked into the asset.
  Keep adjacent skill names and empty image alt text to avoid duplicate
  announcements. Brainstorm, Draft, and Review form the three-step sequence;
  a sentence below it explains the handoff to implementation after approval.
- The site workflow watches canonical SVG changes as well as `site/` changes.

## Verification and rollout

Check metadata colors and SVG structure, runtime byte equality, README image
inclusion, Astro type checking and production build. Inspect desktop and
mobile layouts in both color schemes and refresh committed site captures.
All seven marks must remain legible beside their labels.

This proposal builds on runtime-packaging PR #136. Its draft status does not
claim an approved issue, a merged design, or a completed native-host workflow
test. Obtain maintainer agreement on the contribution track before merge.
