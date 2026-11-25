#!/usr/bin/env bash
# Runs every check on the Python code in src/, in order, and stops at the first failure.
# Run it from the repo root: bash tools/check-code.sh
#
# It leaves out the scripts in plugin/, since the code standards don't apply to them (CS-7).
#
# Claude Code asks the owner before each edit to this file, so an agent can't weaken a check to
# make it pass.
set -euo pipefail

cd "$(dirname "$0")/.."

# --locked fails when uv.lock doesn't match pyproject.toml, so the tools are the pinned versions.
run() { uv run --locked "$@"; }

run ruff format --check src

# --ignore-noqa makes every noqa comment do nothing, so no comment can turn off a lint rule.
run ruff check --ignore-noqa src

# mypy can't be told to ignore its type: ignore and mypy: comments, nor the formatter its fmt:
# comments, so this refuses them. It refuses noqa comments too, since they do nothing here and a
# reader would think they do.
if grep -rnE --include='*.py' '#[[:space:]]*(noqa|type:[[:space:]]*ignore|mypy:|fmt:[[:space:]]*(off|skip))' src; then
  echo "A comment above turns off a check. Fix the code instead." >&2
  exit 1
fi

# Ruff has no limit on a file's lines. Blank lines and comment lines don't count.
MAX_FILE_LINES=300
too_long=0
while IFS= read -r -d '' file; do
  lines=$(grep -cvE '^[[:space:]]*(#.*)?$' "$file" || true)
  if ((lines > MAX_FILE_LINES)); then
    echo "$file: $lines lines of code, more than $MAX_FILE_LINES. Split it (CS-2)." >&2
    too_long=1
  fi
done < <(find src -name '*.py' -print0)
((too_long == 0))

run mypy

# pytest exits with 5 when it finds no tests, which isn't a failed test.
status=0
run pytest src || status=$?
if ((status != 0 && status != 5)); then
  exit "$status"
fi
