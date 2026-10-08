<!--
Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0
-->

# EGM Testing & Behavioral Evaluation Playbook

This document provides a step-by-step developer playbook for running both
Tier 1 static unit tests and Tier 2 LiteLLM-driven behavioral evaluations across
the Elephant & Goldfish Model (EGM) skill suite.

---

## 1. Environment Prerequisites & Setup

### A. Python Environment Setup
Create and activate an isolated Python 3.10+ virtual environment:

```bash
# Navigate to the repository root
cd /path/to/egm_opensource

# Create virtual environment
python3 -m venv .venv

# Activate environment
source .venv/bin/activate

# Install testing and evaluation dependencies
pip install -r requirements-dev.txt
```

---

## 2. Tier 1: Offline Static Unit Tests

After installing the development dependencies, Tier 1 tests run offline without
network access, API keys, or model downloads. They validate YAML frontmatter
schemas and relative link integrity, the portable plugin manifest, shared
metadata consistency, marketplace/component paths, and evaluation behavior.
Retry tests exercise LiteLLM with simulated provider responses.

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

## 3. Tier 2: LiteLLM Behavioral Evaluation Flow

Tier 2 evaluations execute conversational scenarios against real model endpoints
using `tools/eval_runner.py` and [LiteLLM](https://docs.litellm.ai/).

### Option A: Testing with Google Gemini (Recommended)

1. **Obtain API Key**:
   - Go to [Google AI Studio](https://aistudio.google.com/apikey).
   - Click **"Create API key"** and select/create a Google Cloud project.
   - Copy the generated API key.

2. **Export Key in Terminal**:
   ```bash
   export GEMINI_API_KEY="AIzaSy..."
   ```

3. **Run the Full Behavioral Suite (All Skills)**:
   ```bash
   # Discovers and runs all test_scenarios.yaml suites across all skill packages
   python tools/eval_runner.py --model gemini/gemini-2.5-flash
   ```

4. **Run an Individual Skill**:
   ```bash
   python tools/eval_runner.py \
     --skill egm_draft \
     --model gemini/gemini-2.5-flash
   ```

5. **Run a Single Targeted Scenario**:
   ```bash
   python tools/eval_runner.py \
     --skill egm_draft \
     --scenario draft_and_write_design_doc \
     --model gemini/gemini-2.5-flash
   ```

6. **Run with a Dedicated LLM Judge**:
   For scenarios with subjective rubrics (e.g.,
   `comprehension_auditor_undefined_jargon` in `egm_review`):
   ```bash
   python tools/eval_runner.py \
     --skill egm_review \
     --scenario comprehension_auditor_undefined_jargon \
     --model gemini/gemini-2.5-flash \
     --judge-model gemini/gemini-2.5-pro
   ```

---

### Option B: Testing with Local Models (Zero Credentials via Ollama)

If you want to test without cloud API keys, you can run a local model using
Ollama:

1. **Start Ollama** (in a separate terminal):
   ```bash
   ollama run llama3
   ```

2. **Execute Evaluation Across All Skills or a Single Skill**:
   ```bash
   # Run all skills against local model
   python tools/eval_runner.py --model ollama/llama3

   # Run a single skill against local model
   python tools/eval_runner.py --skill egm_draft --model ollama/llama3
   ```

---

## 4. Inspecting Evaluation Reports

`tools/eval_runner.py` automatically generates structured JSON evaluation
reports in `eval_results/`:

```bash
# Inspect the latest run report
cat eval_results/egm_draft_results.json | python3 -m json.tool
```

The report records:

- Scenario IDs and evaluation types (`deterministic` vs `llm_judge`).
- Model and judge parameters used.
- Complete turn inputs and model response text.
- Pass/fail statuses and specific error messages for assertion failures.

---

## 5. CLI Parameter Reference

| Flag | Description | Default | Example |
| :--- | :--- | :--- | :--- |
| `--skill` | Target skill directory name | All skills (all suites) | `--skill egm_draft` |
| `--scenario` | Specific scenario ID within the skill suite | All scenarios in skill | `--scenario draft_and_write_design_doc` |
| `--model` | Model identifier string passed to LiteLLM | `gemini/gemini-2.5-flash` | `--model gemini/gemini-2.5-flash` |
| `--judge-model`| Dedicated model for `llm_judge` rubrics | Same as `--model` | `--judge-model gemini/gemini-2.5-pro` |
| `--temperature`| Sampling temperature (0.0 for deterministic eval) | `0.0` | `--temperature 0.0` |
| `--output-dir` | Output directory for JSON execution reports | `eval_results/` | `--output-dir reports/` |

---

## 6. Exit Codes

- `0`: All scenarios passed successfully.
- `1`: One or more scenario assertions or rubric criteria failed.
- `2`: Configuration, CLI argument, or runtime execution error (e.g., missing
  API key or `litellm` library).

## 7. Harness Test Record

A harness counts as supported after `/egm-brainstorm`, `/egm-draft`, and
`/egm-review` run end to end through its plugin install (see
[Harnesses](docs/harnesses.md)). Add a row for each run.

| Harness | Version | Date | Install | Brainstorm | Draft | Review | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Claude Code | | | Not run | | | | |
| OpenAI Codex | | | Not run | | | | |
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
