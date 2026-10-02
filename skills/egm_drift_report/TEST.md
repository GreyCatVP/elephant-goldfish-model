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

Frontmatter and link checks run in `pytest tests/unit`; behavioral evaluations run with `python tools/eval_runner.py --skill egm_drift_report --model <model>` (see [TESTING.md](../../TESTING.md)).
