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

