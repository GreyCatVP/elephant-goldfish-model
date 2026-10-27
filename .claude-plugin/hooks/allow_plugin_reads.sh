#!/bin/sh
# Copyright 2026 Google LLC.
# SPDX-License-Identifier: Apache-2.0

# Approves Read, Grep and Glob only inside the plugin folders that EGM reads at
# run time. Personas and standards live outside the user's workspace, and
# headless runs and background subagents cannot ask for permission, so without
# this a Goldfish cannot read its persona. The rest of the plugin root is left
# out because a local install copies the whole clone, private files included.
# Anything not clearly inside those folders, including any input that contains
# "..", falls through to the normal permission rules.
input=$(cat)
case "$input" in *..*) exit 0 ;; esac

# Backslash is a path separator only on Windows; on POSIX it is a legal
# filename character.
case "$CLAUDE_PLUGIN_ROOT" in
  [A-Za-z]:[\\/]*) windows=1 ;;
  *) windows= ;;
esac

if [ -n "$windows" ]; then
  root=$(printf '%s' "$CLAUDE_PLUGIN_ROOT" | tr '\\' '/')
  root=${root%/}
else
  root=${CLAUDE_PLUGIN_ROOT%/}
fi
[ -n "$root" ] || exit 0

# An absolute or home-relative Glob pattern could name files outside `path`.
if printf '%s' "$input" | grep -Eq '"tool_name"[[:space:]]*:[[:space:]]*"Glob"' &&
  printf '%s' "$input" | grep -Eq '"pattern"[[:space:]]*:[[:space:]]*"(/|~|\\|[A-Za-z]:)'; then
  exit 0
fi

if [ -n "$windows" ]; then
  path=$(printf '%s' "$input" | sed -nE 's/.*"(file_path|path)"[[:space:]]*:[[:space:]]*"(([^"\\]|\\\\)*)".*/\2/p' | head -n 1 | sed 's/\\\\/\//g')
  root=$(printf '%s' "$root" | tr '[:upper:]' '[:lower:]')
  path=$(printf '%s' "$path" | tr '[:upper:]' '[:lower:]')
else
  path=$(printf '%s' "$input" | sed -nE 's/.*"(file_path|path)"[[:space:]]*:[[:space:]]*"([^"\\]*)".*/\2/p' | head -n 1)
fi

case "$path" in
  "$root"/agents | "$root"/agents/* | "$root"/docs | "$root"/docs/* | \
  "$root"/resources | "$root"/resources/* | "$root"/skills | "$root"/skills/*)
    printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow","permissionDecisionReason":"EGM plugin file"}}'
    ;;
esac
exit 0
