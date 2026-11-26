#!/usr/bin/env bash
# Builds the repo the writer works in: main holds only the planning notes.
set -eu
here=$(dirname "$0")
git init -q -b main
git config user.name "Eval"
git config user.email "eval@example.com"
# A CLAUDE.md that says to load the doc standards.
source "$here/../add-claude-md.sh"
cp -R "$here/files/." .
git add -A
git commit -q -m "Add the planning notes"
