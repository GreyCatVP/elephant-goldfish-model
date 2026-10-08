# Copyright 2026 Google LLC.
# SPDX-License-Identifier: Apache-2.0

"""Exercise evaluation retries through LiteLLM without provider requests."""

import importlib
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "tools"))
from eval_runner import run_scenario


@pytest.mark.parametrize("failure_phase", ["model", "judge"])
@pytest.mark.parametrize("exhaust_retries", [False, True])
def test_evaluation_retries(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
    failure_phase: str,
    exhaust_retries: bool,
) -> None:
  """Recover from an outage, or propagate it after the retry budget ends."""
  monkeypatch.setenv("LITELLM_LOCAL_MODEL_COST_MAP", "True")
  import litellm

  main = importlib.import_module("litellm.main")
  completion = litellm.completion
  attempts = {"model": 0, "judge": 0}

  def provider_response(model, *args, **kwargs):
    phase = "judge" if model == "gpt-4o" else "model"
    attempts[phase] += 1
    if phase == failure_phase and (
        exhaust_retries or attempts[phase] == 1
    ):
      raise litellm.ServiceUnavailableError(
          message="Temporary provider outage",
          llm_provider="openai",
          model=model,
      )
    content = '{"passed": true}' if phase == "judge" else "Design Intent"
    return litellm.ModelResponse(
        choices=[{"message": {"role": "assistant", "content": content}}]
    )

  def offline_completion(*args, **kwargs):
    return completion(*args, mock_response="offline", **kwargs)

  monkeypatch.setattr(main, "mock_completion", provider_response)
  monkeypatch.setattr(litellm, "completion", offline_completion)
  scenario = {
      "scenario_id": "retry-outage",
      "eval_type": "llm_judge",
      "turns": [{"user_input": "Draft a design", "rubric": {}}],
  }
  if exhaust_retries:
    with pytest.raises(litellm.ServiceUnavailableError):
      run_scenario(tmp_path, scenario, "gpt-4o-mini", "gpt-4o")
    assert attempts[failure_phase] == 4
    if failure_phase == "model":
      assert attempts["judge"] == 0
  else:
    result = run_scenario(tmp_path, scenario, "gpt-4o-mini", "gpt-4o")
    assert result.passed
    assert result.turn_results[0].model_response == "Design Intent"
    assert attempts[failure_phase] == 2
    assert attempts["judge" if failure_phase == "model" else "model"] == 1
