# Copyright 2026 Google LLC.
# SPDX-License-Identifier: Apache-2.0

"""Claude reviewer frontmatter contracts."""

from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
REVIEWERS = (
    "codebase_details", "comprehension", "design_critic",
    "implementation_readiness", "structural", "style", "zoom_out",
)


def frontmatter(path: Path) -> dict:
  return yaml.safe_load(path.read_text().split("---", 2)[1])


@pytest.mark.parametrize("name", REVIEWERS)
def test_reviewers_are_read_only_with_fresh_context(name: str) -> None:
  config = frontmatter(ROOT / "agents" / f"{name}.md")
  assert {t.strip() for t in config["tools"].split(",")} == {"Read", "Grep", "Glob"}
  assert config["model"] == "inherit"
  assert config["omitClaudeMd"] is True
  assert "memory" not in config


def test_skills_reference_claude_guide() -> None:
  assert (ROOT / "docs/claude.md").is_file()
  skills = list((ROOT / "skills").glob("*/SKILL.md"))
  assert skills
  for skill in skills:
    assert "${CLAUDE_PLUGIN_ROOT}/docs/claude.md" in skill.read_text()
