<!--
Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0
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

