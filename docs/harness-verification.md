<!--
Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0
-->

# Combined harness verification

Date: 2026-10-07. This records a synthetic test, not a blanket support guarantee.

The candidate combined PRs #42, #43, and #46–#54 on
`test/combined-pr-validation`. Native runs loaded candidate `a9fd6d7`.
Commit `c1e6991` incorporates the compatibility fixes pushed to #42 and #49;
its unit suite passes all 61 tests. The combined site passes check and build.

The fixture designs an offline UTF-8 nonblank-line counter. It preapproves
human decisions and uses direct reviewer dispatch. Interactive approval gates
and nested delegation are not covered. No implementation code is requested.

| Host | Result | Evidence and limits |
| --- | --- | --- |
| Codex 0.161.0 | Automated fixture passed | Native installation, isolation, and full brainstorm/draft/review tests passed; the workflow test checks 15 completed reviewers and installed-resource reads. |
| Claude Code 2.1.293, Sonnet | Partial | Isolation/resource probe passed. Full run produced all reports and 15 Agent calls with child traces, but reported parallel stages and a mismatched brainstorm lens. Four malformed parent-trace lines prevent complete trace verification. |
| Cursor 2026.10.01-e373342, composer-2.5 | Workflow fixture completed | Trace contains 15 successful native tasks; brief, draft, final design, and five review-stage reports exist. Final design matches draft. Separate isolation canaries were not tested. |
| Antigravity CLI 1.3.1 | Failed fixture constraints | Installation validated seven skills and nine agents. Automatic resource discovery stalled. An explicit-installed-path retry generated brief and draft, but a structural reviewer invoked web search despite the offline fixture restriction; the run was stopped before review completion. |

Compatibility fixes retain the host manifests in #42 and allow Claude-only
adapters to resolve canonical shared personas in #49. The integration merge
also retains both Codex and Claude skill guidance and installs the full
development requirements in CI.
