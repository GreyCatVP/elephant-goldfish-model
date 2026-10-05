<!--
Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0
-->

# Test Plan: Goldfish Review Loop Skill

This document details how to validate and evaluate the `egm_review_loop` skill.

## 1. Skill Syntax & Frontmatter Validation

To check that the `egm_review_loop` skill markdown definitions conform to canonical formatting rules, run:

```bash
python3 -c '
import yaml
with open("skills/egm_review_loop/SKILL.md") as f:
    content = f.read().split("---")[1]
    data = yaml.safe_load(content)
    assert data["name"] == "egm-review-loop"
    assert "description" in data
print("✓ SKILL.md frontmatter valid")
'
```

## 2. Behavioral Evaluations

Behavioral evaluation scenarios are defined in `test_scenarios.yaml` and
evaluated via `tools/eval_runner.py`:

```bash
python tools/eval_runner.py --skill egm_review_loop --model gemini/gemini-2.5-flash
```

## 3. Protocol Verification Checklist

When evaluating or exploring `egm_review_loop` interactively in chat, verify:

-   **Step 1 (Intake & Config):** Validates required inputs and resolves standard paths.
-   **Step 2.1 (Target Resolution):** Unconditionally re-scans line numbers before auditing.
-   **Step 2.2 (Review Swarm):** Spawns subagents (or sequentially iterates personas in degraded mode) across requested standards.
-   **Step 2.3 & 2.4 (Resolve Handoff & Turn Boundary):** Hands findings to `egm-resolve` and respects human decision gates.
