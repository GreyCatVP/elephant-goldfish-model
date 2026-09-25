<!--
Copyright 2026 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Contributing to the Elephant & Goldfish Model (EGM)

We welcome contributions! We all benefit when new ideas, skills, and reviewer
perspectives are shared across the open-source community.

## Design Principles

These general principles guide development of the EGM framework:

*   **Humans Own the Outcomes**: AI is an exploration and review partner, but
    human engineers remain responsible for all design decisions and code.
*   **Artifact-First UX**: Large proposals, drafts, and reviews belong in
    dedicated files, not dumped into chat streams.
*   **Living Specifications**: Code and design specifications must evolve
    together.

## Contribution Workflow

Any non-trivial feature, new skill, or architectural change should follow the
EGM Spec-Driven Development process:

1.  **Discuss & Ideate**:
    Start by framing the problem using `/egm-brainstorm` or `/egm-discuss`.
    Align on goals, constraints, non-goals, and alternatives before writing code.

2.  **Draft Design Specification**:
    Draft a technical design specification under `docs/designs/<feature>.md`
    using `/egm-draft`.

3.  **Goldfish Review**:
    Run `/egm-review docs/designs/<feature>.md` to stress-test your proposal
    against the EGM document standards. Triage and resolve findings using
    `/goldfish-review-resolve`.

4.  **Open a Pull Request**:
    Submit your proposed design specification in a PR. Tag the PR description
    with `#egm`.

5.  **Implement against the Spec**:
    Once the specification is merged or approved, implement code following the
    detailed execution plan.

## Automated Validation & Testing

*   **Skill Definitions**: Ensure all `SKILL.md` files contain valid YAML
    frontmatter (`name`, `description`, `inputs`).
*   **Evaluation Suites**: New skills must include a co-located behavioral
    evaluation suite in `skills/<skill_name>/test_scenarios.yaml` and
    verification instructions in `skills/<skill_name>/TEST.md`. See
    [TESTING.md](TESTING.md) for running Tier 1 static checks (`pytest tests/unit`)
    and Tier 2 behavioral evaluations (`python tools/eval_runner.py`).
*   **Formatting**: Format markdown files cleanly using standard formatters
    (e.g., Prettier or markdownlint).

## Contributor License Agreement (CLA)

Contributions to this project must be accompanied by a
[Contributor License Agreement](https://cla.developers.google.com/about) (CLA).
You (or your employer) retain the copyright to your contribution; this simply
gives us permission to use and redistribute your contributions as part of the
project.

If you or your current employer have already signed the Google CLA (even if it
was for a different project), you probably don't need to do it again.

Visit <https://cla.developers.google.com/> to see your current agreements or to
sign a new one.

## Community Guidelines

This project follows
[Google's Open Source Community Guidelines](https://opensource.google/conduct/).
