<!--
Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0
-->

# Codex plugin support

Author: n3wth

## Problem

Installation and skill discovery do not establish that Codex can execute the
EGM workflow. Offline unit tests check packaging; nothing runs the installed
plugin's file tools or native reviewer delegation. Bundled paths also need an
explicit base directory when the user's project is outside the plugin.

## Goals and non-goals

Goals:

- Keep one shared skill suite. Add Codex-specific guidance for resource paths,
  fresh-context delegation, structured question tool availability, and
  artifact links.
- Check the packaging contract in offline CI.
- Run opt-in live tests that install the candidate in an unrelated workspace
  and inspect reviewer results and generated artifacts.

Non-goals:

- Changing other harnesses' behavior.
- Implementing a new agent runtime.
- Changing human approval gates.
- Claiming support for untested Codex versions, interactive UI behavior, or
  nested delegation.

## Approach

- `docs/codex.md` holds the Codex adapter instructions. Skills resolve
  `references/` against the skill directory and `agents/`, `resources/`, and
  `docs/` against the plugin root. Each of the seven `skills/*/SKILL.md` entry
  points links to the guide; `docs/harnesses.md` explains capability detection
  instead of specifying a tool name.
- Native delegation uses the Codex multi-agent tools (`spawn_agent`,
  `wait_agent`) with `fork_context: false` or `fork_turns: "none"`, so each
  Goldfish starts without the parent transcript.
- `tests/unit/test_codex_packaging.py` validates that
  `.agents/plugins/marketplace.json` resolves to `.codex-plugin/plugin.json`,
  specifies `authentication: "ON_INSTALL"` and `category: "Productivity"`,
  and checks skill identities, bundled persona and template references, and
  access to the shared Codex guide. Existing offline CI discovers these tests.
- `tests/integration/test_codex.py` runs only when `EGM_CODEX_LIVE=1`. It
  installs a copied candidate under a unique temporary marketplace name, uses
  the user's existing `codex login` session, and removes the installation
  afterward. It runs `codex exec --skip-git-repo-check --ignore-user-config
  --sandbox workspace-write --json` with `features.multi_agent=true` and
  `features.remote_plugin`, `features.hooks`, and `features.memories` disabled.
- Reviewer evidence comes from the Codex trace. The test reads `thread_id`
  from the `thread.started` event on stdout, locates
  `$CODEX_HOME/sessions/**/*<thread_id>.jsonl`, requires `SubAgentActivity`
  started and completed events, and then reads each child trace. The
  `successful_reads` helper inspects both `stdout` and `aggregated_output`,
  and accepts literal absolute multi-file `cat` commands.
- The isolation scenario puts a random marker only in the parent's input; the
  child must answer `UNKNOWN`. The workflow scenario produces a brief, a
  design, and all five review reports for an offline line-counting tool. Human
  gates receive scripted approval replies from the test fixture; the skill's
  interactive contract does not change.
- `TESTING.md` documents live-test costs, prerequisites, evidence, and limits,
  and holds the harness test record in its "Harness Test Record" section.
  `docs/designs/README.md` indexes this design.

## Risks and limits

- Cost: each live scenario has a 20-minute timeout and consumes model usage.
  Run it on demand, not on every pull request.
- Shared CLI state: `codex plugin` commands mutate the global Codex
  configuration. Run one live test at a time and point `CODEX_HOME` at an
  isolated directory when possible.
- Isolation scope: fresh context isolates conversation history, not filesystem
  access or shared memory services. The marker probe is a regression test for
  transcript inheritance, not a security boundary against a reviewer that
  searches for transcripts.
- Schema drift: Codex tool names and trace event types vary by CLI version.
  Tests fail when `SubAgentActivity` evidence is missing. Record the tested CLI
  version in the harness test record.
- Coverage: passing the noninteractive fixture does not verify the interactive
  gates.

## Alternatives

Copying skills into a project bypasses packaging and breaks bundled resources.
Testing only model replies cannot show native subagent execution. Forking the
skill suite for Codex would duplicate the workflow and allow it to drift. The
shared guide and native opt-in test avoid those gaps.
