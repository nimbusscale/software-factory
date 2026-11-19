#!/usr/bin/env bash
# Builds the repo the reviewer works in: main has the spec before the change, and the branch
# room-use has the change, which adds FR-6 and FR-7.
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
git commit -q -m "Add the functional spec"
git checkout -q -b room-use
cp -R "$here/files/change/." .
git add -A
git commit -q -m "Show each room's booked hours, and keep cancelled bookings for 30 days"
