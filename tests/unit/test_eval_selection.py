# Copyright 2026 Google LLC.
# SPDX-License-Identifier: Apache-2.0

"""CLI regression coverage for empty evaluation selections."""

import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.parametrize(
    "selection",
    [
        ["--scenario", "nonexistent-scenario"],
        ["--skill", "egm_draft", "--scenario", "nonexistent-scenario"],
        ["--skill", "nonexistent-skill"],
    ],
)
def test_empty_selection_fails(
    repo_root: Path, tmp_path: Path, selection: list[str],
) -> None:
  result = subprocess.run(
      [
          sys.executable, str(repo_root / "tools/eval_runner.py"),
          *selection, "--output-dir", str(tmp_path / "reports"),
      ],
      capture_output=True,
      text=True,
      check=False,
  )
  assert result.returncode == 1
  assert "0/0 scenarios passed" not in result.stdout
  assert "No scenario" in result.stdout + result.stderr
  assert not list(tmp_path.rglob("*_results.json"))
