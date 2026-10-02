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
