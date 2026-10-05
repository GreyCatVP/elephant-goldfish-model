<!--
Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0
-->

# Verification and Evaluation Commands for `egm-bootstrap`

## Skill Syntax & Frontmatter Validation

Validate YAML frontmatter and markdown structure:

```bash
# Verify YAML frontmatter syntax
python3 -c '
import yaml
with open("skills/egm_bootstrap/SKILL.md") as f:
    content = f.read().split("---")[1]
    data = yaml.safe_load(content)
    assert data["name"] == "egm-bootstrap"
    assert "description" in data
print("✓ SKILL.md frontmatter valid")
'
```

## Manual Verification Scenarios

1. **Small Tree Execution (Sequential)**:
   - Target a directory with 2-5 subdirectories.
   - Verify that the agent executes sequentially without spawning subagents.
   - Verify generated `README.md` files contain Interface, Invariants, Side Effects, and relative links.
2. **Safety Gate Threshold (>15 Subdirectories)**:
   - Target a directory with 16+ subdirectories.
   - Verify that discovery pauses upon reaching >15 directories and requests user confirmation in chat before proceeding.
3. **Subagent Halting Gate**:
   - Run in an environment without task delegation tools.
   - Verify that the prominent halting banner is displayed and execution stops immediately.

## Automated Evaluation Suite

Run the evaluation suite using the open-source evaluation runner:

```bash
python tools/eval_runner.py --skill egm_bootstrap --model gemini/gemini-2.5-flash
```
