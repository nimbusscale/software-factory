#!/usr/bin/env bash
# Builds the repo the reviewer works in: main has both specs before the change, and the branch
# backups has the change, which adds AD-3, AD-4 and AD-5 to the technical spec.
set -eu
here=$(dirname "$0")
git init -q -b main
git config user.name "Eval"
git config user.email "eval@example.com"
# A CLAUDE.md that says to load the doc standards.
source "$here/../add-claude-md.sh"
cp -R "$here/files/base/." .
git add -A
git commit -q -m "Add the functional and technical specs"
git checkout -q -b backups
cp -R "$here/files/change/." .
git add -A
git commit -q -m "Say how the databases are backed up"
