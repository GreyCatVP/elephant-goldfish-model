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

# Test Plan: EGM Brainstorm Skill

This document details how to validate and evaluate the `egm_brainstorm` skill.

## 1. Skill Syntax & Frontmatter Validation

To check that the `egm_brainstorm` skill markdown definitions conform to canonical formatting rules, run:

```bash
python3 -c '
import yaml
with open("skills/egm_brainstorm/SKILL.md") as f:
    content = f.read().split("---")[1]
    data = yaml.safe_load(content)
    assert data["name"] == "egm-brainstorm"
    assert "description" in data
print("✓ SKILL.md frontmatter valid")
'
```

## 2. Automated Evaluations

To verify multi-lens ideation, open-ended problem drilling, and the readiness checkpoint gate:

```bash
python tools/eval_runner.py --skill egm_brainstorm --model gemini/gemini-2.5-flash
```

## 3. Protocol Verification Checklist

When evaluating or exploring `egm_brainstorm` interactively in chat, verify:

-   **Step 1 (Open-Ended Clarification & Gate):** Drills down into half-baked concepts
    using open-ended chat questions (without structured question tools or multiple-choice lists)
    and enforces a user readiness checkpoint gate before subagent invocation.
-   **Step 2 (Upstream Multi-Lens Ideation):** Evaluates feature concepts across the
    6 specialized Goldfish perspective lenses (Contrarian/YAGNI, Cost/Quota Economics,
    UX Ergonomics, Migration & Compatibility, Observability & SRE, Tech Debt & Maintenance).
-   **Step 3 & 4 (Concepts Brief Deliverable & Handoff):** Compiles and saves the
    synthesized `concepts_brief.md` artifact for user review and handoff to
    `/egm-draft`.
