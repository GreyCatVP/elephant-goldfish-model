<!--
Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0
-->

# Claude Code integration

Use Claude Code 2.1.271 or later for `omitClaudeMd` support. Older versions
must not be treated as verified Goldfish isolation environments.

## Invocation and resources

Enable the installed plugin with `claude plugin enable egm@elephant-goldfish-model`.
Start messages with `/egm:egm-brainstorm`, `/egm:egm-draft`, or `/egm:egm-review`.
Skills retain `disable-model-invocation: true`: their absence from automatic
skill discovery is expected. Keep drafting and orchestration in the main context.

Claude substitutes `${CLAUDE_PLUGIN_ROOT}` in plugin skill bodies. Use that
resolved absolute root for `agents/`, `resources/`, and `docs/`; use the invoked
skill's directory for its `references/`. This standalone guide is read as a file,
so placeholders here are explanatory: use the root already resolved in the
invoked skill. Never guess a cache version or search another installed copy.
Review targets and generated artifacts belong to the user's workspace, not the
plugin cache. Pass absolute resource and target paths to each reviewer.

## Reviewer isolation

Spawn a new native Agent of the plugin's registered reviewer type for each
independent review, for example `egm:egm-zoom-out`. Do not fork the conversation
or resume a previous reviewer. Provide only the task, target, persona/standard
paths, and explicitly supplied Goldfish context; do not copy parent deliberation.

The Claude-only adapters in `integrations/claude/agents/` declare
`tools: Read, Grep, Glob`, `model: inherit`, and `omitClaudeMd: true`.
The Claude manifest points to these adapters, which read the canonical shared
personas in `agents/`. Shared persona frontmatter stays unchanged for other hosts.
The adapters cannot edit files or execute shell commands through
their tool set. No persistent `memory` is configured. Bootstrap and synthesis
orchestrators retain their existing capabilities. The parent handles fixes.

Normal subagents exclude parent conversation history. `omitClaudeMd` additionally
excludes user/project/local instruction files, but managed policies still apply.
This is context and tool isolation, not filesystem isolation: reviewers can read
accessible files. Pass any required review constraints explicitly and keep
unrelated history, logs, and memory out of the review task.

For local testing, load a uniquely named copy with `claude --plugin-dir <copy>`
to avoid confusion with an already installed `egm` plugin. Validate it with
`claude plugin validate <copy>/.claude-plugin/plugin.json`.

References: [plugin paths](https://code.claude.com/docs/en/plugins-reference),
[skill invocation](https://code.claude.com/docs/en/skills), and
[subagent context and tools](https://code.claude.com/docs/en/sub-agents).
