<!--
Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0
-->

# EGM Testing & Behavioral Evaluation Playbook

This document provides a step-by-step developer playbook for running both
unit tests and LiteLLM-driven evals evaluations across the EGM skill suite.

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

# Install testing and evaluation dependencies
pip install -r requirements-dev.txt
```

---

## Unit Tests

Unit tests run offline without network access, API keys, or model
dependencies. They validate YAML frontmatter schemas and relative link
integrity.

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

## LiteLLM Evals

Evaluations execute conversational scenarios against model endpoints
using `tools/eval_runner.py` and [LiteLLM](https://docs.litellm.ai/).

### Testing with Gemini

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

### Testing with Local Models

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
[Harnesses](docs/harnesses.md)). Contributors adding support for other
harnesses should add a row for each verification run.

| Harness | Version | Date | Install | Brainstorm | Draft | Review | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Antigravity | | | Not run | | | | |
| Gemini CLI | | | Not run | | | | |
