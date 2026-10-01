<!--
Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0
-->

## Contribution Type

Please select the track that matches this pull request:

- [ ] **Bug Fix / Minor Patch** (Targeted fix, non-test diff <= 100 lines and < 3 core files in `skills/`, `personas/`, `rules/`; no design doc required)
- [ ] **Feature / Architectural Change -- Stage 1: Design Doc PR** (`Refs #___` with `status: approved-for-design` | Adds `docs/designs/<name>.md` and updates `docs/designs/README.md`; use `Refs` instead of `Closes` so the issue stays open for Stage 2)
- [ ] **Feature / Architectural Change -- Stage 2: Implementation PR** (`Closes #___` with `status: approved-for-pr` | Implements merged `docs/designs/<name>.md`)

## Summary of Key Changes

List all key changes made in this pull request and why:

<!-- Describe each key change and its motivation here. -->

## Human Accountability Affirmation

- [ ] I am a human contributor. I have personally reviewed, understood, and can explain every line of this change in review (using AI tools to write code is welcome, but human understanding of the submitted change is required).

## Verification

- [ ] **For Design Doc PRs (Stage 1)**: Executed `/egm-review docs/designs/<name>.md`, resolved findings via `/goldfish-review-resolve`, and verified relative links (`pytest tests/unit/test_link_integrity.py`).
- [ ] **For Bug Fix / Implementation PRs (Stage 2)**: Unit tests or `test_scenarios.yaml` added/updated and `pytest tests/unit` executed.
