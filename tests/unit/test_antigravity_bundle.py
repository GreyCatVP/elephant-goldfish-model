# Copyright 2026 Google LLC.
# SPDX-License-Identifier: Apache-2.0

"""Antigravity packaging must restrict reviewers and keep other files intact."""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "build_antigravity", ROOT / "tools/build_antigravity.py",
)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


def split(path: Path) -> tuple[str, str]:
    header, body = path.read_text(encoding="utf-8").split("\n---\n", 1)
    return header, body


def test_bundle_restricts_reviewers(tmp_path: Path) -> None:
    output = tmp_path / "bundle"
    BUILDER.build(ROOT, output)
    for name in BUILDER.REVIEWERS:
        header, body = split(output / "agents" / f"{name}.md")
        assert "tools:\n- view_file\n- grep_search\n" in header
        assert "commandExecutionPolicy: 'off'" in header
        assert "mainAgent: false" in header
        assert "subagent: true" in header
        assert split(ROOT / "agents" / f"{name}.md")[1] in body
    for name in ("bootstrap_orchestrator", "synthesizer"):
        assert (output / "agents" / f"{name}.md").read_bytes() == (
            ROOT / "agents" / f"{name}.md"
        ).read_bytes()
    for path in (output / "skills").glob("*/SKILL.md"):
        assert "disable-model-invocation" not in split(path)[0]
    assert (output / "resources/document_standards/feature-spec-standard.md").is_file()
    assert (output / "skills/egm_draft/references/design_doc.md").is_file()


def test_rejects_existing_output(tmp_path: Path) -> None:
    with pytest.raises(FileExistsError):
        BUILDER.build(ROOT, tmp_path)
