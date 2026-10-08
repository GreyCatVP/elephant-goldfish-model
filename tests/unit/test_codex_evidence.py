# Copyright 2026 Google LLC.
# SPDX-License-Identifier: Apache-2.0

"""Regression checks that missing native evidence cannot produce a pass."""

import json
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "integration"))
from test_codex import assert_isolated_spawns, child_traces, successful_reads


def test_parent_claim_is_not_a_native_review() -> None:
    trace = [{"type": "response_item", "payload": {
        "type": "message", "role": "assistant",
        "content": [{"text": "All 15 reviewers completed successfully."}],
    }}]
    with pytest.raises(AssertionError, match="No native"):
        child_traces(trace)
    with pytest.raises(AssertionError, match="No native"):
        assert_isolated_spawns(trace)


@pytest.mark.parametrize("arguments", [{}, {"fork_context": True}, {"fork_turns": "all"}])
def test_inherited_or_unspecified_context_fails(arguments: dict) -> None:
    trace = [{"type": "response_item", "payload": {
        "type": "function_call", "name": "spawn_agent",
        "arguments": json.dumps(arguments),
    }}]
    with pytest.raises(AssertionError, match="inherited"):
        assert_isolated_spawns(trace)


def test_failed_read_is_not_resource_evidence(tmp_path: pathlib.Path) -> None:
    target = tmp_path / "SKILL.md"
    trace = [{"type": "event_msg", "payload": {"item": {
        "type": "CommandExecution", "status": "completed", "exit_code": 1,
        "cwd": tmp_path.as_uri(), "stdout": "partial output",
        "parsed_cmd": [{"type": "read", "path": str(target)}],
    }}}]
    assert target not in successful_reads(trace)
