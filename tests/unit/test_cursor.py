# Copyright 2026 Google LLC.
# SPDX-License-Identifier: Apache-2.0

"""Offline Cursor package contracts, not native workflow or isolation proof."""

import json
from pathlib import Path
import re
import shutil

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
REVIEWERS = {
    "codebase_details", "comprehension", "design_critic",
    "implementation_readiness", "structural", "style", "zoom_out",
}


def frontmatter(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1])


@pytest.fixture
def installed(tmp_path: Path) -> Path:
    """Reproduce the documented copy, without another host's manifest."""
    package = tmp_path / "Cursor candidate café" / "egm"
    package.mkdir(parents=True)
    for name in (".cursor-plugin", "skills", "agents", "resources", "docs"):
        shutil.copytree(ROOT / name, package / name)
    shutil.copy2(ROOT / "LICENSE", package / "LICENSE")
    return package


def test_manifest_selects_native_adapters(installed: Path) -> None:
    manifest = json.loads(
        (installed / ".cursor-plugin/plugin.json").read_text(encoding="utf-8")
    )
    canonical = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    for field in ("name", "version", "description", "author", "homepage",
                  "repository", "license"):
        assert manifest[field] == canonical[field]
    assert manifest["skills"] == "./skills/"
    assert manifest["agents"] == "./.cursor-plugin/agents/"
    assert manifest["rules"] == "./.cursor-plugin/rules/"
    assert set(manifest) == {
        "name", "version", "description", "author", "homepage", "repository",
        "license", "skills", "agents", "rules",
    }
    assert not (installed / "plugin.json").exists()
    for component in ("skills", "agents", "rules"):
        assert (installed / manifest[component]).is_dir()
    adapters = installed / manifest["agents"]
    assert {p.stem for p in adapters.glob("*.md")} == REVIEWERS


@pytest.mark.parametrize("name", sorted(REVIEWERS))
def test_reviewers_use_canonical_personas(installed: Path, name: str) -> None:
    adapter = installed / ".cursor-plugin/agents" / f"{name}.md"
    config = frontmatter(adapter)
    persona = installed / "agents" / f"{name}.md"
    assert config["name"] == frontmatter(persona)["name"]
    assert config["readonly"] is True
    assert config["is_background"] is False
    assert config["model"] == "inherit"
    assert set(config) == {"name", "description", "model", "readonly", "is_background"}
    text = adapter.read_text(encoding="utf-8")
    paths = re.findall(r"EGM_ROOT/([\w/.-]+\.md)", text)
    assert paths == [f"agents/{name}.md"]
    assert all((installed / path).is_file() for path in paths)
    assert "incomplete review" in text
    assert len(text.splitlines()) < 25  # Routing only, no copied persona rules.
    assert persona.read_bytes() == (ROOT / "agents" / persona.name).read_bytes()


def test_relocated_package_keeps_all_canonical_resources(installed: Path) -> None:
    for folder in ("skills", "agents", "resources", "docs"):
        for source in (ROOT / folder).rglob("*"):
            if source.is_file():
                destination = installed / source.relative_to(ROOT)
                assert not destination.is_symlink()
                assert destination.read_bytes() == source.read_bytes()
    for prompt in [*installed.glob("skills/*/SKILL.md"),
                   *installed.glob("agents/*.md")]:
        if prompt.name == "SKILL.md":
            assert prompt.parents[2] == installed
        text = prompt.read_text(encoding="utf-8")
        for target in re.findall(
            r"`((?:agents|resources|references)/[^`\s]+\.md)`", text
        ):
            if any(char in target for char in "{}[]<>"):
                continue
            base = prompt.parent if target.startswith("references/") else installed
            assert (base / target).is_file(), f"{prompt}: missing {target}"
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if target.startswith("../../"):
                assert (prompt.parent / target.split("#")[0]).is_file()


def test_host_rule_and_guide_keep_failure_and_artifact_contracts() -> None:
    rule = ROOT / ".cursor-plugin/rules/egm.mdc"
    assert frontmatter(rule)["alwaysApply"] is True
    text = " ".join(rule.read_text(encoding="utf-8").split())
    for contract in (
        "EGM_ROOT/docs/cursor.md", "absolute file paths", "Never resume",
        "human approval gates", "stop the stage", "Do not simulate",
    ):
        assert contract in text
    guide = " ".join((ROOT / "docs/cursor.md").read_text(encoding="utf-8").split())
    assert "EGM artifact directory: <path>" in guide
    assert "Grok Bot remains a separate, unverified surface" in guide
    assert "No Cursor trace parser is supplied" in guide
