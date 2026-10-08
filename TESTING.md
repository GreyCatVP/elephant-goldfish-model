# EGM Testing Playbook

This document provides a step-by-step developer playbook for running unit tests across the EGM skill suite.

---

## Setup

### A. Python Environment Setup
Create and activate an isolated Python 3.10+ virtual environment:

```bash
# Navigate to the repository root
cd /path/to/egm_opensource

# Create virtual environment
python3 -m venv .venv

# Activate environment
source .venv/bin/activate

# Install testing dependencies
pip install -r requirements-dev.txt
```

---

## Unit Tests

Unit tests run offline without network access, API keys, or model
dependencies. They validate YAML frontmatter schemas and relative link
integrity, the portable plugin manifest, shared metadata consistency, and
marketplace/component paths.

```bash
# Run all unit tests
pytest tests/unit

# Run with verbose output
pytest tests/unit -v

# Run a specific unit test module
pytest tests/unit/test_frontmatter.py -v
pytest tests/unit/test_link_integrity.py -v
```
---

## Native Claude Reviewer Probe (Opt-in)

With an authenticated Claude Code 2.1.271+ installation, run:

```bash
EGM_CLAUDE_LIVE=1 pytest tests/integration/test_claude.py
```

This uses the account's model quota. It loads a copy of the plugin, invokes
the review skill, and checks that a native reviewer reads only its persona and
sees no parent or project `CLAUDE.md` context. See [Claude integration](docs/claude.md).
---

## Native Codex Integration Tests (Opt-in)

Unit tests include Codex manifest, discovery, and bundled-resource checks; they
do not execute the native Codex plugin, filesystem tools, or subagents.

To test those boundaries, run from a Git checkout with an authenticated Codex
CLI and native subagent support. These tests consume model usage and can take
several minutes:

```sh
EGM_CODEX_LIVE=1 pytest tests/integration/test_codex.py -v
```

Each scenario has a 20-minute timeout. Without `EGM_CODEX_LIVE=1`, integration
tests skip before installing or invoking Codex.

The fixture installs the current candidate through a uniquely named local
marketplace and removes that temporary plugin and
marketplace afterward. It leaves existing EGM installations intact. It ignores
user configuration and disables unrelated remote plugins, hooks, and memories
for the model run, while using normal CLI authentication. Do not run concurrent
plugin configuration edits while this fixture is installing or cleaning up.

Tests run outside the source checkout. The isolation probe checks the actual
child response for a random parent-only marker. The workflow test checks
brainstorm and draft artifacts, five review reports, and native reviewer
completion. Its synthetic user explicitly approves all fixture gates; it does
not verify interactive question UI or human approval behavior.

Traces stay in pytest's tmp dir; see `tests/integration/test_codex.py` for what
is checked.

---

## Harness Test Record

A harness counts as supported after `/egm-brainstorm`, `/egm-draft`, and
`/egm-review` run end to end through its plugin install (see
[Harnesses](docs/harnesses.md)). Add a row for each run.

| Harness | Version | Date | Install | Brainstorm | Draft | Review | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Claude Code | | | Not run | | | | |
| OpenAI Codex | 0.161.0 | 2026-10-07 | Pass | Pass (fixture) | Pass (fixture) | Pass (fixture) | 15 native reviewers; isolation probe passed. Interactive gates and nesting not tested. |
| Cursor | | | Not run | | | | |
| Gemini CLI | | | Not run | | | | |
| Antigravity | | | Not run | | | | |

### Interpreting native test results

See the [combined harness verification record](docs/harness-verification.md)
for a worked example with explicit limits and partial results.

- Record the candidate commit, host version, model, invocation, and artifact
  locations. When testing several pending PRs, use their combined candidate;
  separate passing runs cannot reveal interactions between their changes.
- Check native tool traces for reviewer launches, completion, and reads of the
  intended installed resources. A parent's success message or a folder of
  reports alone is insufficient evidence.
- Verify stage order and reviewer roles as well as artifact existence. A run
  can produce every report while parallelizing stages that should be sequential
  or assigning the wrong review lens. Record this as a deviation.
- Distinguish review findings about the fixture's design from failures of the
  review workflow. Finding a design defect is not itself a harness failure.
- A fixture that preapproves user decisions does not test interactive approval
  gates. Direct dispatch does not test nested delegation. Record both limits.
- Keep discovery, installation, workflow execution, and isolation results
  separate. An explicit-path workaround must not count as successful automatic
  discovery; malformed or incomplete traces leave the affected checks unverified.
