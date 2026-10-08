# Copyright 2026 Google LLC.
# SPDX-License-Identifier: Apache-2.0

"""Build an Antigravity bundle without changing shared host definitions."""

import argparse
import json
from pathlib import Path
import re
import shutil

REVIEWERS = {
    "codebase_details", "comprehension", "design_critic",
    "implementation_readiness", "structural", "style", "zoom_out",
}
REVIEWER_FRONTMATTER = (
    "tools:\n- view_file\n- grep_search\n"
    "mainAgent: false\nsubagent: true\nmodel: inherit\n"
    "commandExecutionPolicy: 'off'\n"
)
REVIEWER_PREAMBLE = (
    "Review only the supplied target and bundled standards. "
    "Return findings to the parent. Do not browse, execute commands, "
    "write files, or read conversation logs or memory. If required "
    "context is missing, report the missing input instead.\n"
)
SKILL_PREAMBLE = (
    "Resolve bundled agents, docs, and resources relative to this "
    "installed SKILL.md (plugin root is two directories above). "
    "Use fresh named EGM reviewers with invoke_subagent. Pass absolute "
    "target and standard paths, the review mode, and task restrictions "
    "in each child prompt. Never use self or an unrestricted replacement. "
    "Wait for each review stage before starting the next; parallelize "
    "only reviewers within the same stage. The parent writes reports. "
    "Stop if a required reviewer is unavailable.\n"
)


def splice(path: Path, extra_frontmatter: str, preamble: str) -> None:
    header, body = path.read_text(encoding="utf-8").split("\n---\n", 1)
    header = re.sub(r"^disable-model-invocation:.*\n", "", header + "\n",
                    flags=re.M)
    path.write_text(header + extra_frontmatter + "---\n\n" + preamble + body,
                    encoding="utf-8")


def build(source: Path, output: Path) -> None:
    if output.exists():
        raise FileExistsError(f"Output already exists: {output}")
    output.mkdir(parents=True)
    for directory in ("skills", "agents", "resources", "docs"):
        shutil.copytree(source / directory, output / directory)
    manifest = json.loads((source / "plugin.json").read_text())
    (output / "plugin.json").write_text(json.dumps({
        "name": manifest["name"],
        "description": manifest["description"],
    }, indent=2) + "\n")
    for path in (output / "agents").glob("*.md"):
        if path.stem in REVIEWERS:
            splice(path, REVIEWER_FRONTMATTER, REVIEWER_PREAMBLE)
    for path in (output / "skills").glob("*/SKILL.md"):
        splice(path, "", SKILL_PREAMBLE)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    build(Path(__file__).resolve().parents[1], args.output)
