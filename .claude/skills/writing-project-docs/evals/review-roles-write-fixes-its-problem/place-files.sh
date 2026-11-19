#!/usr/bin/env bash
# Builds the repo the agent works in: main has the files before the change, and the branch
# no-show-email has the agent's change, not yet committed.
set -eu
here=$(dirname "$0")
git init -q -b main
git config user.name "Eval"
git config user.email "eval@example.com"
# The doc standards, copied from their source in the factory repo, so the case tests the
# current ones.
standards="$(git -C "$here" rev-parse --show-toplevel)/docs/standards"
[[ -f $standards/project-docs.md ]] || { echo "no doc standards at $standards" >&2; exit 1; }
mkdir -p docs/standards
cp -R "$standards"/. docs/standards/
cp -R "$here/files/base/." .
git add -A
git commit -q -m "Add the functional spec and the booking code"
git checkout -q -b no-show-email
cp -R "$here/files/change/." .
