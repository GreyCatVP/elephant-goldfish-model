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

Opt-in integration tests run the live candidate through a temporary Codex marketplace:

```sh
EGM_CODEX_LIVE=1 pytest tests/integration/test_codex.py -v
```

Tests verify candidate installation, fresh-context reviewer isolation, and workflow artifacts.
Each test runs with an authenticated Codex CLI in an isolated sandbox.
See [Codex integration](docs/codex.md) and [Codex support design](docs/designs/codex_support.md).

---

## Harness Test Record

A harness counts as supported after `/egm-brainstorm`, `/egm-draft`, and
`/egm-review` run end to end through its plugin install (see
[Harnesses](docs/harnesses.md)). Add a row for each run.

| Harness | Version | Date | Install | Brainstorm | Draft | Review | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Antigravity CLI | 1.4.5 | 2026-10-21 | Pass; validator warnings | Not run | Not run | Not run | Packaging regression only; broader AGY work is separate. |
| Claude Code | 2.1.308 | 2026-10-21 | Pass (`--plugin-dir`) | Pass (fixture) | Pass (fixture) | Pass (fixture) | 15 native reviewers in stage order; separate isolation probe passed. |
| Claude Cowork | Current desktop, cloud task | 2026-10-21 | Pass (ZIP) | Completed | Completed | Partial verification | Five reports exist; malformed exported traces and missing standard read prevent a clean verification result. |
| OpenAI Codex | 0.163.0 | 2026-10-22 | Pass | Pass (fixture) | Pass (fixture) | Pass (fixture) | Final fresh command: 2 passed in 568.10s, including isolation. |
| ChatGPT Work | GPT-6.1 Sol, Light | 2026-10-21 | Pass (runtime ZIP) | Completed with recovery | Completed | Completed | Native UI confirms delegation; exported artifacts match. Raw trace coverage limited. |

### Interpreting native test results

Track open cloud verification gaps in [#105 (Cowork)](https://github.com/google/elephant-goldfish-model/issues/105) and [#106 (ChatGPT Work)](https://github.com/google/elephant-goldfish-model/issues/106).

- Inspect native tool traces for reviewer launches, completion, and intended resource reads.
- Verify sequential stage execution and persona lenses in addition to artifact existence.
- Distinguish fixture design findings from execution failures of the review workflow.
- Keep installation, execution, and transcript isolation results recorded separately.
