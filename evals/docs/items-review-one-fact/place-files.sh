#!/usr/bin/env bash
# Builds the repo the reviewer works in: main has the spec before the change, and the branch
# booking-limits has the change, which adds FR-4 and FR-5.
set -eu
here=$(dirname "$0")
git init -q -b main
git config user.name "Eval"
git config user.email "eval@example.com"
# A CLAUDE.md that says to load the doc standards.
source "$here/../add-claude-md.sh"
cp -R "$here/files/base/." .
git add -A
git commit -q -m "Add the functional spec"
git checkout -q -b booking-limits
cp -R "$here/files/change/." .
git add -A
git commit -q -m "Cap each member's upcoming bookings, and refuse bookings too far ahead"
