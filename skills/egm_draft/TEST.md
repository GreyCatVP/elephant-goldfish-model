<!--
Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0
-->

# Test Plan: EGM Draft Skill

This document details how to validate and evaluate the `egm-draft` skill.

## 1. Syntax Validation
Verify that `SKILL.md` contains valid YAML frontmatter and adheres to standard Agent Skill specifications:
- Ensure `name` and `description` are defined in the frontmatter.
- Verify all referenced document paths exist.

## 2. Automated Evaluations
Run the benchmark evaluation suite against your target model:
```bash
python tools/eval_runner.py --skill egm_draft --model gemini/gemini-2.5-flash
```

The suite validates:
- **Design Ingestion & Synthesis**: The agent ingests `discussion_summary.md` and generates structured Overview, Goals, Non-Goals, Technical Plan, and Implementation.
- **CUJ & Architectural Structure**: CUJs follow Given/When/Then formatting, and architecture contains clear diagrams/flows.
- **Artifact-First Discipline**: The agent writes drafts to files rather than dumping long documents into chat.

