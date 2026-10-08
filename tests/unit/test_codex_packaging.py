# Copyright 2026 Google LLC.
# SPDX-License-Identifier: Apache-2.0

"""Offline checks for the installable Codex plugin, including bundled prompts."""

import json
import pathlib
import re

import yaml


EXPECTED_SKILLS = {
    "egm-bootstrap", "egm-brainstorm", "egm-draft", "egm-drift-report",
    "egm-resolve", "egm-review", "egm-review-loop",
}


def test_codex_marketplace_resolves_plugin(repo_root: pathlib.Path) -> None:
    marketplace = json.loads(
        (repo_root / ".agents/plugins/marketplace.json").read_text()
    )
    entries = [p for p in marketplace["plugins"] if p["name"] == "egm"]
    assert len(entries) == 1
    entry = entries[0]
    plugin_root = (repo_root / entry["source"]).resolve()
    assert plugin_root.is_relative_to(repo_root.resolve())
    manifest = json.loads(
        (plugin_root / ".codex-plugin/plugin.json").read_text()
    )
    assert manifest["name"] == entry["name"]
    assert re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"])
    assert entry["policy"]["installation"] == "AVAILABLE"
    skills_root = (plugin_root / manifest["skills"]).resolve()
    assert skills_root.is_relative_to(plugin_root)
    names = []
    for skill in skills_root.glob("*/SKILL.md"):
        names.append(yaml.safe_load(skill.read_text().split("---", 2)[1])["name"])
    assert len(names) == len(set(names)), "Duplicate discoverable skill names"
    assert set(names) == EXPECTED_SKILLS


def test_codex_bundled_prompt_dependencies(repo_root: pathlib.Path) -> None:
    # Markdown-link tests deliberately ignore inline code. Prompt paths mostly
    # live in inline code, so check these separately, including persona callers.
    prompts = list((repo_root / "skills").glob("*/SKILL.md"))
    prompts += list((repo_root / "agents").glob("*.md"))
    references = set()
    for prompt in prompts:
        for target in re.findall(
            r"`((?:agents|resources|references)/[^`\s]+\.md)`",
            prompt.read_text(),
        ):
            if any(char in target for char in "{}[]<>"):
                continue  # Parameterized paths are resolved below for personas.
            root = prompt.parent if target.startswith("references/") else repo_root
            path = (root / target).resolve()
            assert path.is_relative_to(repo_root.resolve())
            assert path.is_file(), f"{prompt}: missing bundled dependency {target}"
            references.add(target)
    assert "agents/synthesizer.md" in references
    assert "resources/document_standards/zoom-out-standard.md" in references
    assert "references/design_doc.md" in references

    personas = [
        yaml.safe_load(p.read_text().split("---", 2)[1])["name"]
        for p in (repo_root / "agents").glob("*.md")
    ]
    assert len(personas) == len(set(personas)), "Ambiguous persona name"
    required = {
        "egm-design", "egm-codebase-details", "egm-zoom-out",
        "egm-comprehension", "egm-implementation-readiness", "egm-structural",
        "egm-synthesizer", "egm-style",
    }
    assert required <= set(personas)
    for filename in (
        "design_critic", "codebase_details", "zoom_out", "comprehension",
        "implementation_readiness", "structural", "style", "synthesizer",
    ):
        assert (repo_root / "agents" / f"{filename}.md").is_file()
    for standard in (
        "zoom-out", "re-implementation", "feature-spec",
        "implementation-readiness", "heilmeier",
    ):
        assert (repo_root / "resources/document_standards"
                / f"{standard}-standard.md").is_file()


def test_codex_integration_reference_reachable(repo_root: pathlib.Path) -> None:
    for skill in (repo_root / "skills").glob("*/SKILL.md"):
        targets = re.findall(r"\[Codex integration\]\(([^)]+)\)", skill.read_text())
        assert len(targets) == 1, f"{skill}: no unique Codex entry point"
        assert (skill.parent / targets[0]).resolve() == repo_root / "docs/codex.md"
    assert (repo_root / "docs/codex.md").is_file()
