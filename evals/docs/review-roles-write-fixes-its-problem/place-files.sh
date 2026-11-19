#!/usr/bin/env bash
# Builds the repo the agent works in: main has the files before the change, and the branch
# no-show-email has the agent's change, not yet committed.
set -eu
here=$(dirname "$0")
git init -q -b main
git config user.name "Eval"
git config user.email "eval@example.com"
# The doc standards, the doc check script and a CLAUDE.md that points to them.
source "$here/../add-doc-standards.sh"
cp -R "$here/files/base/." .
git add -A
git commit -q -m "Add the functional spec and the booking code"
git checkout -q -b no-show-email
cp -R "$here/files/change/." .
