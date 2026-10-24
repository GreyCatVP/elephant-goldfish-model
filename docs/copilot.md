<!-- Copyright 2026 Google LLC. SPDX-License-Identifier: Apache-2.0 -->

# GitHub Copilot CLI integration

Experimental adapter for [issue #147](https://github.com/google/elephant-goldfish-model/issues/147).
Workflow execution and reviewer isolation remain unverified. This guide does
not establish support for Copilot in VS Code or the cloud agent.

## Interface and installation

The offline reference version is GitHub Copilot CLI **1.0.82**.
Use the existing Agent Plugins 1.0 root `plugin.json`. Copilot-specific profiles
live in `com.github.copilot/agents/`. The shared skills, personas, and standards
remain in `skills/`, `agents/`, and `resources/`.

Use a complete checkout at a fixed candidate commit. Keep that checkout while
the session runs. Do not copy only `skills/` or install the profile directory alone.
The root manifest takes precedence over the Claude compatibility manifest.
No Copilot hooks, MCP servers, or replacement manifest are required.

Set `EGM_ROOT` to the absolute path of the candidate checkout:

```sh
EGM_ROOT=/absolute/path/to/elephant-goldfish-model
git -C "$EGM_ROOT" rev-parse HEAD
copilot --version
COPILOT_OFFLINE=true copilot --plugin-dir "$EGM_ROOT" plugin list
```

The last command must list `egm` under external plugins. It checks registration,
not reviewer execution. For a separate profile, set `COPILOT_HOME` to a new
directory. This does not disable every user-level skill or project instruction.
Inspect the host inventories before any live test.

After explicit authorization for model usage, start Copilot from the target project:

```sh
copilot --plugin-dir "$EGM_ROOT" --add-dir "$EGM_ROOT" --agent egm
```

In the first message, supply the absolute package root and requested skill:

```text
EGM package root: /absolute/path/to/elephant-goldfish-model
Read that package's docs/copilot.md and run egm-brainstorm.
EGM artifact directory: .dev/docs
```

Use `egm-draft` or `egm-review` in later requests. Provide the target document
for review. Use the `egm` entry agent so the host mapping loads before a skill.
Selecting a reviewer as the main session does not establish a fresh Goldfish context.
Check `/agent` for name conflicts before use; personal profiles can override package profiles.

The verified offline path uses `--plugin-dir`. Persistent installation through
`copilot plugin install` remains unverified. Version 1.0.82 help does not document
local-path installation, although current GitHub documentation does. Do not infer
that a newer command interface works on this version.

## Resource paths

Resolve the package root from the mounted checkout or the native plugin inventory.
For a discovered `skills/<skill>/SKILL.md`, move three parent directories upward.
Read the guide and canonical skill from that root before delegation.

- Resolve `agents/`, `resources/`, and `docs/` against the package root.
- Resolve a skill's `references/` against that skill's directory.
- Resolve user documents against the project working directory.
- Pass absolute paths to reviewers, including the package root, target, and standards.
- Preserve spaces and Unicode characters in paths. Do not split paths on whitespace.
- Stop if any required resource is unavailable. Never substitute a project file.

`<EGM_ROOT>` in a profile is a task-supplied path, not an environment expansion.
This adapter does not assume that Copilot expands variables inside Markdown bodies.

## Native delegation

Use Copilot's native custom-agent delegation tool. Inspect its exposed schema.
Select the registered profile by its exact name; do not invent tool arguments.
The entry profile permits `agent` for delegation and `edit` for artifacts.
Each reviewer permits only `read` and `search`. Reviewers cannot delegate or write reports.

| Profile | Canonical persona |
| --- | --- |
| `egm-design` | `agents/design_critic.md` |
| `egm-codebase-details` | `agents/codebase_details.md` |
| `egm-comprehension` | `agents/comprehension.md` |
| `egm-implementation-readiness` | `agents/implementation_readiness.md` |
| `egm-structural` | `agents/structural.md` |
| `egm-style` | `agents/style.md` |
| `egm-zoom-out` | `agents/zoom_out.md` |

Start a new native child for every reviewer invocation, including repeat reviews.
Use a task that contains only the requested mode, target, line ranges, persona,
standards, and explicit reading list. Do not forward the conversation, private
rationale, memory, previous findings, or answers the target should explain.

Use direct dispatch for the shared skills' synthesizer steps. Read the canonical
`agents/synthesizer.md` for reviewer selection and report format. The main session
collects results and writes artifacts. Do not attempt nested delegation or register
an unrestricted synthesizer. Bootstrap workers are outside this adapter's verified scope.

Keep `include-custom-instructions: false` for reviewers. Current GitHub documentation
describes this setting for delegated children, not agents selected as the main session.
The local version's enforcement is unverified. A separate context window alone
does not prove that instructions, memory, or shared files are isolated.

Wait for each native completion before synthesis. Check required resource reads
in host records where available. A missing child, read failure, timeout, or denied
tool makes that stage incomplete. Stop and report the limitation. Never simulate
a child or treat missing findings as a passing result.

## Human gates and artifacts

Follow the canonical skill's approval steps and stage order. Use one plain-text
question and wait when a structured question tool is unavailable. A missing tool
does not grant approval. Do not enable autopilot to bypass these gates.

Write artifacts to the working directory unless the user supplies
`EGM artifact directory: <path>`. Resolve relative artifact paths against that
working directory. Preserve the skill's filenames and report their final paths.
Keep artifact writes in the main session; reviewers return findings only.

## Validation and remaining limits

Run `pytest tests/unit/test_copilot_adapter.py` and `pytest tests/unit` offline.
The host-specific tests check profiles, path resolution, and canonical resource
preservation in a relocated package. They do not call a model.

With CLI 1.0.82 installed, include its offline registration check:

```sh
EGM_COPILOT_OFFLINE=1 pytest tests/unit
```

On 2026-10-24, CLI 1.0.82 registered the mounted root package with
`COPILOT_OFFLINE=true` and a disposable `COPILOT_HOME`. Registration does not prove
profile discovery, skill execution, tool denial, or context isolation.
On this version, `copilot --plugin-dir "$EGM_ROOT" skill list` did not list the
mounted package's skills. Native skill and profile discovery remain unverified.

Before a support claim, run the existing brainstorm, draft, and review scenarios
from each skill's `test_scenarios.yaml` with explicit model-use authorization.
Record these outcomes separately:

1. Installation: candidate SHA, package identity, complete resources, and loaded profiles.
2. Workflow: host version, model identifier, date, native child starts and completions,
   required reads, artifact paths, and a real human approval pause.
3. Isolation: a random parent-only marker, actual child context, injected instructions,
   memory and MCP exposure, and attempted writes to a disposable fixture.

Inspect tool records to verify write denial. A reviewer promise is not enforcement.
If records are unavailable, retain an unverified result. Read access to shared files
can expose prior findings; fresh context is not a filesystem sandbox.

Cursor local Agent and Grok Bot require separate assessment under
[issue #145](https://github.com/google/elephant-goldfish-model/issues/145).
This Copilot adapter provides no evidence of support for either surface.

## Official references

- [Plugin format and precedence](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference)
- [Custom agents and instruction inheritance](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-custom-agents-for-cli)
- [Agent tools and aliases](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference)

These references describe capabilities. They are not EGM runtime test evidence.
