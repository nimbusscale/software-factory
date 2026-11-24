#!/usr/bin/env bash
# Claude Code runs this after each Edit or Write. It formats and lints the file when it's a
# Python file under src/, so errors come back right away. Exit code 2 sends stderr back to
# Claude Code.
#
# Claude Code asks the owner before each edit to this file, so an agent can't weaken a check to
# make it pass.
set -uo pipefail

file_path=$(jq -r '.tool_input.file_path // empty')
case "$file_path" in
  *.py) ;;
  *) exit 0 ;;
esac

# The file's own checkout, so an edit in a git worktree is checked against that worktree's config.
repo=$(git -C "$(dirname "$file_path")" rev-parse --show-toplevel 2>/dev/null) || exit 0
case "$file_path" in
  "$repo"/src/*) ;;
  *) exit 0 ;;
esac
cd "$repo" || exit 1

if ! output=$(uv run --locked ruff format "$file_path" 2>&1); then
  printf 'ruff format failed on %s:\n%s\n' "$file_path" "$output" >&2
  exit 2
fi

if ! output=$(uv run --locked ruff check --ignore-noqa "$file_path" 2>&1); then
  printf 'ruff check failed on %s:\n%s\n' "$file_path" "$output" >&2
  exit 2
fi
