# Copyright 2026 Google LLC.
# SPDX-License-Identifier: Apache-2.0

"""Offline packaging contracts for the shared plugin and host manifests."""

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_URL = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
NAME_RE = r"(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?"
COMPATIBILITY_MANIFESTS = [
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
]
MARKETPLACES = [
    ".agents/plugins/marketplace.json",
    ".claude-plugin/marketplace.json",
]


def read_json(path: str) -> dict:
  return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_portable_manifest_schema() -> None:
  manifest = read_json("plugin.json")
  assert manifest["$schema"] == SCHEMA_URL
  assert re.fullmatch(NAME_RE, manifest["name"])


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
  if path == ".agents/plugins/marketplace.json":
    assert entry["policy"]["authentication"] == "ON_INSTALL"
    assert entry["category"] == "Productivity"


def test_compatibility_agents_resolve_shared_personas() -> None:
  paths = read_json(".claude-plugin/plugin.json")["agents"]
  assert all((ROOT / path).is_file() for path in paths)
