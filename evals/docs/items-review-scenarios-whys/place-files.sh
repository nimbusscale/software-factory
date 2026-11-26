#!/usr/bin/env bash
# Builds the repo the reviewer works in: main has the spec before the change, and the branch
# booking-rules has the change, which adds FR-4, FR-5 and FR-6 with Whys, and check-ins, as FR-7
# and FR-8 with scenarios.
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
git checkout -q -b booking-rules
cp -R "$here/files/change/." .
git add -A
git commit -q -m "Limit bookings to building hours, email invites, say when a room is taken, and add check-ins that cancel bookings nobody checks in to"
