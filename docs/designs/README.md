<!--
Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0
-->

# EGM Design Specifications

This directory contains the canonical technical design specifications defining
the Elephant & Goldfish Model (EGM) framework, skills, reviewer personas, and
operational guardrails.

| Document | Author | Primary Component |
| :------- | :----- | :---------------- |
| [architecture.md](architecture.md)<br>System architecture of the EGM framework covering component models, end-to-end dataflow, and agent lifecycle. | [@quinnjim](https://github.com/quinnjim), [@eewing314](https://github.com/eewing314) | [EGM Framework Architecture](../../README.md) |
| [brainstorm.md](brainstorm.md)<br>Fast zero-doc ideation tool using a 6-lens Goldfish swarm to audit and stress-test early concepts before drafting. | [@briansuchy](https://github.com/briansuchy) | [`egm_brainstorm`](../../skills/egm_brainstorm/SKILL.md) |
| [draft.md](draft.md)<br>Iterative section-by-section specification drafting protocol and semantic boundary definitions. | [@quinnjim](https://github.com/quinnjim), [@eewing314](https://github.com/eewing314) | [`egm_draft`](../../skills/egm_draft/SKILL.md) |
| [drift_report.md](drift_report.md)<br>Automated scanner to detect and report divergence between checked-in design specifications and live codebase implementations. | [@quinnjim](https://github.com/quinnjim) | [`egm_drift_report`](../../skills/egm_drift_report/SKILL.md) |
| [bootstrap.md](bootstrap.md)<br>Bottom-up recursive bootstrapping and sentinel-block upserting of documentation across package and repository trees. | [@briansuchy](https://github.com/briansuchy) | [`egm_bootstrap`](../../skills/egm_bootstrap/SKILL.md) |
| [review.md](review.md)<br>Multi-stage verification protocol and automated resolution engine using isolated Goldfish reviewer personas. | [@tearseb](https://github.com/tearseb), [@briansuchy](https://github.com/briansuchy) | [`egm_review`](../../skills/egm_review/SKILL.md) |
| [rules.md](rules.md)<br>Persistent behavioral, anti-sycophancy, link hygiene, and formatting constraints injected across agent sessions. | [@quinnjim](https://github.com/quinnjim) | [`rules/`](../../rules/) |
| [synthesizer.md](synthesizer.md)<br>Intermediate orchestration subagent to coordinate swarm fan-out, deduplicate critiques, and normalize link citations. | [@briansuchy](https://github.com/briansuchy) | [`synthesizer`](../../personas/synthesizer.md) |
| [oss_testing_architecture.md](oss_testing_architecture.md)<br>Two-tiered static verification (`pytest`) and provider-agnostic LiteLLM behavioral evaluation architecture. | [@eewing314](https://github.com/eewing314) | [Testing & Evaluation](../../TESTING.md) |
| [oss_pr_triage_governance.md](oss_pr_triage_governance.md)<br>Open-source PR triage, contributor speed bumps, two-stage design alignment, and automated scope advisory architecture. | [@briansuchy](https://github.com/briansuchy) | [Contribution Governance](../../CONTRIBUTING.md) |
