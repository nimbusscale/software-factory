#!/usr/bin/env bash
# Builds the repo the reviewer works in: main has the spec and the waitlist notes, and the branch
# waitlists adds waitlists to the spec. FR-7 closes waitlists 30 minutes before the slot, where the
# notes say only "shortly before". The commit message gives no hint of it.
set -eu
here=$(dirname "$0")
git init -q -b main
git config user.name "Eval"
git config user.email "eval@example.com"
# A CLAUDE.md that says to load the doc standards.
source "$here/../add-claude-md.sh"
cp -R "$here/files/base/." .
git add -A
git commit -q -m "Add the functional spec and the waitlist notes"
git checkout -q -b waitlists
cp -R "$here/files/change/." .
git add -A
git commit -q -m "Add waitlists to the spec, from the planning notes"
