# Copyright 2026 Google LLC.
# SPDX-License-Identifier: Apache-2.0

"""Claude reviewer tool/context contracts and bundled integration resources."""

import json
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
def test_reviewers_have_read_only_fresh_context(name: str) -> None:
  path = ROOT / "agents" / f"{name}.md"
  config = frontmatter(path)
  assert {tool.strip() for tool in config["tools"].split(",")} == {
      "Read", "Grep", "Glob",
  }
  assert config["omitClaudeMd"] is True
  assert config["model"] == "inherit"
  assert "memory" not in config
  manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
  assert f"./agents/{name}.md" in manifest["agents"]


def test_orchestrators_keep_delegation_and_writing_capabilities() -> None:
  for name in ("bootstrap_orchestrator", "synthesizer"):
    config = frontmatter(ROOT / "agents" / f"{name}.md")
    assert "tools" not in config
    assert not config.get("omitClaudeMd")


def test_skills_resolve_claude_guide_from_plugin_root() -> None:
  guide = ROOT / "docs/claude.md"
  assert guide.is_file()
  skills = list((ROOT / "skills").glob("*/SKILL.md"))
  assert skills
  for skill in skills:
    assert "${CLAUDE_PLUGIN_ROOT}/docs/claude.md" in skill.read_text()
    assert frontmatter(skill)["disable-model-invocation"] is True
    assert "context" not in frontmatter(skill)
