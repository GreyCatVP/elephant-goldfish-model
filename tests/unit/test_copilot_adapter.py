# Copyright 2026 Google LLC.
# SPDX-License-Identifier: Apache-2.0

"""Offline Copilot package contracts; no model or isolation claims."""

import os
from pathlib import Path
import re
import shutil
import subprocess

import pytest

from .test_harnesses import REVIEWERS, frontmatter


def test_copilot_profiles_use_canonical_read_only_reviewers(repo_root: Path) -> None:
    profiles = repo_root / "com.github.copilot/agents"
    expected_names = {
        frontmatter(repo_root / f"agents/{p}.md")["name"] for p in REVIEWERS
    }
    assert {p.stem.removesuffix(".agent") for p in profiles.glob("*.agent.md")} == (
        expected_names | {"egm"}
    )
    for persona in REVIEWERS:
        canonical = repo_root / f"agents/{persona}.md"
        name = frontmatter(canonical)["name"]
        profile = profiles / f"{name}.agent.md"
        config = frontmatter(profile)
        assert config["name"] == name
        assert config["tools"] == ["read", "search"]
        assert config["include-custom-instructions"] is False
        assert config["user-invocable"] is False
        assert set(config) == {
            "name", "description", "tools", "include-custom-instructions",
            "user-invocable",
        }
        text = profile.read_text(encoding="utf-8")
        assert f"<EGM_ROOT>/agents/{persona}.md" in text
        assert "incomplete review" in text
        assert "Do not retrieve parent history" in text
        assert "${" not in text  # No undocumented Markdown variable expansion.
    entry = profiles / "egm.agent.md"
    assert frontmatter(entry)["tools"] == ["read", "search", "edit", "agent"]
    assert "<EGM_ROOT>/docs/copilot.md" in entry.read_text(encoding="utf-8")


@pytest.fixture
def copilot_package(repo_root: Path, tmp_path: Path) -> Path:
    """Relocate the full runtime, including paths with spaces and Unicode."""
    package = tmp_path / "relocated EGM café"
    package.mkdir()
    for directory in ("skills", "agents", "resources", "docs", "com.github.copilot"):
        shutil.copytree(repo_root / directory, package / directory)
    shutil.copy2(repo_root / "plugin.json", package / "plugin.json")
    return package


def test_copilot_relocated_resources(repo_root: Path, copilot_package: Path) -> None:
    for directory in ("skills", "agents", "resources", "docs"):
        for source in (repo_root / directory).rglob("*"):
            if source.is_file():
                installed = copilot_package / source.relative_to(repo_root)
                assert installed.read_bytes() == source.read_bytes()
    for skill in (copilot_package / "skills").glob("*/SKILL.md"):
        assert skill.parents[2] == copilot_package
    profiles = copilot_package / "com.github.copilot/agents"
    for profile in profiles.glob("*.agent.md"):
        text = profile.read_text(encoding="utf-8")
        for relative in re.findall(r"<EGM_ROOT>/([\w/.-]+)", text):
            assert (copilot_package / relative).exists(), (profile.name, relative)
    assert not (copilot_package / "com.github.copilot/skills").exists()


def test_copilot_native_offline_registration(
    copilot_package: Path, tmp_path: Path,
) -> None:
    """Opt-in local CLI inspection only; never start an agent or prompt."""
    if os.environ.get("EGM_COPILOT_OFFLINE") != "1":
        pytest.skip("Set EGM_COPILOT_OFFLINE=1 for the CLI registration check")
    executable = shutil.which("copilot")
    if executable is None:
        pytest.skip("Copilot CLI is not installed")
    env = dict(
        os.environ, COPILOT_OFFLINE="true",
        COPILOT_HOME=str(tmp_path / "profile"),
    )
    result = subprocess.run(
        [executable, "--plugin-dir", str(copilot_package), "plugin", "list"],
        cwd=tmp_path, env=env, capture_output=True, text=True, timeout=30, check=True,
    )
    assert "External Plugins (via --plugin-dir):" in result.stdout
    assert re.search(r"(?m)^\s*• egm\s*$", result.stdout), result.stdout
