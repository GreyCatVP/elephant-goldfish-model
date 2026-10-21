<!--
Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0
-->

# Codex integration

## Install and locate the plugin

Install the whole plugin, including its personas and standards:

```sh
codex plugin marketplace add google/elephant-goldfish-model
codex plugin add egm@elephant-goldfish-model
```

Start a fresh session after installation. Select the installed `egm` skill
from the available skills. Use its discovered absolute `SKILL.md` path;
do not assume a particular cache directory, version, or checkout location.

From `<plugin>/skills/<skill>/SKILL.md`, the plugin root is three parent
directories above the file. Resolve bundled `agents/`, `resources/`, and
`docs/` paths against that root. Resolve `references/` against the active
skill's directory. Resolve user documents and generated artifacts against
the user's working directory. Never substitute similarly named files in the
user's project for bundled personas or standards.

## Fresh-context reviewers

Inspect the available native subagent tool schema. Tool names can be
namespaced and vary by Codex version. When `spawn_agent` exposes
`fork_context`, explicitly set `fork_context: false` for every Goldfish.
When the schema instead exposes `fork_turns`, use `fork_turns: "none"`.
This applies to reviewers launched by a synthesizer too. Use a general-purpose agent
and pass absolute paths to the persona, standards, target document, and
explicitly selected reading list. Do not pass the parent transcript, private
reasoning, or answers the document is supposed to explain.

Wait for actual reviewer completion before synthesizing findings. Propagate
failures and timeouts; a launched reviewer is not a completed review. If
nesting is unavailable, dispatch reviewers directly from the parent while
preserving the same isolation. If the available tool cannot establish a fresh
context, stop the Goldfish review and report that limitation.

Fresh conversation context does not isolate the filesystem, configured memory
services, or project instructions. Do not retrieve conversation history or
memory to supply missing design context. An isolation test should use a unique
parent-only marker and check the actual child result, not the parent's claim.

## Questions and artifacts

The shared skills' question payloads describe the intended interaction, not a
literal Codex API. Use a structured question tool only when it is available
and permitted in the current mode, mapping to its actual schema. Otherwise
ask one plain-text question and wait for the answer. Preserve the skill's
readiness and section approval gates; tool unavailability is not approval.

Link generated artifacts with absolute-path Markdown links such as
`[design draft](/absolute/project/design_draft.md)`. For paths containing
spaces use `[design draft](</absolute/my project/design_draft.md>)`.
Do not use `file://` links in Codex chat.

## Verification

Run the offline packaging checks with `pytest tests/unit`. The opt-in native
workflow tests are documented in [TESTING.md](../TESTING.md). They require
an authenticated Codex CLI and consume model usage. Installing or discovering
the plugin alone does not establish end-to-end workflow support.

## ChatGPT

Enterprise, Business, and Edu workspaces can import the plugin via Admin > Plugins > Add > Import marketplace.
Set the repository URL to `https://github.com/google/elephant-goldfish-model` and marketplace path to `.agents/plugins`.
Skills are accessible via `@egm` for direct interaction.
ChatGPT lacks subagent tools, so Goldfish reviewer isolation is not available.
Do not claim verified support for ChatGPT workflows.
