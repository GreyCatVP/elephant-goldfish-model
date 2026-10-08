<!--
Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0
-->

<!-- Fill in every section; CI fails until the description matches this template. -->

## Related issue

<!--
Bug fixes need no issue. Stage 1 design doc PRs use "Refs #<issue>" so the issue
stays open for Stage 2. Stage 2 implementation PRs use "Closes #<issue>".
-->

None

## Contribution Type

<!-- Tick one. Scope rules are in CONTRIBUTING.md. -->

- [ ] **Bug Fix / Minor Patch**: targeted fix, non-test diff <= 100 lines and fewer than 3 core files in `skills/` or `agents/`; no design doc required.
- [ ] **Feature / Architectural Change -- Stage 1: Design Doc PR**: adds `docs/designs/<name>.md` and updates `docs/designs/README.md`; the linked issue has `status: approved-for-design`.
- [ ] **Feature / Architectural Change -- Stage 2: Implementation PR**: implements a merged `docs/designs/<name>.md`; the linked issue has `status: approved-for-pr`.

## Summary of Key Changes

<!-- What changed and why, one bullet per change; name the files to read first. -->

-

## Human Accountability Affirmation

<!-- Tick this yourself. AI tools may write the code; a human must own the change. -->

- [ ] I am a human contributor. I have personally reviewed, understood, and can explain every line of this change in review (using AI tools to write code is welcome, but human understanding of the submitted change is required).

## Verification

<!-- Tick the line that applies and note what you ran. -->

- [ ] Design doc PR (Stage 1): ran `/egm-review docs/designs/<name>.md`, resolved findings with `/egm-resolve`, and `pytest tests/unit/test_link_integrity.py` passes.
- [ ] Bug fix or implementation PR (Stage 2): unit tests or `test_scenarios.yaml` added or updated as needed, and `pytest tests/unit` passes.
