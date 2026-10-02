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

# Test Plan: Goldfish Review Resolve Skill

This document details how to validate and evaluate the `egm_resolve` skill.

## 1. Skill Syntax & Frontmatter Validation

To check that the `egm_resolve` skill markdown definitions conform to canonical formatting rules, run:

```bash
python3 -c '
import yaml
with open("skills/egm_resolve/SKILL.md") as f:
    content = f.read().split("---")[1]
    data = yaml.safe_load(content)
    assert data["name"] == "egm-resolve"
    assert "description" in data
print("✓ SKILL.md frontmatter valid")
'
```

## 2. Behavioral Evaluations

Behavioral evaluation scenarios are defined in `test_scenarios.yaml` and
evaluated via `tools/eval_runner.py`:

```bash
python tools/eval_runner.py --skill egm_resolve --model gemini/gemini-2.5-flash
```

## 3. Protocol Verification Checklist

When evaluating or exploring `egm_resolve` interactively in chat, verify:

-   **Step 1 (Intake & Context):** Ingests `TargetFile`, `LineRange`, and `FindingsList`.
-   **Step 2 (Evaluate & Categorize):** Defends valid design choices (`CONTEST`) and drafts concrete repairs (`PROPOSE FIX`).
-   **Step 3 (Report Fixes):** Generates `goldfish_review_report.md` artifact.
-   **Step 4 (Resolution Gate):** Prompts the user with clear decision choices (Auto accept, Continue, Interactive breakdown) without modal popups, and executes approved file modifications.
