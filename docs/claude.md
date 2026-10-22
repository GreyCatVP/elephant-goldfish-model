<!--
Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0
-->

# Claude Code integration

Use Claude Code 2.1.271 or later for `omitClaudeMd` support. Older versions
must not be treated as verified Goldfish isolation environments.

## Invocation and resources

```sh
claude plugin marketplace add google/elephant-goldfish-model
claude plugin install egm@elephant-goldfish-model
```

Enable the installed plugin with `claude plugin enable egm@elephant-goldfish-model`.
Start messages with `/egm:egm-brainstorm`, `/egm:egm-draft`, or `/egm:egm-review`.
Skills retain `disable-model-invocation: true`: their absence from automatic
skill discovery is expected. Keep drafting and orchestration in the main context.

Claude substitutes `${CLAUDE_PLUGIN_ROOT}` in plugin skill and agent bodies. Use that
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

Claude adapters in `.claude-plugin/agents/` declare `tools: [Read, Grep, Glob]`,
`model: inherit`, and `omitClaudeMd: true`. Each adapter reads its canonical
persona from `agents/` through `${CLAUDE_PLUGIN_ROOT}`. Keep Claude tool names
out of shared persona frontmatter: other hosts can interpret `tools` themselves.
Reviewers cannot edit files or run shell commands, and no persistent `memory`
is configured. Bootstrap and synthesis orchestrators keep their capabilities.
The parent handles fixes.

Normal subagents exclude parent conversation history. `omitClaudeMd` additionally
excludes user/project/local instruction files, but managed policies still apply.
This is context and tool isolation, not filesystem isolation: reviewers can read
accessible files. Pass any required review constraints explicitly and keep
unrelated history, logs, and memory out of the review task.

For local testing, load a uniquely named copy with `claude --plugin-dir <copy>`
to avoid confusion with an already installed `egm` plugin. Validate it with
`claude plugin validate <copy>/.claude-plugin/plugin.json`.

## Claude Cowork

Claude Cowork uses the same `.claude-plugin` package as Claude Code.
Install the plugin from claude.ai/plugins or the Cowork plugin panel via marketplace `google/elephant-goldfish-model`.
For a candidate package, Customize > Plugins > Add plugin > Upload plugin
accepts a ZIP containing the Claude manifest, adapters, and shared runtime files.
Install it and choose **Try in chat**. Record whether the resulting task runs
locally or in the cloud; the tested desktop surface used cloud tasks.
Verify resource resolution and reviewer tools in the actual Cowork session.
Installation alone does not establish that Claude Code's subagent settings or
`${CLAUDE_PLUGIN_ROOT}` substitution work on that surface.
Local testing with `claude --plugin-dir` is supported in Claude Code only.

References: [plugin paths](https://code.claude.com/docs/en/plugins-reference),
[skill invocation](https://code.claude.com/docs/en/skills), and
[subagent context and tools](https://code.claude.com/docs/en/sub-agents).
