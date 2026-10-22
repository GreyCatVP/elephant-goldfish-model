# Copyright 2026 Google LLC.
# SPDX-License-Identifier: Apache-2.0

"""Read evidence must work across retained Codex trace versions."""

from pathlib import Path
import runpy

import pytest

successful_reads = runpy.run_path(str(
    Path(__file__).resolve().parents[1] / "integration/test_codex.py"
))["successful_reads"]


@pytest.mark.parametrize("output_key", ["stdout", "aggregated_output"])
@pytest.mark.parametrize("exit_code", [0, 1])
def test_successful_read_evidence(output_key: str, exit_code: int) -> None:
    item = {
        "type": "CommandExecution", "status": "completed",
        "exit_code": exit_code, output_key: "persona content",
        "cwd": "file:///tmp/egm", "parsed_cmd": [
            {"type": "read", "path": "agents/zoom_out.md"},
        ],
    }
    reads = successful_reads([{"payload": {"item": item}}])
    expected = {Path("/tmp/egm/agents/zoom_out.md").resolve()}
    assert reads == (expected if exit_code == 0 else set())


@pytest.mark.parametrize("command, expected", [
    ("cat /tmp/egm/a.md '/tmp/egm/b c.md'", {"a.md", "b c.md"}),
    ("echo cat /tmp/egm/a.md", set()),
    ("cat /tmp/egm/a.md; echo /tmp/egm/b.md", set()),
    ("cat /tmp/egm/*.md", set()),
])
def test_literal_multi_file_read(command: str, expected: set[str]) -> None:
    item = {
        "type": "CommandExecution", "status": "completed", "exit_code": 0,
        "aggregated_output": "file contents", "cwd": "file:///tmp/egm",
        "parsed_cmd": [{"type": "unknown", "cmd": command}],
    }
    assert successful_reads([{"payload": {"item": item}}]) == {
        Path("/tmp/egm", name).resolve() for name in expected
    }
