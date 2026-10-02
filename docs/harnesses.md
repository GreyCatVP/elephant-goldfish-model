<!--
Copyright 2026 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Harnesses

EGM is one set of skills, personas, and rules. This repository is also the
plugin marketplace for each supported harness. No harness gets a fork of the
skill text.

## Install

| Harness | Install |
| --- | --- |
| Claude Code | `/plugin marketplace add google/elephant-goldfish-model`, then `/plugin install egm@elephant-goldfish-model` |
| OpenAI Codex | `codex plugin marketplace add google/elephant-goldfish-model`, then install `egm` from `/plugins` |
| Cursor | Add `https://github.com/google/elephant-goldfish-model` as a team marketplace, then install `egm` |
| Gemini CLI | `gemini extensions install https://github.com/google/elephant-goldfish-model` |
| Antigravity | `/plugin`, then install from `https://github.com/google/elephant-goldfish-model` |

Install the whole plugin. Skill-only installers that copy `skills/` alone
break EGM, because the skills read `personas/`, `rules/`, and
`resources/document_standards/` at run time.

## Manifests

| Harness | Manifest | Skills | Subagents |
| --- | --- | --- | --- |
| Claude Code | `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` | `skills/` (default) | Listed file by file in `plugin.json` `agents` |
| OpenAI Codex | `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json` | `skills` path | Not shipped; general-purpose subagent reads the persona file |
| Cursor | `.cursor-plugin/plugin.json`, `.cursor-plugin/marketplace.json` | `skills` path | Not shipped; general-purpose subagent reads the persona file |
| Gemini CLI | `gemini-extension.json` | `skills/` (default) | `agents/` (default) |
| Antigravity | `plugin.json` | `skills/` (default) | `agents/` (default) |

`agents` is a symlink to `personas/`. Each persona has `name` and
`description` frontmatter, so harnesses that load `agents/*.md` register them
as named subagents (`egm-design`, `egm-zoom-out`, and so on). On Windows,
enable `core.symlinks` before you clone.

When you add a persona, also add its path to `agents` in
`.claude-plugin/plugin.json`. Claude Code does not scan a directory there.

## Delegation

Skills say "spawn a subagent" and name a persona. Each harness maps that
phrase to its own tool:

| Harness | Subagent tool | Named personas | Nesting |
| --- | --- | --- | --- |
| Claude Code | Agent (Task) tool | Yes | Up to 3 levels by default |
| OpenAI Codex | `spawn_agent`, `wait_agent` | No | Not verified |
| Cursor | Subagents | No | Not verified |
| Gemini CLI | Subagents | Yes | Not verified |
| Antigravity | `invoke_subagent` | Yes | Yes |

Where a harness has no named persona, the skill spawns a general-purpose
subagent and tells it to read `personas/<file>.md` first. If a harness cannot
nest subagents, use direct dispatch instead of the synthesizer.

A Goldfish review needs a fresh context. If a harness has no subagent tool,
the review skills stop instead of running in the same context. ChatGPT web
Skills fall into this category, so EGM does not support ChatGPT web.

## Support status

A harness counts as supported after `/egm-brainstorm`, `/egm-draft`, and
`/egm-review` run end to end on it. Record each run in
[TESTING.md](../TESTING.md).
