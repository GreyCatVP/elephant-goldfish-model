# Multi-Harness Support: Hermes Agent, OpenClaw, and Delta

* **Authors:** Sriram ([@Seburan](https://github.com/Seburan)), Sriram Yatham ([@yathamsriram243-blip](https://github.com/yathamsriram243-blip))
* **Status:** Stage 1 Design Proposal (Draft Adapters; Live Traces Unverified)
* **Date:** 2026-10-24
* **Refs:** [#116](https://github.com/google/elephant-goldfish-model/issues/116)
* **Related PRs:** [#119](https://github.com/google/elephant-goldfish-model/pull/119), [#148](https://github.com/google/elephant-goldfish-model/pull/148)

---

## 1. Overview & Problem Statement

The Elephant-Goldfish Model (EGM) implements Spec-Driven Development (SDD) using dual memory boundaries: deep persistent context for drafting specifications (The Elephant) and isolated, stateless subagents for reviewing and stress-testing specifications (The Goldfish).

Currently, EGM packages official manifests for three environments:
1. **Antigravity**: Root `plugin.json` declaring the Agent Plugins 1.0.0 schema.
2. **Claude Code & Claude Cowork**: `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`.
3. **OpenAI Codex & ChatGPT Work**: `.codex-plugin/plugin.json` and `.agents/plugins/marketplace.json`.

Developers operating in emerging autonomous coding harnesses—specifically **Hermes Agent** (Nous Research), **OpenClaw**, and **Delta**—must maintain ad-hoc fork modifications or manually map file paths to install EGM. This leads to documentation drift, broken subagent delegations, and accidental leaks of parent conversation context into reviewer sessions.

This document defines the architectural specification, manifest schemas, directory discovery mappings, subagent delegation mechanics, failure recovery guardrails, and the two-stage rollout criteria required to support Hermes Agent, OpenClaw, and Delta in EGM.

---

## 2. Heilmeier Catechism Analysis

| Catechism Dimension | Project Evaluation |
| :--- | :--- |
| **Objectives**<br>*(No Jargon)* | Enable developers using Hermes Agent, OpenClaw, and Delta coding assistants to install and run this repository's specification drafting and isolated subagent review workflows directly from source without copying files, editing configuration scripts, or modifying the shared skill instructions. |
| **State of the Art** | EGM officially packages manifests for Antigravity, Claude Code/Cowork, and OpenAI Codex/ChatGPT. Developers on other emerging agent platforms (Hermes Agent, OpenClaw, Delta) must manually copy skill files or maintain private forks. This duplicates text, breaks relative markdown links to personas and rubrics, risks leaking parent conversation history into reviewers (violating zero-context isolation), and burdens users with manual updates whenever upstream prompts improve. |
| **New Approach** | Introduce lightweight, static manifest adapters (`.hermes/plugin.yaml`, `.openclaw/openclaw.plugin.json`, `.delta/plugin.json`) pointing directly to shared `skills/` and `agents/` directories without runtime transpilation or build steps. This succeeds because modern agent platforms natively support declarative plugin manifests and isolated subprocess/child-session spawning, allowing single-source prompt text to execute within each host's native isolation boundaries. |
| **Impact** | Developers on Hermes Agent, OpenClaw, and Delta gain first-class access to spec-driven development with verified reviewer isolation. EGM maintainers avoid managing disparate forks or complex transpilation pipelines, expanding EGM's reach across the autonomous agent ecosystem with zero ongoing build overhead. |
| **Risks & Payoffs** | **Risks**: Upstream manifest schema drift, accidental parent context leakage during subagent dispatch, and premature support claims before live execution proof.<br>**Payoffs**: Universal single-source distribution across six agent platforms, guaranteed reviewer isolation, and automated offline regression prevention. |
| **Cost & Token Economics** | **Infrastructure & Runtime**: Zero financial cost, zero background daemons, zero external cloud dependencies. Manifest parsing overhead is under 5 ms.<br>**Token Budget**: Multi-stage reviews consume an estimated 16k–32k input tokens per reviewer run (~60k–120k tokens total across stages 5–9). Local inference hosts (e.g., vLLM, Ollama) require models with >= 32k context windows and sequential dispatch (concurrency limit = 1) to prevent VRAM exhaustion.<br>**Headcount**: Zero additional maintainer headcount; manifest synchronization is verified via CI unit tests executing offline in under 10 seconds. |
| **Timeline** | **Stage 1 (Design & Contracts)**: Immediate; delivered and verified in PR #119.<br>**Stage 2 (Live Trace Promotion)**: Estimated 2 to 4 weeks per harness, driven asynchronously as community contributors or maintainers capture live execution traces and canary isolation proofs. |
| **Metrics & Exams** | **Mid-Term Exam (Stage 1)**: 100% pass on offline schema synchronization and strict JSON/YAML validation (`pytest tests/unit/test_harnesses.py`), zero broken relative links (`pytest tests/unit/test_link_integrity.py`), and 100% compliance with EGM document standards.<br>**Final Exam (Stage 2)**: Captured end-to-end execution logs and child session transcripts for `/egm-brainstorm`, `/egm-draft`, and `/egm-review` on live harnesses, verifying (1) zero parent context leakage via canary assertions and (2) strict enforcement of read-only tools (`Read`, `Grep`, `Glob`) with write/edit/shell blocked. |

---

## 3. Goals vs. Non-Goals

### 3.1 In-Scope Goals
* **Single-Source Text Integrity**: Maintain EGM's core invariant: *No harness gets a fork of the skill text*. All harnesses share the identical root `skills/`, `agents/`, and `resources/` files.
* **Canonical Compatibility Manifests**: Provide static manifests matching native discovery standards:
  * Hermes Agent: `.hermes/plugin.yaml`
  * OpenClaw: `.openclaw/openclaw.plugin.json`
  * Delta: `.delta/plugin.json`
* **Subagent Delegation Mappings**: Document explicit subagent invocation mappings ensuring Goldfish zero-context isolation:
  * Hermes: Subprocess dispatch via `hermes.spawn`
  * OpenClaw: Native child session dispatch via `sessions_spawn`
  * Delta: Task runner delegation via `delta.spawn` (or `delta run --isolated`)
* **Automated Offline Contract Validation**: Maintain polymorphic unit tests in `tests/unit/test_harnesses.py` enforcing metadata alignment (`name`, `version`, `author`, `repository`, `license`) between root `plugin.json` and all compatibility manifests, with strict JSON validation for `.json` and YAML validation for `.yaml`.
* **Documentation & Harness Guide**: Document installation commands, manifest structures, and delegation tools in `docs/harnesses.md` and `TESTING.md`.

### 3.2 Out-of-Scope Non-Goals
* **No Runtime Transpilation**: EGM skills will not be transpiled or wrapped in Python/JavaScript packages. Harnesses must execute standard markdown `SKILL.md` files.
* **No Proprietary Registries**: EGM will not host custom package server infrastructure. Harnesses discover plugins via Git repositories or local directory paths.
* **No Gateway Extensions**: OpenClaw chat channel bridges (Slack, Discord) are out of scope. EGM targets coding agent workflows exclusively.
* **No Multi-Device Synchronization**: Remote profile synchronizers and session state persistence are left to the underlying harness runtimes.

---

## 4. Harness Specification Matrix

| Feature / Dimension | Hermes Agent | OpenClaw | Delta |
| :--- | :--- | :--- | :--- |
| **Native Manifest** | `.hermes/plugin.yaml` | `.openclaw/openclaw.plugin.json` | `.delta/plugin.json` |
| **Manifest Format** | YAML 1.2 | Strict JSON (RFC 8259) | Strict JSON (RFC 8259) |
| **Minimum Engine Version** | `>= 0.8.2` | `>= 1.0.4` | `>= 0.9.0` |
| **Skill Discovery Path** | `skills` (`skills/`) | `skills` (`skills/`) | `skills` (`skills/`) |
| **Persona Discovery Path**| `agents` (`agents/`) | `agents` (`agents/`) | `agents` (`agents/`) |
| **Subagent Tool Mapping** | `hermes.spawn` | `sessions_spawn` | `delta.spawn` |
| **Invocation Signature** | `hermes.spawn(task="...", tools=["Read","Grep","Glob"])` | `sessions_spawn(task="...", mode="isolated", tools=["Read","Grep","Glob"])` | `delta.spawn(task="...", isolate=True, tools=["Read","Grep","Glob"])` |
| **Context Isolation Guarantee** | Clean subprocess / isolated thread | Isolated child session (`mode: "isolated"`) | Fresh runner subprocess (`isolate: True`) |
| **Tool Restriction Policy** | Read-only tools (`Read`, `Grep`, `Glob`) | Read-only tools (`Read`, `Grep`, `Glob`) | Read-only tools (`Read`, `Grep`, `Glob`) |
| **Tool Enforcement Mechanism** | Prompt-level dispatch + dispatch argument tool filter | Prompt-level dispatch + dispatch argument tool filter | Prompt-level dispatch + dispatch argument tool filter |
| **Install Command (Remote)** | `hermes plugins install <repo>` | `openclaw plugins install <repo>` | `delta skills tap add <repo>` |
| **Install Command (Local)** | `hermes plugins install ./` | `openclaw plugins install ./` | `delta skills tap add ./` |
| **Stage 1 Support Status** | **Unverified** (#116) | **Unverified** (#116) | **Unverified** (#116) |

---

## 5. Architectural Design & Manifest Layout

To prevent file duplication, compatibility manifests are thin declarative metadata adapters co-located within dedicated harness directories at the repository root:

```text
elephant-goldfish-model/
├── plugin.json                 # Canonical Agent Plugins 1.0.0
├── .claude-plugin/             # Claude Code & Cowork adapter
├── .codex-plugin/              # OpenAI Codex adapter
├── .hermes/                    # Hermes Agent adapter
│   └── plugin.yaml
├── .openclaw/                  # OpenClaw adapter
│   └── openclaw.plugin.json
├── .delta/                     # Delta adapter
│   └── plugin.json
├── agents/                     # Persona definitions (egm-zoom-out, egm-design, etc.)
├── skills/                     # Canonical EGM skills (egm_brainstorm, egm_draft, etc.)
├── resources/                  # Document standards & finding contracts
└── docs/
    ├── designs/
    │   ├── README.md           # Design index
    │   └── multi_harness_support.md
    └── harnesses.md            # Harness installation & delegation matrix
```

### 5.1 Hermes Agent Manifest (`.hermes/plugin.yaml`)
```yaml
name: egm
version: 0.1.0
description: "Elephant-Goldfish Model: spec-driven development with deep-context drafting and zero-context Goldfish reviews."
author:
  name: Google LLC
homepage: https://egm.dev
repository: https://github.com/google/elephant-goldfish-model
license: Apache-2.0
skills: skills
agents: agents
```

### 5.2 OpenClaw Manifest (`.openclaw/openclaw.plugin.json`)
```json
{
  "name": "egm",
  "version": "0.1.0",
  "description": "Elephant-Goldfish Model: spec-driven development with deep-context drafting and zero-context Goldfish reviews.",
  "author": {
    "name": "Google LLC"
  },
  "homepage": "https://egm.dev",
  "repository": "https://github.com/google/elephant-goldfish-model",
  "license": "Apache-2.0",
  "skills": "skills",
  "agents": "agents"
}
```

### 5.3 Delta Manifest (`.delta/plugin.json`)
```json
{
  "name": "egm",
  "version": "0.1.0",
  "description": "Elephant-Goldfish Model: spec-driven development with deep-context drafting and zero-context Goldfish reviews.",
  "author": {
    "name": "Google LLC"
  },
  "homepage": "https://egm.dev",
  "repository": "https://github.com/google/elephant-goldfish-model",
  "license": "Apache-2.0",
  "skills": "skills",
  "agents": "agents"
}
```

---

## 6. Staging & Contribution Boundary (Stage 1 vs. Stage 2)

In accordance with EGM's contribution guidelines ([AGENTS.md](../../AGENTS.md)), harness expansion follows a strict two-stage lifecycle:

### Stage 1: Design Specification & Manifest Contracts
* **Deliverable Files**:
  1. `docs/designs/multi_harness_support.md` (This technical design specification)
  2. `docs/designs/README.md` (Design index registration)
  3. `.hermes/plugin.yaml` (Hermes compatibility manifest)
  4. `.openclaw/openclaw.plugin.json` (OpenClaw compatibility manifest)
  5. `.delta/plugin.json` (Delta compatibility manifest)
  6. [`docs/harnesses.md`](../harnesses.md) (Installation and delegation matrix updates)
  7. [`TESTING.md`](../../TESTING.md) (Harness test record with unverified status)
  8. [`tests/unit/test_harnesses.py`](../../tests/unit/test_harnesses.py) (Strict JSON/YAML polymorphic manifest tests)
  9. [`tests/integration/test_codex.py`](../../tests/integration/test_codex.py) (Cross-platform UTF-8 trace decoding)
* **Support Status**: Hermes Agent, OpenClaw, and Delta are explicitly recorded as **Unverified** in `TESTING.md` and `docs/harnesses.md`.
* **Prerequisites for Merge**: All 50 offline unit tests pass, relative links pass integrity validation, and maintainer design consensus is reached.
* **Stage 1 Maintenance Policy**: If an upstream harness publishes breaking schema or discovery path changes while in Stage 1 prior to live verification, the adapter manifest and unit test schema assertions must be updated in a minor patch PR, preserving offline test integrity without blocking independent Stage 2 promotions.

### Stage 2: Live Verification & Support Promotion
* **Decoupled Promotion**: Hermes Agent, OpenClaw, and Delta may be promoted independently across separate follow-up PRs as contributors or maintainers capture live evidence for each target.
* **Submission Format**: Live evidence may be submitted as:
  * Formatted execution summaries with raw JSONL traces attached directly to the Pull Request body (following [Pull Request Template](../../.github/PULL_REQUEST_TEMPLATE.md)), or
  * Automated opt-in integration tests under `tests/integration/` (matching the `test_codex.py` harness pattern: `tests/integration/test_hermes.py` activated via `EGM_HERMES_LIVE=1`, `tests/integration/test_openclaw.py` activated via `EGM_OPENCLAW_LIVE=1`, and `tests/integration/test_delta.py` activated via `EGM_DELTA_LIVE=1`).
* **Required Evidence Checklist for Each Harness**:
  1. **Installation Log**: Clean terminal transcript of the plugin installation command.
  2. **Workflow Execution**: Verified artifacts from end-to-end execution of `/egm-brainstorm`, `/egm-draft`, and `/egm-review`.
  3. **Canary Isolation Proof**: Verified absence of a unique parent canary token in child session transcripts, confirming zero parent conversation inheritance.
  4. **Tool Restriction Proof**: Evidence that child reviewers operate with write and shell tools disabled, and that any attempted modifications are rejected.

### Rollback & Deprecation Protocol
If an upstream harness release breaks manifest parsing, alters plugin discovery paths, or compromises child subagent isolation:
1. **Immediate Status Demotion**: The affected harness row in `TESTING.md` will be updated from `Pass` to `Degraded` or `Broken`, referencing the tracking issue.
2. **Advisory Documentation**: A notice will be added to `docs/harnesses.md` documenting the regression and pinning the last known good engine version.
3. **Reversion / Patch**: If an upstream harness removes compatibility support entirely, its compatibility manifest directory will be deprecated and removed in a follow-up patch PR.

---

## 7. Alternatives Considered

1. **Dynamic Runtime Transpiler / CLI Wrapper**:
   * *Concept*: Build a CLI utility (`egm-cli`) that translates EGM skills dynamically into proprietary plugin packages at install time.
   * *Rejection Rationale*: Violates EGM's minimalism and zero-runtime principles. Markdown-based `SKILL.md` is already an industry standard natively consumable by modern agents. Introducing runtime build steps introduces unnecessary failure modes and dependencies.
2. **Filesystem Symlinking into `.agents/skills/`**:
   * *Concept*: Symlink root `skills/` to `.agents/skills/` to satisfy harnesses expecting `.agents/`.
   * *Rejection Rationale*: Symlinks fail on Windows filesystems without administrative privileges or developer mode enabled. Furthermore, `.agents/` is reserved for Codex plugin catalog discovery (`.agents/plugins/marketplace.json`).
3. **Discrete Static Compatibility Manifests (Selected)**:
   * *Concept*: Maintain thin static metadata adapters (`.hermes/plugin.yaml`, `.openclaw/openclaw.plugin.json`, `.delta/plugin.json`) pointing to shared `skills/` and `agents/`.
   * *Adoption Rationale*: Retains single-source textual integrity, requires no runtime build steps, and integrates cleanly with unit test assertions against metadata drift.
4. **Monolithic Root Manifest Extension**:
   * *Concept*: Embed harness-specific configuration blocks directly inside root `plugin.json` (e.g., `"hermes": {...}`, `"openclaw": {...}`, `"delta": {...}`).
   * *Rejection Rationale*: External harnesses scan for specific filenames and directory conventions (`.hermes/plugin.yaml` requires YAML format, `.openclaw/openclaw.plugin.json` resides in `.openclaw/`). Injecting harness-specific schemas into root `plugin.json` violates the portable Agent Plugins 1.0.0 JSON schema contract and creates unnecessary coupling between independent harness ecosystems.

---

## 8. Risks, Failure Modes & Mitigations

* **Risk 1: Subagent Parent Context Leaks**:
  * *Failure Mode*: A child session inherits the parent chat conversation, violating the zero-context Goldfish requirement.
  * *Mitigation*: Subagent dispatch policies specify clean child boundaries via native tools (`sessions_spawn`, `hermes.spawn`, `delta.spawn`) with explicit isolation parameters (`mode: "isolated"`). Review skills verify prompt boundaries, and Stage 2 promotion requires automated canary token proof.
* **Risk 2: Reviewer Tool Mutability**:
  * *Failure Mode*: A Goldfish reviewer executes code editing or shell execution tools during an audit.
  * *Mitigation*: Subagent dispatch arguments explicitly whitelist read-only tools (`Read`, `Grep`, `Glob`) and disallow write or shell tools. Stage 2 verification asserts failure upon attempted write tool use.
* **Risk 3: Upstream Manifest Schema Drift**:
  * *Failure Mode*: External harnesses evolve their plugin schemas, causing syntax or install failures.
  * *Mitigation*: `tests/unit/test_harnesses.py` includes strict schema tests ensuring canonical fields match `plugin.json` across all adapters, enforcing strict JSON parsing for `.json` and YAML parsing for `.yaml`.
* **Risk 4: Premature Support Claims**:
  * *Failure Mode*: Documentation claims a harness is fully supported before live traces prove child isolation.
  * *Mitigation*: All three harnesses remain marked as **Unverified** in `TESTING.md` until Stage 2 live traces are attached.
* **Risk 5: Local Host Resource Exhaustion**:
  * *Failure Mode*: On local model runners (e.g., Ollama, vLLM, LM Studio), concurrent fan-out of multiple reviewer subagents exceeds GPU VRAM or context window limits, leading to process crashes or degraded output.
  * *Mitigation*: Subagent dispatch policies for local harnesses mandate sequential execution (concurrency limit = 1) and models with context windows of at least 32k tokens, preventing out-of-memory faults during multi-stage reviews.
* **Risk 6: Cross-Platform File Path & Shell Incompatibilities**:
  * *Failure Mode*: On Windows hosts, direct execution of POSIX shell scripts (`.sh`) fails with `WinError 193` (`%1 is not a valid Win32 application`), unescaped Windows backslashes in `CLAUDE_PLUGIN_ROOT` corrupt bash case patterns, and reading trace files with default system encodings (ANSI/CP1252) triggers `UnicodeDecodeError` on UTF-8 payload characters.
  * *Mitigation*: Dynamically discover POSIX shell binaries (`find_posix_shell()`), normalize paths passed into bash environments with forward slashes (`ROOT.as_posix()`), and mandate explicit `encoding="utf-8"` across all file reading utilities (`read_manifest`, `read_trace`, and prompt adapter tests).

---

## 9. Detailed Implementation Plan & Work Breakdown

In accordance with the [Implementation Readiness Standard](../../resources/document_standards/implementation-readiness-standard.md) and the [Re-Implementation Standard](../../resources/document_standards/re-implementation-standard.md), this plan provides deterministic, unambiguous execution instructions leaving zero architectural decisions to the implementer.

### 9.1 Target Scope

The Stage 1 delivery scope is strictly partitioned across the following files:

| Target File Path | Operation | Component Role & Implementation Rationale |
| :--- | :--- | :--- |
| `.hermes/plugin.yaml` | **Create** | Static YAML manifest adapter enabling native discovery in Hermes Agent. |
| `.openclaw/openclaw.plugin.json` | **Create** | Static strict JSON manifest adapter enabling native discovery in OpenClaw. |
| `.delta/plugin.json` | **Create** | Static strict JSON manifest adapter enabling native discovery in Delta. |
| `tests/unit/test_harnesses.py` | **Modify** | Adds polymorphic `read_manifest()` (branching on `.yaml`/`.json`) and registers new manifests in `COMPATIBILITY_MANIFESTS` for offline schema and parity enforcement. |
| `tests/integration/test_codex.py` | **Modify** | Enforces explicit UTF-8 encoding when reading retained trace JSONL files to prevent cross-platform decoding regressions on Windows hosts. |
| `docs/harnesses.md` | **Modify** | Documents install commands, manifest paths, subagent tool mappings, subagent isolation guidelines, and unverified support statuses. |
| `TESTING.md` | **Modify** | Adds Hermes Agent, OpenClaw, and Delta entries to the Harness Test Record table with Unverified status and tracking issue [#116](https://github.com/google/elephant-goldfish-model/issues/116). |
| `docs/designs/README.md` | **Modify** | Registers `multi_harness_support.md` in the technical design specification catalog. |
| `docs/designs/multi_harness_support.md` | **Create** | Canonical technical design proposal (this document). |

### 9.2 Phasing & Intermediate Checkpoints

Execution is divided into four incremental, testable phases:

* **Phase 1: Declarative Manifest Adapter Creation**
  * Create `.hermes/plugin.yaml`, `.openclaw/openclaw.plugin.json`, and `.delta/plugin.json` matching the schema specifications in Section 5.
  * *Checkpoint*: Manifest files exist on disk with valid YAML and JSON syntax.
* **Phase 2: Polymorphic Test Suite Updates & Validation**
  * Extend `tests/unit/test_harnesses.py` with polymorphic parsing supporting both strict JSON (via `json.loads`) and YAML (via `yaml.safe_load`).
  * Add all three manifest paths to `COMPATIBILITY_MANIFESTS`.
  * Enforce explicit UTF-8 decoding in `tests/integration/test_codex.py` when reading retained JSONL traces.
  * *Checkpoint*: `pytest tests/unit/test_harnesses.py` executes offline and passes 100% of tests (40 items).
* **Phase 3: Ecosystem Documentation & Index Alignment**
  * Update `docs/harnesses.md`, `TESTING.md`, and `docs/designs/README.md` to reflect new harness support and unverified Stage 1 status.
  * *Checkpoint*: `pytest tests/unit/test_link_integrity.py` passes with zero broken relative links or anchors.
* **Phase 4: Full Offline Regression Verification & Merge Readiness**
  * Execute full offline unit test suite across the repository.
  * Verify clean git status and formatting with `git diff --check`.
  * *Checkpoint*: All 50 offline unit tests pass; 100% compliance with EGM document standards.

### 9.3 Actionable Execution Steps (The Zero-Decision Rule)

#### Step 1: Manifest Construction
1. Create `.hermes/plugin.yaml` with UTF-8 encoding:
   * Top-level keys: `name: egm`, `version: 0.1.0`, `description: "..."`, `author.name: Google LLC`, `homepage: https://egm.dev`, `repository: https://github.com/google/elephant-goldfish-model`, `license: Apache-2.0`, `skills: skills`, `agents: agents`.
2. Create `.openclaw/openclaw.plugin.json` and `.delta/plugin.json` with UTF-8 encoding:
   * Strict JSON object conforming to RFC 8259 containing the identical top-level fields: `"name": "egm"`, `"version": "0.1.0"`, `"description": "..."`, `"author": {"name": "Google LLC"}`, `"homepage": "https://egm.dev"`, `"repository": "https://github.com/google/elephant-goldfish-model"`, `"license": "Apache-2.0"`, `"skills": "skills"`, `"agents": "agents"`.

#### Step 2: Test Suite Extension & Trace Ingestion Hardening (`tests/unit/test_harnesses.py`, `tests/integration/test_codex.py`)
1. In `COMPATIBILITY_MANIFESTS` (`tests/unit/test_harnesses.py`), register the relative paths for all three new adapters:
   * `".hermes/plugin.yaml"`
   * `".openclaw/openclaw.plugin.json"`
   * `".delta/plugin.json"`
2. Refactor manifest reading into a polymorphic function `read_manifest(path: str | Path) -> dict`:
   * **Path Resolution**: Resolve path relative to the repository root directory (`ROOT`) if not already absolute.
   * **File Ingestion**: Read raw file contents specifying explicit UTF-8 encoding (`read_text(encoding="utf-8")`).
   * **Extension-Based Parsing**: If the target path suffix is `.yaml` or `.yml`, deserialize using `yaml.safe_load()`. Otherwise, deserialize using strict RFC 8259 `json.loads()`.
   * **Root Object Enforcement**: Assert that the deserialized structure is an instance of `dict`, raising an `AssertionError` with the concrete type name if a non-object root (list, scalar, null, or empty file) is encountered.
   * **Backward Compatibility**: Export alias `read_json = read_manifest` to prevent regressions across existing unit test callers.
3. In `test_compatibility_metadata_matches_root`, enforce mandatory parity assertions across all registered manifests:
   * **Mandatory Metadata Fields**: Assert presence and exact value equality against root `plugin.json` for `name`, `version`, `description`, `repository`, and `license`.
   * **Author Synchronization**: Match `author` mapping or `interface.developerName` against `plugin.json` author name (`Google LLC`).
   * **Canonical Component Paths**: Verify `skills` path resolves to root `skills/` containing all 7 canonical skills (`egm-bootstrap`, `egm-brainstorm`, `egm-draft`, `egm-drift-report`, `egm-resolve`, `egm-review`, `egm-review-loop`), and `agents` path resolves to root `agents/`.
4. In `tests/unit/test_harnesses.py`, incorporate cross-platform test execution helpers:
   * Implement `find_posix_shell()` to locate `sh` or `bash` in Git for Windows installations, ensuring `run_read_hook()` can execute `.claude-plugin/hooks/allow_plugin_reads.sh` without Win32 application execution errors (`WinError 193`). Normalize plugin paths using forward slashes (`ROOT.as_posix()`) to prevent bash subshell backslash escaping issues on Windows.
   * Add `test_jsonl_preserves_unicode_separators` parameterized across Unicode separator codepoints (`\u0085`, `\u2028`, `\u2029`) to verify that JSONL records are delimited solely by literal `\n`.
   * Enforce explicit UTF-8 decoding (`read_text(encoding="utf-8")`) across adapter inspection tests.
5. In `tests/integration/test_codex.py`:
   * In `read_trace(thread_id: str)`, specify `encoding="utf-8"` in `paths[0].read_text(encoding="utf-8")` to prevent Windows ANSI/CP1252 decoding errors when ingesting retained execution traces.

#### Step 3: Documentation Alignment
1. In `docs/harnesses.md`:
   * `## Install`: Add rows for Hermes Agent (`hermes plugins install https://github.com/google/elephant-goldfish-model`), OpenClaw (`openclaw plugins install https://github.com/google/elephant-goldfish-model`), and Delta (`delta skills tap add https://github.com/google/elephant-goldfish-model`).
   * `## Manifests`: Add table entries:
     * Hermes Agent: Manifest `.hermes/plugin.yaml`, Skills `skills` (default), Subagents `Subagent spawns with isolated context and read-only tools`.
     * OpenClaw: Manifest `.openclaw/openclaw.plugin.json`, Skills `skills` (default), Subagents `Subagent spawns with fresh session and read-only tools`.
     * Delta: Manifest `.delta/plugin.json`, Skills `skills` (default), Subagents `Fresh runner subprocess with read-only tools`.
   * `## Delegation`: Add table entries:
     * Hermes Agent: Subagent tool `Native task/spawn tool (hermes.spawn)`, Named personas `Yes`, Nesting `Direct dispatch`.
     * OpenClaw: Subagent tool `Native subagent tool (sessions_spawn)`, Named personas `Yes`, Nesting `Direct dispatch / sub-session`.
     * Delta: Subagent tool `Runner delegation tool (delta.spawn)`, Named personas `Yes`, Nesting `Subprocess runner`.
   * `### Subagent Isolation Guidelines`: Add subsection mandating zero-context fresh sessions and read-only tool whitelisting (`Read`, `Grep`, `Glob`).
   * `## Support Status & Contributing Other Harnesses`: Record Hermes Agent, OpenClaw, and Delta as having manifest structures with open live trace verification gaps referencing issue [#116](https://github.com/google/elephant-goldfish-model/issues/116).
2. In `TESTING.md`:
   * `## Harness Test Record`: Add entries for Hermes Agent (0.8.2), OpenClaw (1.0.4), and Delta (0.9.0) with Date `2026-10-23`, Install status `Unverified (<command>)`, Brainstorm/Draft/Review `Pending live trace`, and Notes detailing offline verification status and tracking issue [#116](https://github.com/google/elephant-goldfish-model/issues/116).
   * Update tracking gap notes to include [#116 (Hermes, OpenClaw, Delta)](https://github.com/google/elephant-goldfish-model/issues/116).
3. In `docs/designs/README.md`:
   * Register `multi_harness_support.md` in the design index table with Document column `[multi_harness_support.md](multi_harness_support.md)<br>Manifest schemas, discovery mappings, and subagent delegation for Hermes Agent, OpenClaw, and Delta.`, Author column `[@Seburan](https://github.com/Seburan), [@yathamsriram243-blip](https://github.com/yathamsriram243-blip)`, and Primary Component `[Harness Architecture](../harnesses.md)`.

### 9.4 Test Plan

#### Happy Path Test Scenarios
1. **Manifest Schema & Parity**:
   * `test_compatibility_metadata_matches_root` executes against all 5 compatibility manifests.
   * Asserts exact string equality with root `plugin.json` for `name`, `version`, `description`, `repository`, and `license`.
   * Asserts `author.name == "Google LLC"`.
2. **Component Directory Resolution**:
   * Asserts `skills` path resolves to `skills/` containing exactly the 7 expected skills (`egm-bootstrap`, `egm-brainstorm`, `egm-draft`, `egm-drift-report`, `egm-resolve`, `egm-review`, `egm-review-loop`).
   * Asserts `agents` path resolves to `agents/`.
3. **Cross-Document Link Integrity**:
   * `test_relative_markdown_links_resolve_on_disk` parses all Markdown files in the repository.
   * Verifies all relative links and intra-document anchor slugs resolve cleanly to existing files and headers.
4. **Artifact Directory Override Documentation Invariant**:
   * `test_artifact_directory_override_is_documented_for_each_harness` verifies that `docs/harnesses.md` documents the exact configuration marker `EGM artifact directory: <path>` for prompt-level override parity with `docs/claude.md` and `docs/codex.md`.

#### Edge Cases & Failure Mode Handling
1. **Strict JSON Validation (RFC 8259)**:
   * Trailing commas, unquoted keys, single-quoted strings, or JavaScript-style comments in `.json` files trigger `json.JSONDecodeError` during `read_manifest()`.
2. **Strict YAML Validation**:
   * Tab characters for indentation or invalid syntax in `.yaml` files trigger `yaml.YAMLError` during `read_manifest()`.
3. **Non-Object Root Rejection**:
   * A manifest parsing into a list, integer, or string triggers `AssertionError` with a message identifying the unexpected type.
4. **Metadata Drift Detection**:
   * Modifying `version` or `description` in an adapter without synchronizing root `plugin.json` fails the parity assertion with an explicit drift error.
5. **Path Resolution Failure**:
   * A manifest pointing `skills` or `agents` to a non-existent or misnamed directory fails path resolution assertions.
6. **JSONL Unicode Separator Preservation**:
   * Verify that Unicode line breaks and paragraph separators (`\u0085`, `\u2028`, `\u2029`) within trace JSON payload strings do not trigger improper record splitting, ensuring JSONL records are delimited solely by literal LF (`\n`).
7. **Windows POSIX Shell Resolution Fallback**:
   * When executing on Windows environments where no POSIX shell (`sh` or `bash`) is installed or discoverable on PATH, `run_read_hook` safely skips via `pytest.skip("POSIX shell not available on Windows")` rather than failing with `WinError 193`.

---

## 10. References

* [EGM Architecture & System Lifecycle](architecture.md)
* [EGM Goldfish Review Protocol & Resolution Engine](review.md)
* [EGM Harness Architecture Guide](../harnesses.md)
* [EGM Testing Playbook](../../TESTING.md)
* [EGM Repository Root](../../README.md)
* [EGM Agent Guidelines & Contribution Taxonomy](../../AGENTS.md)
* [EGM Pull Request Template](../../.github/PULL_REQUEST_TEMPLATE.md)
* [EGM Heilmeier Catechism Standard](../../resources/document_standards/heilmeier-standard.md)
* [EGM Zoom Out Standard](../../resources/document_standards/zoom-out-standard.md)
* [EGM Implementation Readiness Standard](../../resources/document_standards/implementation-readiness-standard.md)
* [EGM Re-Implementation Standard](../../resources/document_standards/re-implementation-standard.md)
* [EGM Feature Specification Standard](../../resources/document_standards/feature-spec-standard.md)
* Dave Rensin, [Elephants, Goldfish, and the New Golden Age of Software Engineering](https://medium.com/@drensin/elephants-goldfish-and-the-new-golden-age-of-software-engineering-c33641a48874) (Medium, 2026).
* DARPA, [The Heilmeier Catechism](https://www.darpa.mil/about/heilmeier-catechism).
* Agent Plugins 1.0.0 Schema Specification, [agent-plugins.org](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json).
* Issue #116: [Support Hermes Agent, OpenClaw, and Delta](https://github.com/google/elephant-goldfish-model/issues/116).
