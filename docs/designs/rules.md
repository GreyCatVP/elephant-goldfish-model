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

# EGM Behavioral & Guardrails Architecture (Rules Layer)

*   **Author:** Jim Quinn ([@quinnjim](https://github.com/quinnjim))
*   **Status:** Current
*   **Date:** 2026-08-20

--------------------------------------------------------------------------------

## Overview

The Elephant & Goldfish Model (EGM) provides a dedicated **Rules Layer**
(`rules/`) that injects continuous behavioral and operational constraints into
coding agent sessions.

These rules govern agent cognition, inquiry, and output across three critical
domains:

1.  **Critical Thinking & Anti-Sycophancy** (`rules/anti_sycophancy.md`)
2.  **Symbolic Search Query Robustness** (`rules/search_terms.md`)
3.  **Pull Request Categorization & Tagging** (`rules/pr_tagging.md`)

This document specifies the purpose, mechanics, and architectural rationale for
each rule.

## Runtime Integration & Prompt Injection

Rules are stored as modular markdown files under `rules/`. In supporting agent
runtimes, rules are loaded into the active agent context or inherited by
subagents:

1.  **Direct Prompt Injection**: Rules are configured into the system prompt or
    injected via Antigravity workspace instructions, agent profiles, or
    framework rule registries.
2.  **Swarm Inheritance**: When orchestrators spawn subagents or review
    swarms, subagent contexts inherit behavioral constraints, ensuring
    consistent adversarial rigor across all worker nodes.
3.  **Conditionality**: Rules can apply globally (e.g., anti-sycophancy) or be
    triggered conditionally based on active workflows (e.g., PR creation).

## Implementation Files

The EGM behavioral guardrails are implemented across the following rule files:

| File Path | Type | Purpose & Reason for Existence |
| :-------- | :--- | :----------------------------- |
| `rules/anti_sycophancy.md` | Cognitive Rule | Mandates adversarial stress-testing, critique-first feedback, and eliminates hollow flattery. |
| `rules/search_terms.md` | Code Navigation Rule | Enforces symbol-based code search queries over fragile line numbers. |
| `rules/pr_tagging.md` | VCS Tagging Rule | Enforces `#egm` hashtag categorization in pull request descriptions for changes implementing EGM specifications. |

## References

*   Dave Rensin, [Elephants, Goldfish, and the New Golden Age of Software Engineering](https://medium.com/@drensin/elephants-goldfish-and-the-new-golden-age-of-software-engineering-c33641a48874) (Medium, 2026).
