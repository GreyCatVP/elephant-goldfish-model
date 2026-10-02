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

Frontmatter and link checks run in `pytest tests/unit`; behavioral evaluations run with `python tools/eval_runner.py --skill egm_review_loop --model <model>` (see [TESTING.md](../../TESTING.md)).

## Protocol Verification Checklist

When evaluating or exploring `egm_review_loop` interactively in chat, verify:

-   **Step 1 (Intake & Config):** Validates required inputs and resolves standard paths.
-   **Step 2.1 (Target Resolution):** Unconditionally re-scans line numbers before auditing.
-   **Step 2.2 (Review Swarm):** Spawns subagents (or sequentially iterates personas in degraded mode) across requested standards.
-   **Step 2.3 & 2.4 (Resolve Handoff & Turn Boundary):** Hands findings to `egm-resolve` and respects human decision gates.
