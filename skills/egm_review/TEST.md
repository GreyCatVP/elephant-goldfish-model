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

# Test Plan: EGM Review & Subagents

Frontmatter and link checks run in `pytest tests/unit`; behavioral evaluations run with `python tools/eval_runner.py --skill egm_review --model <model>` (see [TESTING.md](../../TESTING.md)).

## Protocol Verification Checklist

When evaluating or exploring `egm_review` interactively in chat, verify:

-   **Step 1 (Intake):** Gathers `TargetFile` and optional `GoldfishContext`.
-   **Step 2 (Semantic Split):** Discovers the split line between Feature Spec
    and Detailed Implementation Plan.
-   **Step 3 (Flow Selection):** Offers Full EGM Flow vs. Individual Stages (Steps 5, 6, 7, 8, 9).
-   **Subflows:** Properly delegates Zoom Out, Comprehension, Critic Review, and Readiness Test.
