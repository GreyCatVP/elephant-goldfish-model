# Directory packages

Build a runtime folder and ZIP using only Python's standard library:

```sh
python3 scripts/pack_plugin.py --target claude --output /tmp/egm-release
python3 scripts/pack_plugin.py --target openai --output /tmp/egm-release
```

The output contains `egm-claude/` and `egm-claude.zip`, or `egm-openai/`
and `egm-openai.zip`. Existing outputs are refused. ZIP entry order,
timestamps, and permissions are fixed; identical inputs produce identical
archives on the same Python/zlib runtime.

The allowlist includes skill instructions and references, personas, standards,
runtime guides, manifests, and icons. It excludes the site, tests, workflows,
marketplace catalogs, hooks, and build tools. Claude retains its native agent
adapters; OpenAI excludes Claude components. Runtime files are nonexecutable.
Symlinked runtime paths and escaping manifest references are rejected.

For Anthropic, check the generated `egm-claude/` into a dedicated repository
subfolder and submit that subfolder through the directory portal. Regenerate
it after source changes. For OpenAI, upload `egm-openai.zip`. Build output
alone does not establish installation, workflow support, or directory approval.
