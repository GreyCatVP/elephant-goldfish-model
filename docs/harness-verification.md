<!--
Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0
-->

# Harness verification

## PR #103: current-client validation

Date: 2026-10-21–22 (America/Los_Angeles). Runtime fixes: `500eca2`, based on
`597f5ea`; verification documentation was updated after the runs. This is a synthetic
fixture, not a blanket support guarantee.

The fixture designs an offline UTF-8 nonblank-line counter. It preapproves
human decisions and dispatches reviewers directly. Interactive approval gates,
nested delegation, and adversarial filesystem isolation are not covered.
Review findings about the synthetic design are not harness failures.

| Host | Result | Evidence and limits |
| --- | --- | --- |
| Claude Code 2.1.308 | Isolation and workflow passed | Native isolation probe passed with Claude adapters. Full `--plugin-dir` run completed 15 reviewers in stage order, with canonical persona reads in child traces. Brief, draft, final design, and all five reports exist; final design matches draft. |
| Codex 0.163.0 | Isolation and workflow passed | Final fresh native command: 2 passed in 568.10 seconds. Fifteen completed fresh-context reviewers, installed-resource reads, five reports, matching draft/final design, and no implementation files. |
| Claude desktop / cloud Cowork | Workflow completed; verification partial | Candidate ZIP installed and seven skills discovered. Native UI shows all five stages. Export contains 15 reviewer transcripts and all artifacts, but eight transcripts have malformed records. Draft/final differ only in Status. One stage-9 reviewer did not read its supplied standard; isolation remains unverified. |
| ChatGPT Work, GPT-6.1 Sol (Light) | Workflow completed with recoveries | Runtime-only ZIP installed with seven skills. Native UI shows reviewer completion and the isolation child's actual response. Exported brief, draft, final design, and five reports are present; draft/final match. Supporting-resource lookup and an initial persona-path error recovered through installed local files. Full raw child traces were not exported. |
| Antigravity CLI 1.4.5 | Packaging regression passed | Native install and validation accept nine agents and seven skills after removing Claude-only fields from shared personas. Full AGY workflow and Gemini migration belong in a separate PR. |
| Gemini CLI 0.65.0 | Legacy packaging only | Client updated and manifest validation checked. No live model workflow tested in this PR. |

Fixes and research:

- Claude reviewer restrictions now live in seven thin adapters. The shared
  personas retain host-neutral frontmatter. Claude documents substitution in
  [agent content](https://code.claude.com/docs/en/plugins/components) and
  [`omitClaudeMd`](https://code.claude.com/docs/en/sub-agents). AGY documents
  [different native tool names](https://antigravity.google/docs/subagents?tab=cli).
- The Claude isolation prompt supplies the exact canonical persona path. The
  assertion still requires a real read and absence of parent/project markers.
- Codex trace parsing accepts both `stdout` and `aggregated_output`. It handles
  literal absolute multi-file `cat` reads, rejecting shell composition and
  expansion. Offline regression tests cover these cases. Initial failures were
  recorded before fixes; rerunning assertions on retained traces is distinct
  from a fresh model run.
- Marketplace metadata includes authentication policy and category from the
  [current plugin guide](https://developers.openai.com/plugins/build/plugins).
- ChatGPT personal upload succeeded with runtime files only. A full repository
  archive returned a generic upload error. This does not prove which extra file
  caused that error; the documented recipe records the working package.
- Product installation and live invocation were tested separately, following
  [OpenAI's deployment guidance](https://developers.openai.com/plugins/deploy/connect-chatgpt).

Warnings remain: Claude's validator reports a missing listing icon. AGY reports
skill-directory/name mismatches, an oversized bootstrap body, and that the
repository's contributor `AGENTS.md` is not plugin rules. These are not hidden
as clean validator output. Broader AGY changes are outside this PR.

### Cloud evidence boundaries

Open known issues track these limits and their acceptance criteria:

- [#105: Cowork workflow and isolation verification](https://github.com/google/elephant-goldfish-model/issues/105).
- [#106: ChatGPT Work recovery and native trace verification](https://github.com/google/elephant-goldfish-model/issues/106).

Keep the harness-support verification checkbox in #103 open until these gaps
are resolved or the supported scope is explicitly narrowed. Completing a
workflow does not close a verification issue by itself.

The Cowork parent's first summary claimed 16 reviewers; its export contains 15.
Use the exported records and native activity, not the parent's count. The export
removed host-added attachment records, so it cannot prove that account memory
or host instructions were absent. No Cowork isolation canary was run. Do not
transfer the Claude Code `omitClaudeMd` test result to cloud Cowork.

ChatGPT's native isolation child reported no substantive parent history and no
knowledge of the parent-only marker. The exported evidence file is a parent
summary, not an independent trace. The native UI independently shows completed
reviewers, but this run does not establish raw trace-level coverage of every
spawn argument or resource read. Installed skill SHA-256 values in the export
match the candidate's brainstorm, draft, and review skills.

Temporary Codex marketplaces are removed by the fixture. The task-installed
AGY plugin and ChatGPT test plugin were uninstalled; the Cowork test upload was
disabled. Uploaded packages and test conversations remain available for review.

### Reproduction and retained runs

Run `pytest tests` for the offline checks. Enable live tests explicitly:

```sh
EGM_CLAUDE_LIVE=1 pytest tests/integration/test_claude.py -v
EGM_CODEX_LIVE=1 pytest tests/integration/test_codex.py -v
```

The manual Claude Code workflow reused the synthetic prompt from
`test_brainstorm_draft_review`, prefixed by `/egm:egm-brainstorm`, in an empty
workspace. It used `--plugin-dir <candidate> --model sonnet`, disabled hooks,
and supplied an empty strict MCP configuration. Read, Write, Edit, Glob, Grep,
Agent, and Skill were allowed; an attempted parent Bash call was denied and
the run continued with file tools. Session
`8a876286-7376-4143-8715-f19da27255db` completed 15 agents with no failures.
Usage reports Sonnet 5.5 and Opus 5.5; the requested model alias alone does not
prove that every runtime operation used the same model.

Codex workflow `01a1625f-0645-76a1-8d6f-be15cd9f95b9` used GPT-6.1 Sol.
The test process had loaded the old multi-file parser before that fix landed;
replaying the final assertions on this retained trace passed. Native timestamps
confirm sequential stage boundaries and 15 completed reviewers. This retained
run is recorded separately from the final fresh test command. The fresh command
passed both tests in 568.10 seconds; its workflow trace is
`01a16263-6cd7-7173-8a6d-632f0cf2bb71`.

Cloud runs used uniquely named `egm-pr103-test` packages and the same design
fixture. Cowork's desktop updater reported the latest version. ChatGPT Work is
a hosted surface without a pinned client version. Artifacts and local traces
were retained for review; raw account-bearing traces are not committed.

## Historical combined verification

Date: 2026-10-07. This records a synthetic test, not a blanket support guarantee.

The candidate combined PRs #42, #43, and #46 to #54 on
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
