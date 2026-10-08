# Copyright 2026 Google LLC.
# SPDX-License-Identifier: Apache-2.0

"""Offline packaging contracts for the shared plugin and host manifests."""

import json
from pathlib import Path

from jsonschema import Draft202012Validator
import pytest

ROOT = Path(__file__).resolve().parents[2]
COMPATIBILITY_MANIFESTS = [
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
    "gemini-extension.json",
]
MARKETPLACES = [
    ".agents/plugins/marketplace.json",
    ".claude-plugin/marketplace.json",
    ".cursor-plugin/marketplace.json",
]


def read_json(path: str) -> dict:
  return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_portable_manifest_schema() -> None:
  schema = read_json("tests/fixtures/plugin-1.0.0.schema.json")
  Draft202012Validator.check_schema(schema)
  Draft202012Validator(schema).validate(read_json("plugin.json"))


@pytest.mark.parametrize("path", COMPATIBILITY_MANIFESTS)
def test_compatibility_metadata_matches_root(path: str) -> None:
  canonical = read_json("plugin.json")
  manifest = read_json(path)
  for field in ("name", "version", "description"):
    assert manifest[field] == canonical[field], f"{path}: {field} drift"
  for field in ("author", "homepage", "repository", "license"):
    if field in manifest:
      assert manifest[field] == canonical[field], f"{path}: {field} drift"
  if "interface" in manifest:
    assert manifest["interface"]["developerName"] == canonical["author"]["name"]
  if "skills" in manifest:
    assert (ROOT / manifest["skills"]).resolve() == ROOT / "skills"


@pytest.mark.parametrize("path", MARKETPLACES)
def test_marketplace_resolves_shared_package(path: str) -> None:
  canonical = read_json("plugin.json")
  marketplace = read_json(path)
  assert marketplace["name"] == "elephant-goldfish-model"
  assert len(marketplace["plugins"]) == 1
  entry = marketplace["plugins"][0]
  assert entry["name"] == canonical["name"]
  assert (ROOT / entry["source"]).resolve() == ROOT
  if "description" in entry:
    assert entry["description"] == canonical["description"]


def test_compatibility_agents_resolve_shared_personas() -> None:
  paths = read_json(".claude-plugin/plugin.json")["agents"]
  resolved = [(ROOT / path).resolve() for path in paths]
  assert len(resolved) == len(set(resolved))
  assert set(resolved) == set((ROOT / "agents").glob("*.md"))
  assert all(path.is_file() for path in resolved)
