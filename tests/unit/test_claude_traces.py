# Copyright 2026 Google LLC.
# SPDX-License-Identifier: Apache-2.0

"""Offline regression coverage for Claude's native transcript directory."""

from pathlib import Path
import json
import runpy

import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("config_mode", ["unset", "default", "custom"])
def test_trace_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, config_mode: str
) -> None:
  trace_directory = runpy.run_path(str(ROOT / "tests/integration/test_claude.py"))[
      "trace_directory"
  ]
  monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path / "home"))
  config = tmp_path / "home" / ".claude"
  if config_mode == "unset":
    monkeypatch.delenv("CLAUDE_CONFIG_DIR", raising=False)
  else:
    if config_mode == "custom":
      config = tmp_path / "custom config"
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(config))

  assert trace_directory(Path("/work/egm probe.v1")) == (
      config / "projects" / "-work-egm-probe-v1"
  )


@pytest.mark.parametrize("result", ["success", "error", "missing", "unrelated", "empty"])
def test_child_probe_requires_successful_read(result: str) -> None:
  check = runpy.run_path(str(ROOT / "tests/integration/test_claude.py"))[
      "assert_child_probe"
  ]
  persona = Path("/plugin/agents/zoom_out.md")
  events = [{"type": "assistant", "message": {"content": [{
      "type": "tool_use", "id": "read-persona", "name": "Read",
      "input": {"file_path": str(persona)},
  }]}}]
  if result != "missing":
    events.append({"type": "user", "message": {"content": [{
        "type": "tool_result",
        "tool_use_id": "other-read" if result == "unrelated" else "read-persona",
        "is_error": result == "error",
        "content": "" if result == "empty" else "Persona text",
    }]}})
  events.append({"type": "assistant", "message": {"content": [{
      "type": "text", "text": "UNKNOWN",
  }]}})
  raw = "\n".join(json.dumps(event) for event in events)
  if result == "success":
    check(raw, persona, ["parent-only-marker"])
  else:
    with pytest.raises(AssertionError, match="successful native tool result"):
      check(raw, persona, ["parent-only-marker"])


@pytest.mark.parametrize("separator", ["\u0085", "\u2028", "\u2029"])
def test_child_probe_keeps_unicode_inside_json_records(separator: str) -> None:
  check = runpy.run_path(str(ROOT / "tests/integration/test_claude.py"))[
      "assert_child_probe"
  ]
  persona = Path("/plugin/agents/zoom_out.md")
  events = [
      {"type": "assistant", "message": {"content": [{
          "type": "tool_use", "id": "read", "name": "Read",
          "input": {"file_path": str(persona)},
      }]}},
      {"type": "user", "message": {"content": [{
          "type": "tool_result", "tool_use_id": "read",
          "content": f"Persona{separator}text",
      }]}},
      {"type": "assistant", "message": {"content": [{
          "type": "text", "text": "UNKNOWN",
      }]}},
  ]
  raw = "\n".join(json.dumps(event, ensure_ascii=False) for event in events)
  check(raw, persona, ["parent-only-marker"])
  with pytest.raises(AssertionError):
    check(raw, persona, ["Persona"])
