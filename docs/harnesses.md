<!--
Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0
-->

# Harnesses

EGM is one set of skills and personas. This repository is also the
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
break EGM, because the skills read `agents/` and
`resources/document_standards/` at run time.

## Manifests

Root `plugin.json` is the canonical source for plugin identity, version,
description, and publisher metadata. It declares the portable Agent Plugins
1.0.0 schema. Update shared values there first, then update the compatibility
manifests; unit tests reject metadata drift. Keep platform-specific fields in
their existing manifests until installation tests justify removing them.

Marketplace files are discovery catalogs pointing to this package, not copies
of its skills. In particular, `.agents/plugins/` contains the Codex catalog,
while `agents/` contains reviewer personas. All hosts share the same `skills/`,
`agents/`, and `resources/` content.

| Harness | Manifest | Skills | Subagents |
| --- | --- | --- | --- |
| Claude Code | `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` | `skills/` (default) | Listed file by file in `plugin.json` `agents` |
| OpenAI Codex | `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json` | `skills` path | Not shipped; general-purpose subagent reads the persona file |
| Cursor | `.cursor-plugin/plugin.json`, `.cursor-plugin/marketplace.json` | `skills` path | Not shipped; general-purpose subagent reads the persona file |
| Gemini CLI | `gemini-extension.json` | `skills/` (default) | `agents/` (default) |
| Antigravity | `plugin.json` | `skills/` (default) | `agents/` (default) |

Persona prompts live in `agents/`, the directory Gemini CLI and Antigravity
scan for subagents. Each persona has `name` and `description` frontmatter, so
harnesses that load `agents/*.md` register them as named subagents
(`egm-design`, `egm-zoom-out`, and so on).

When you add a persona, also add its path to `agents` in
`.claude-plugin/plugin.json`. Claude Code does not scan a directory there.

## Delegation

Skills say "spawn a subagent" and name a persona. Each harness maps that
phrase to its own tool:

| Harness | Subagent tool | Named personas | Nesting |
| --- | --- | --- | --- |
| Claude Code | Agent (Task) tool | Yes | Up to 3 levels by default |
| OpenAI Codex | Native spawn/wait tools; inspect the available schema | No | Detect at runtime; direct dispatch fallback |
| Cursor | Subagents | No | Not verified |
| Gemini CLI | Subagents | Yes | Not verified |
| Antigravity | `invoke_subagent` | Yes | Yes |

Where a harness has no named persona, the skill spawns a general-purpose
subagent and tells it to read `agents/<file>.md` first. If a harness cannot
nest subagents, use direct dispatch instead of the synthesizer.

A Goldfish review needs a fresh context. If a harness has no subagent tool,
the review skills stop instead of running in the same context. ChatGPT web
Skills fall into this category, so EGM does not support ChatGPT web.

## Common pitfalls

- **Testing the wrong copy:** An existing installation can take precedence over
  a local candidate. Use a uniquely named test plugin where supported and
  verify the paths actually read by the agent.
- **Incomplete installation:** Keep the whole bundle together. Skills need
  personas, reference files, and document standards; copying only skill files
  is insufficient.
- **Discovery versus invocation:** Skills with `disable-model-invocation: true`
  may be absent from automatic discovery. Invoke them explicitly using the
  host's command syntax before concluding that installation failed.
- **Resource lookup:** Resolve bundled files from the installed plugin, and
  keep generated artifacts in the user's project. Do not guess cache versions.
  See [TESTING.md](../TESTING.md#interpreting-native-test-results) for how to
  record an explicit-path workaround.
- **Isolation limits:** Fresh subagent context does not imply filesystem
  isolation or exclusion of all host instructions. Verify the host's behavior.
- **Task constraints:** Pass offline, read-only, and resource-scope requirements
  explicitly to each delegated reviewer. Check its tool use; parent instructions
  alone do not establish that a child followed those restrictions.

For Codex, read [Codex integration](codex.md) for installed-resource paths,
explicit fresh-context delegation, question-tool fallbacks, and artifact links.

## Support status

A harness counts as supported after `/egm-brainstorm`, `/egm-draft`, and
`/egm-review` run end to end on it. Record each run in
[TESTING.md](../TESTING.md).
