---
trigger: model_decision
description: Enforces `#egm` tagging in pull request and review descriptions
  for changes implementing or referencing EGM design specifications.
---

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

### EGM Pull Request & Changelist Tagging

When authoring or updating a Pull Request (PR), Changelist (CL), or review description
that implements, refactors, or references an Elephant & Goldfish Model (EGM) specification
or review:

1. Include the `#egm` hashtag in the description body or footer.
2. **Do NOT** place `#egm` in the git commit title/subject line (to prevent breaking
   Conventional Commit linting rules).
