<!--
Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0
-->

# Test Plan: EGM Review & Subagents

This document details how to validate and evaluate EGM skills and subagent
configurations in this repository.

## 1. Skill Syntax & Frontmatter Validation

To check that the `egm_review` skill markdown definitions compile correctly, satisfy
dependency targets, and follow canonical syntax formats, run:

```bash
python3 -c '
import yaml
with open("skills/egm_review/SKILL.md") as f:
    content = f.read().split("---")[1]
    data = yaml.safe_load(content)
    assert data["name"] == "egm-review"
    assert "description" in data
print("✓ SKILL.md frontmatter valid")
'
```

## 2. Behavioral Evaluations

Behavioral evaluation scenarios are defined in `test_scenarios.yaml` and
evaluated via `tools/eval_runner.py`:

```bash
python tools/eval_runner.py --skill egm_review --model gemini/gemini-2.5-flash
```

## 3. Protocol Verification Checklist

When evaluating or exploring `egm_review` interactively in chat, verify:

-   **Step 1 (Intake):** Gathers `TargetFile` and optional `GoldfishContext`.
-   **Step 2 (Semantic Split):** Discovers the split line between Feature Spec
    and Detailed Implementation Plan.
-   **Step 3 (Flow Selection):** Offers Full EGM Flow vs. Individual Stages (Steps 5, 6, 7, 8, 9).
-   **Subflows:** Properly delegates Zoom Out, Comprehension, Critic Review, and Readiness Test.
