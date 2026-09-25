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

# Test Plan: EGM Drift Report Skill

This document details how to validate and evaluate the `egm-drift-report` skill.

## 1. Skill Validation (Syntax Check)

Verify that `SKILL.md` contains valid YAML frontmatter and adheres to the Agent Skill specification:
- Ensure `name` and `description` are defined in the frontmatter.
- Verify Markdown header formatting and output template syntax.

## 2. Automated Evaluations

To verify that the agent scans the codebase and identifies schema/logic drift:

```bash
python tools/eval_runner.py --skill egm_drift_report --model gemini/gemini-2.5-flash
```

The suite tests:
- **Drift Detection**: Verifies the agent compares design docs with implementation files and accurately reports discrepancies.
- **Strict Report Output**: Ensures the agent outputs `{YYYY-MM-DD}_DRIFT_REPORT.md` following the required format without chat dumps.\n

