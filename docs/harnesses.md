<!--
Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0
-->

# Harnesses

EGM is one set of skills and personas. This repository serves as the
plugin source for each supported harness. No harness gets a fork of the skill
text.

## Install

| Harness | Install |
| --- | --- |
| Antigravity | `/plugin`, then install from `https://github.com/google/elephant-goldfish-model` |
| Gemini CLI | `gemini extensions install https://github.com/google/elephant-goldfish-model` |

Install the whole plugin. Skill-only installers that copy `skills/` alone
break EGM, because the skills read `agents/` and
`resources/document_standards/` at run time.

## Manifests

| Harness | Manifest | Skills | Subagents |
| --- | --- | --- | --- |
| Antigravity | `plugin.json` | `skills/` (default) | `agents/` (default) |
| Gemini CLI | `gemini-extension.json` | `skills/` (default) | `agents/` (default) |

Persona prompts live in `agents/`, the directory Antigravity and Gemini CLI
scan for subagents. Each persona has `name` and `description` frontmatter, so
harnesses that load `agents/*.md` register them as named subagents
(`egm-design`, `egm-zoom-out`, and so on).

## Delegation

Skills say "spawn a subagent" and name a persona. Each harness maps that
phrase to its own tool:

| Harness | Subagent tool | Named personas | Nesting |
| --- | --- | --- | --- |
| Antigravity | `invoke_subagent` | Yes | Yes |
| Gemini CLI | Subagents | Yes | Not verified |

Where a harness has no named persona, the skill spawns a general-purpose
subagent and tells it to read `agents/<file>.md` first. If a harness cannot
nest subagents, use direct dispatch instead of the synthesizer.

A Goldfish review needs a fresh context. If a harness has no subagent tool,
the review skills stop instead of running in the same context.

## Support Status & Contributing Other Harnesses

Our initial release supports **Antigravity** and **Gemini CLI**. We welcome
contributors who want to help add and verify support for other agent harnesses!

A harness counts as supported after `/egm-brainstorm`, `/egm-draft`, and
`/egm-review` run end to end on it. To contribute support for another harness,
see [CONTRIBUTING.md](../CONTRIBUTING.md) and record each run in
[TESTING.md](../TESTING.md).
