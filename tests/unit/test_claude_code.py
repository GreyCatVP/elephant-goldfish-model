# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests for the Claude Code plugin in .claude-plugin/."""

import json
import pathlib
import re
from typing import Any, Dict, List

import yaml

# Personas that spawn other agents and so are not limited to read-only tools.
ORCHESTRATORS = ("egm-bootstrap-orchestrator", "egm-synthesizer")
READ_ONLY_TOOLS = {"Read", "Grep", "Glob"}
# Keys only Claude Code understands. Antigravity and Gemini CLI read `tools`
# as their own tool names, so these must stay out of agents/.
CLAUDE_ONLY_KEYS = ("tools", "omitClaudeMd")


def frontmatter_of(path: pathlib.Path) -> Dict[str, Any]:
  """Parses the YAML frontmatter at the top of an agent file."""
  parts = path.read_text(encoding="utf-8").split("---", 2)
  assert len(parts) == 3, f"No frontmatter in {path}"
  return yaml.safe_load(parts[1])


def load_json(path: pathlib.Path) -> Dict[str, Any]:
  """Reads a JSON manifest."""
  return json.loads(path.read_text(encoding="utf-8"))


def test_every_persona_has_a_matching_wrapper(
    repo_root: pathlib.Path,
) -> None:
  """Verifies each persona in agents/ has a Claude wrapper that points to it."""
  personas = sorted((repo_root / "agents").glob("*.md"))
  wrapper_dir = repo_root / ".claude-plugin" / "agents"
  assert personas, "No personas found in agents/"
  assert {p.name for p in personas} == {
      w.name for w in wrapper_dir.glob("*.md")
  }, "agents/ and .claude-plugin/agents/ list different files"
  for persona in personas:
    wrapper = wrapper_dir / persona.name
    canonical, claude = frontmatter_of(persona), frontmatter_of(wrapper)
    assert claude["name"] == canonical["name"], f"name differs in {wrapper}"
    assert claude["description"] == canonical["description"], (
        f"description differs in {wrapper}"
    )
    pointer = f"${{CLAUDE_PLUGIN_ROOT}}/agents/{persona.name}"
    assert pointer in wrapper.read_text(encoding="utf-8"), (
        f"{wrapper} does not point to {pointer}"
    )
    for key in CLAUDE_ONLY_KEYS:
      assert key not in canonical, f"Claude-only key '{key}' in {persona}"


def test_reviewers_are_read_only_with_fresh_context(
    repo_root: pathlib.Path,
) -> None:
  """Verifies Claude reviewers cannot write and start without CLAUDE.md."""
  for wrapper in sorted((repo_root / ".claude-plugin" / "agents").glob("*.md")):
    claude = frontmatter_of(wrapper)
    if claude["name"] in ORCHESTRATORS:
      continue
    tools = {t.strip() for t in claude.get("tools", "").split(",")}
    assert tools == READ_ONLY_TOOLS, f"{wrapper} allows {sorted(tools)}"
    assert claude.get("omitClaudeMd") is True, (
        f"{wrapper} must set omitClaudeMd: true"
    )


def test_dispatched_personas_exist(
    repo_root: pathlib.Path,
    discovered_skills: List[pathlib.Path],
) -> None:
  """Verifies every egm-* name in skills/ is a skill or a Claude agent."""
  skill_names = {
      frontmatter_of(path / "SKILL.md")["name"] for path in discovered_skills
  }
  agent_names = {
      frontmatter_of(path)["name"]
      for path in (repo_root / ".claude-plugin" / "agents").glob("*.md")
  }
  for path in discovered_skills:
    text = (path / "SKILL.md").read_text(encoding="utf-8")
    for name in set(re.findall(r"\begm-[a-z]+(?:-[a-z]+)*", text)):
      assert name in skill_names | agent_names, (
          f"{path.name} dispatches unknown agent '{name}'"
      )


def test_manifests_agree(repo_root: pathlib.Path) -> None:
  """Verifies the Claude manifests match the other harness manifests."""
  plugin = load_json(repo_root / ".claude-plugin" / "plugin.json")
  marketplace = load_json(repo_root / ".claude-plugin" / "marketplace.json")
  gemini = load_json(repo_root / "gemini-extension.json")
  antigravity = load_json(repo_root / "plugin.json")
  assert len(marketplace["plugins"]) == 1, "Expected one marketplace entry"
  entry = marketplace["plugins"][0]
  assert entry["name"] == plugin["name"] == antigravity["name"]
  assert entry["source"] == "./"
  assert plugin["version"] == gemini["version"]
  assert entry["description"] == plugin["description"] == (
      gemini["description"]
  )
  listed = {pathlib.PurePosixPath(p).name for p in plugin["agents"]}
  wrappers = {
      p.name for p in (repo_root / ".claude-plugin" / "agents").glob("*.md")
  }
  assert listed == wrappers, "plugin.json agents differ from the wrapper files"
