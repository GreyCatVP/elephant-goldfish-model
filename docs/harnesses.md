# Harnesses

EGM is one set of skills and personas. This repository serves as the
plugin source for each supported harness. No harness gets a fork of the skill
text.

## Install

| Harness | Install |
| --- | --- |
| Antigravity | `/plugin`, then install from `https://github.com/google/elephant-goldfish-model` |
| Gemini CLI | `gemini extensions install https://github.com/google/elephant-goldfish-model` |
| Claude Code | `/plugin marketplace add google/elephant-goldfish-model`, then `/plugin install egm@elephant-goldfish-model` |

Install the whole plugin. Skill-only installers that copy `skills/` alone
break EGM, because the skills read `agents/` and
`resources/document_standards/` at run time.

## Manifests

| Harness | Manifest | Skills | Subagents |
| --- | --- | --- | --- |
| Antigravity | `plugin.json` | `skills/` (default) | `agents/` (default) |
| Gemini CLI | `gemini-extension.json` | `skills/` (default) | `agents/` (default) |
| Claude Code | `.claude-plugin/plugin.json` | `skills/` (default) | `.claude-plugin/agents/` |

Persona prompts live in `agents/`, the directory Antigravity and Gemini CLI
scan for subagents. Each persona has `name` and `description` frontmatter, so
harnesses that load `agents/*.md` register them as named subagents
(`egm-design`, `egm-zoom-out`, and so on).

Claude Code registers them through short wrappers in `.claude-plugin/agents/`
instead, as `egm:egm-design` and so on. Each wrapper points at its persona in
`agents/` and adds Claude Code tool limits; see [Claude Code](#claude-code).

## Delegation

Skills say "spawn a subagent" and name a persona. Each harness maps that
phrase to its own tool:

| Harness | Subagent tool | Named personas | Nesting |
| --- | --- | --- | --- |
| Antigravity | `invoke_subagent` | Yes | Yes |
| Gemini CLI | Subagents | Yes | Not verified |
| Claude Code | `Agent` | Yes | Yes |

Where a harness has no named persona, the skill spawns a general-purpose
subagent and tells it to read `agents/<file>.md` first. If a harness cannot
nest subagents, use direct dispatch instead of the synthesizer.

A Goldfish review needs a fresh context. If a harness has no subagent tool,
the review skills stop instead of running in the same context.

## Claude Code

Claude Code installs the plugin outside the user's project. When a prompt
starts with `/egm:`, a hook in `.claude-plugin/plugin.json` tells the agent the
plugin root and points it here. The rest of this section is for that agent.

*   **Paths**: Read `agents/`, `resources/`, and `skills/` from the plugin root.
    Everything else, including `docs/designs/` and every file the skills write,
    is in the working directory. A skill's `references/` folder is relative to
    the skill's own directory.
*   **Commands**: Claude Code names skill commands after their folders, so
    `/egm-review` in a skill means `/egm:egm_review`.
*   **Subagents**: Start each one with a new `Agent` call whose
    `subagent_type` is `egm:<persona name>`, for example `egm:egm-zoom-out`.
    Never fork the conversation or continue an earlier reviewer with
    `SendMessage`; both carry the Elephant's history into the review. Pass the
    task, absolute paths to the document and standards, and only the context
    the skill says to pass. To run reviewers in parallel, send several `Agent`
    calls in one message.
*   **Chained skills**: The skills set `disable-model-invocation: true`, so the
    `Skill` tool refuses when one skill invokes another (for example
    `egm-review` invoking `egm-review-loop` or `egm-resolve`). Read that
    skill's `SKILL.md` from the plugin root and follow it in the same thread.
*   **Questions**: Use `AskUserQuestion` with one question per call and
    `multiSelect: false`. Keep the skill's options and order, use each
    option's text as its description with a short label, and don't add
    "(Recommended)". The automatic "Other" answer is the user's write-in.
*   **Runtime subagents**: Claude Code cannot register the bootstrap
    `goldfish-explorer` scout at runtime. Use a new `Explore` agent and put the
    scout's instructions and output schema in its prompt.

The reviewer wrappers allow only `Read`, `Grep`, and `Glob`, and set
`omitClaudeMd: true` (Claude Code 2.1.271 or later), so reviewers cannot edit
files or run commands and do not load the user's or project's `CLAUDE.md`. The
synthesizer may also spawn agents and write its report. These keys live in
`.claude-plugin/agents/`, not `agents/`, because Antigravity and Gemini CLI read
`tools` as a list of their own tool names.

## Support Status & Contributing Other Harnesses

Our initial release officially supports **Antigravity** and **Gemini CLI**.
**Claude Code** support is described [above](#claude-code). We welcome
contributors who want to help add and verify support for other agent harnesses!

### Contributing Support for New Harnesses

A harness counts as supported after `/egm-brainstorm`, `/egm-draft`, and
`/egm-review` run end to end through its plugin install. When contributing
support for another harness:

1. Add the appropriate manifest or configuration file to the repository root
   (e.g., matching the harness's plugin/extension standard).
2. Document install steps, manifest mapping, and delegation mechanics in this guide
   (`docs/harnesses.md`).
3. Verify that `/egm-brainstorm`, `/egm-draft`, and `/egm-review` run end to end,
   and attach verification notes or execution transcripts in your Pull Request description
   (as outlined in the [Pull Request Template](../.github/PULL_REQUEST_TEMPLATE.md)).
