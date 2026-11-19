#!/usr/bin/env bash
# Builds the repo the reviewer works in: main has the files before the change, and the branch
# thirty-days has the change, in one commit.
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
git checkout -q -b thirty-days
cp -R "$here/files/change/." .
git add -A
git commit -q -m "Let members book up to 30 days ahead"
