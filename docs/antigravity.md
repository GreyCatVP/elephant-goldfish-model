<!--
Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0
-->

# Antigravity CLI

Build a host-specific bundle before installation:

```bash
python -m pip install -r requirements-dev.txt
python tools/build_antigravity.py /tmp/egm-antigravity
agy plugin validate /tmp/egm-antigravity
agy plugin install /tmp/egm-antigravity
```

Choose a new output directory outside the checkout. The builder refuses to
overwrite existing files. It copies skills, personas, standards, and references;
shared source files and other hosts' manifests are unchanged.

The bundle makes skills discoverable and limits the seven reviewer personas
to `view_file` and `grep_search`. Reviewers cannot use shell, web, or write
tools from that allowlist. Host-injected communication and MCP tools may still
be available; disable unrelated MCP servers in the host for offline or
sensitive reviews. The parent writes reports. Bootstrap and synthesis
orchestrators retain their original definitions. This is a tool restriction,
not a filesystem sandbox; configure host read scopes for sensitive projects.

Start a fresh session after installing. Invoke `/egm-brainstorm`,
`/egm-draft`, or `/egm-review`; resolve resources relative to the skill path
provided by the host. Do not guess a cache directory. Pass absolute target
and standard paths plus task restrictions to each new reviewer, and wait for
each stage to finish. Do not replace a missing reviewer with `self`.

Official references: [plugins](https://antigravity.google/docs/plugins),
[skills](https://antigravity.google/docs/skills/), and
[subagent tool allowlists](https://antigravity.google/docs/subagents/).
