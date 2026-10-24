# Multi-Harness Support: Hermes Agent, OpenClaw, and Delta

* **Authors:** Sriram (@Seburan), yathamsriram243-blip (@yathamsriram243-blip)
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

This document defines the architectural specification, manifest schemas, directory discovery mappings, subagent delegation mechanics, and the two-stage rollout criteria required to support Hermes Agent, OpenClaw, and Delta in EGM.

---

## 2. Heilmeier Catechism Analysis

| Catechism Dimension | Project Evaluation |
| :--- | :--- |
| **Objective** | Provide declarative manifest adapters and documented delegation contracts so users of Hermes Agent, OpenClaw, and Delta can install EGM and run workflows without modifying skill text. |
| **State of the Art** | EGM supports Antigravity, Claude, and Codex. Other harnesses require manual file copies, which violate EGM's single-source principle and break relative links to personas and document standards. |
| **New Approach** | Introduce lightweight, static manifest adapters (`.hermes/plugin.yaml`, `.openclaw/openclaw.plugin.json`, `.delta/plugin.json`) that point directly to shared `skills/` and `agents/` directories without runtime transpilation or build steps. |
| **Impact** | Enables users of OpenClaw, Hermes Agent, and Delta to run EGM spec-driven workflows with guaranteed reviewer isolation, expanding EGM's ecosystem footprint. |
| **Risks & Payoffs** | Primary risks are upstream manifest schema drift and accidental parent context leakage. Payoffs are zero code duplication and platform-agnostic specification engineering. |
| **Cost & Token Economics** | Zero additional runtime dependencies, background daemon processes, or cloud services. Manifest parsing overhead is under 5ms, and unit tests execute in under 10 seconds offline. |
| **Timeline & Staging** | Two-stage lifecycle: **Stage 1 (this proposal)** establishes design and manifest contracts. **Stage 2** captures live execution traces and promotes harness status from Unverified to Pass. |
| **Metrics & Verification** | Stage 1 requires 100% pass on offline schema synchronization and strict JSON/YAML validation (`pytest tests/unit/test_harnesses.py`). Stage 2 requires verified child session transcripts proving zero parent context leak. |

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
  * Delta: Runner delegation subprocess
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
| **Manifest Format** | YAML (`yaml.safe_load`) | JSON (`json.loads`, strict) | JSON (`json.loads`, strict) |
| **Skill Discovery Path** | `skills` (`skills/`) | `skills` (`skills/`) | `skills` (`skills/`) |
| **Persona Discovery Path**| `agents` (`agents/`) | `agents` (`agents/`) | `agents` (`agents/`) |
| **Subagent Tool Mapping** | Hermes task tool (`hermes.spawn`) | Native subagent tool (`sessions_spawn`) | Delta runner delegation |
| **Context Isolation Guarantee** | Clean subprocess / isolated thread | Isolated child session (`isolated`) | Fresh runner subprocess |
| **Tool Restriction Policy** | Read-only tools (`Read`, `Grep`, `Glob`) | Read-only tools (`Read`, `Grep`, `Glob`) | Read-only tools (`Read`, `Grep`, `Glob`) |
| **Install Command** | `hermes plugins install <repo>` | `openclaw plugins install <repo>` | `delta skills tap add <repo>` |
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

In accordance with EGM's contribution guidelines (`AGENTS.md`), harness expansion follows a strict two-stage lifecycle:

### Stage 1: Design Specification & Manifest Contracts (Current PR #119)
* **Deliverable**: This design document (`docs/designs/multi_harness_support.md`), manifest adapters (`.hermes/plugin.yaml`, `.openclaw/openclaw.plugin.json`, `.delta/plugin.json`), documentation updates (`docs/harnesses.md`), and offline unit tests (`tests/unit/test_harnesses.py`).
* **Support Status**: Hermes Agent, OpenClaw, and Delta are explicitly recorded as **Unverified** in `TESTING.md` and `docs/harnesses.md`.
* **Prerequisites for Merge**: All offline unit tests pass, links pass integrity validation, and maintainer design consensus is reached.

### Stage 2: Live Verification & Support Promotion (Follow-up PR)
* **Deliverable**: Submission of live execution evidence promoting the harness status from Unverified to Pass in `TESTING.md`.
* **Required Evidence Checklist for Each Harness**:
  1. **Installation Log**: Clean terminal output of the plugin install command (`openclaw plugins install`, `hermes plugins install`, or `delta skills tap add`).
  2. **Workflow Execution**: Verified artifacts from end-to-end execution of `/egm-brainstorm`, `/egm-draft`, and `/egm-review`.
  3. **Isolation Proof**: Child session trace confirming:
     * Zero parent conversation leakage.
     * Invocation of reviewer subagents under read-only tool constraints (`Read`, `Grep`, `Glob`).
     * Absence of write or shell execution permissions.

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

---

## 8. Risks, Failure Modes & Mitigations

* **Risk 1: Subagent Parent Context Leaks**:
  * *Failure Mode*: A child session inherits the parent chat conversation, violating the zero-context Goldfish requirement.
  * *Mitigation*: Subagent dispatch policies specify clean child boundaries via native tools (e.g. `sessions_spawn` with isolated boundary) or fresh subprocesses. Review skills verify prompt boundaries and halt if parent context is detected.
* **Risk 2: Reviewer Tool Mutability**:
  * *Failure Mode*: A Goldfish reviewer executes code editing or shell execution tools during an audit.
  * *Mitigation*: Subagent dispatch policies strictly restrict reviewer tools to read-only capabilities (`Read`, `Grep`, `Glob`).
* **Risk 3: Upstream Manifest Schema Drift**:
  * *Failure Mode*: External harnesses evolve their plugin schemas, causing syntax or install failures.
  * *Mitigation*: `tests/unit/test_harnesses.py` includes strict schema tests ensuring canonical fields match `plugin.json` across all adapters, enforcing strict JSON parsing for `.json` and YAML parsing for `.yaml`.
* **Risk 4: Premature Support Claims**:
  * *Failure Mode*: Documentation claims a harness is fully supported before live traces prove child isolation.
  * *Mitigation*: All three harnesses remain marked as **Unverified** in `TESTING.md` until Stage 2 live traces are attached.
