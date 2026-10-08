# Copyright 2026 Google LLC.
# SPDX-License-Identifier: Apache-2.0

"""CLI regression coverage for empty evaluation selections."""

import subprocess
import sys
from pathlib import Path


def test_empty_selection_fails(repo_root: Path, tmp_path: Path) -> None:
  result = subprocess.run(
      [
          sys.executable, str(repo_root / "tools/eval_runner.py"),
          "--skill", "nonexistent-skill",
          "--output-dir", str(tmp_path / "reports"),
      ],
      capture_output=True,
      text=True,
      check=False,
  )
  assert result.returncode == 1
  assert "No scenario" in result.stdout + result.stderr
  assert not list(tmp_path.rglob("*_results.json"))
