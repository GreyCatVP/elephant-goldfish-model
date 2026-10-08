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

"""Unit tests for evaluation runner assertion and parsing utilities."""

import json
import pathlib
import sys

import pytest

# Add tools to sys.path
sys.path.insert(
    0, str(pathlib.Path(__file__).resolve().parent.parent.parent / "tools")
)
from eval_runner import Assertion
from eval_runner import evaluate_assertions
from eval_runner import parse_judge_response


def test_deterministic_assertion_required_pattern() -> None:
  """Tests required_pattern regex assertion evaluation."""
  assertions = [
      Assertion(
          type="required_pattern", pattern=r"\?", message="Must ask question"
      )
  ]
  response = "What is the primary scaling requirement?"
  passed, errors = evaluate_assertions(response, assertions)
  assert passed
  assert not errors


def test_deterministic_assertion_forbidden_pattern() -> None:
  """Tests forbidden_pattern regex assertion evaluation."""
  assertions = [
      Assertion(
          type="forbidden_pattern",
          pattern=r"```[a-zA-Z]*\n",
          message="No code blocks",
      )
  ]
  response_with_code = "Here is the code:\n```python\nprint('hello')\n```"
  passed, errors = evaluate_assertions(response_with_code, assertions)
  assert not passed
  assert len(errors) == 1
  assert "No code blocks" in errors[0]


def test_deterministic_assertion_contains_and_not_contains() -> None:
  """Tests substring presence and absence assertions."""
  assertions = [
      Assertion(
          type="contains",
          pattern="Design Intent",
          message="Must mention Design Intent",
      ),
      Assertion(
          type="not_contains",
          pattern="DeprecatedAPI",
          message="Must not use DeprecatedAPI",
      ),
  ]
  response = (
      "This document establishes the Design Intent for the new service."
  )
  passed, errors = evaluate_assertions(response, assertions)
  assert passed
  assert not errors


def test_deterministic_assertion_negative_cases() -> None:
  """Tests failure reporting across all assertion types."""
  assertions = [
      Assertion(
          type="required_pattern",
          pattern=r"\?",
          message="Missing question mark",
      ),
      Assertion(
          type="contains", pattern="MandatorySection", message="Missing section"
      ),
      Assertion(
          type="not_contains",
          pattern="ForbiddenWord",
          message="Found forbidden word",
      ),
      Assertion(type="unknown_type", pattern="foo", message="Invalid"),
  ]
  response = "Statement without question mark. ForbiddenWord is here."
  passed, errors = evaluate_assertions(response, assertions)
  assert not passed
  assert len(errors) == 4
  assert "Missing question mark" in errors[0]
  assert "Missing section" in errors[1]
  assert "Found forbidden word" in errors[2]
  assert "Unknown assertion type" in errors[3]


def test_parse_judge_response_clean_json() -> None:
  """Tests parsing clean JSON judge responses."""
  passed_text = '{"passed": true, "reason": "All requirements met."}'
  passed, errors = parse_judge_response(passed_text)
  assert passed
  assert not errors

  failed_text = '{"passed": false, "reason": "Failed invariant."}'
  passed, errors = parse_judge_response(failed_text)
  assert not passed
  assert len(errors) == 1
  assert "Failed invariant." in errors[0]


@pytest.mark.parametrize("value", ["false", "true", "", 0, 1, None, [], [1]])
@pytest.mark.parametrize("fenced", [False, True])
def test_parse_judge_response_rejects_non_boolean_verdicts(
    value: object, fenced: bool,
) -> None:
  """Malformed verdicts must not be coerced to passing evaluations."""
  response = json.dumps({"passed": value, "reason": "Judge explanation."})
  if fenced:
    response = f"```json\n{response}\n```"
  passed, errors = parse_judge_response(response)
  assert passed is False
  assert errors == ["Judge 'passed' field must be a JSON boolean."]


@pytest.mark.parametrize("fenced", [False, True])
def test_parse_judge_response_requires_verdict(fenced: bool) -> None:
  """A missing verdict is a schema error, not a valid negative verdict."""
  response = '{"reason": "No verdict supplied."}'
  if fenced:
    response = f"```json\n{response}\n```"
  passed, errors = parse_judge_response(response)
  assert passed is False
  assert errors == ["Judge 'passed' field must be a JSON boolean."]


def test_parse_judge_response_markdown_code_blocks() -> None:
  """Tests parsing markdown code-block wrapped JSON judge verdicts."""
  md_text = (
      "Evaluation complete:\n```json\n"
      '{"passed": true, "reason": "Tone is objective."}\n'
      "```\nExtra commentary."
  )
  passed, errors = parse_judge_response(md_text)
  assert passed
  assert not errors


def test_parse_judge_response_fallbacks_and_malformed() -> None:
  """Tests fallbacks for empty reason, malformed text, and empty inputs."""
  # Empty reason string fallback
  empty_reason = '{"passed": false, "reason": ""}'
  passed, errors = parse_judge_response(empty_reason)
  assert not passed
  assert errors == ["Judge evaluation failed."]

  # Empty string or None
  passed, errors = parse_judge_response("")
  assert not passed
  assert "Empty judge response" in errors[0]

  passed, errors = parse_judge_response(None)
  assert not passed
  assert "Empty judge response" in errors[0]

  # Non-JSON response
  passed, errors = parse_judge_response("I think it passed!")
  assert not passed
  assert "Judge did not return JSON format" in errors[0]

  # Unclosed JSON braces
  passed, errors = parse_judge_response('{"passed": true, "reason": ')
  assert not passed
  assert "Judge did not return JSON format" in errors[0]

  # Malformed JSON syntax inside braces
  malformed_syntax = '{"passed": true, "reason": unquoted_val}'
  passed, errors = parse_judge_response(malformed_syntax)
  assert not passed
  assert "Failed to parse judge JSON" in errors[0]
