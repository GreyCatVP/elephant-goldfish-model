<!--
Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0
-->

# Verifiable Codex plugin support

Author: n3wth

## Problem and goals

Installation and skill discovery do not establish that Codex can execute the
EGM workflow. The existing LiteLLM evaluations check responses without running
the installed plugin's file tools or native reviewer delegation. Bundled paths
also need an explicit base when the user's project is outside the plugin.

This change keeps one shared skill suite and adds Codex-specific guidance for
resource paths, fresh-context delegation, question-tool availability, and
artifact links. Offline CI checks the packaging contract. Opt-in live tests
exercise the installed candidate in an unrelated workspace and inspect actual
reviewer results and generated artifacts.

Non-goals: changing other harnesses' behavior, implementing a new agent runtime,
changing normal human approval gates, or claiming support for untested Codex
versions, interactive UI behavior, or nested delegation.

## Implementation

- `docs/codex.md` holds the Codex adapter instructions. Each of the seven
  `skills/*/SKILL.md` entry points links to it; `docs/harnesses.md` explains
  capability detection instead of promising a particular tool name.
- `tests/unit/test_codex_packaging.py` validates the marketplace-to-manifest
  path, skill identities, bundled persona/template references, and access to
  the shared Codex guide. `tests/unit/test_codex_evidence.py` rejects missing
  reviewer events, inherited context, and failed resource reads. Existing
  offline CI discovers these tests.
- `tests/integration/test_codex.py` installs a copied candidate under a unique
  temporary marketplace name, checks installed bytes, and removes that
  installation afterward. It uses normal Codex authentication without copying
  credentials or replacing the user's EGM installation.
- The native isolation scenario puts a random marker only in the parent's
  input and inspects native delegation and the actual child's result. The
  workflow scenario produces a brief, design, and all five review reports for
  a small offline line-counting tool. Synthetic approvals are explicit test
  inputs, not a change to the skill's interactive contract.
- `TESTING.md` documents live-test costs, prerequisites, evidence, and limits.
  `docs/designs/README.md` indexes this design.

## Validation and limits

Run offline tests on every change. Live tests are opt-in, bounded by a
20-minute timeout per scenario, and retain traces outside the synthetic
workspace for diagnosis. They must fail if native reviewer evidence or
artifacts are missing; a parent summary cannot substitute for either.

Fresh context isolates conversation history, not filesystem access or shared
memory services. Disable unrelated configured integrations in the test run.
The marker probe is a regression test for transcript inheritance, not a
security boundary against a reviewer deliberately searching for transcripts.

Keep actual live results and tested CLI version in the harness test record.
Passing the noninteractive fixture does not verify the interactive gates.

## Alternatives

Copying skills into a project bypasses packaging and breaks bundled resources.
Testing only LiteLLM replies cannot show native subagent execution. Forking
the skill suite for Codex would duplicate the workflow and allow it to drift.
The shared guide and native opt-in test avoid those gaps.
