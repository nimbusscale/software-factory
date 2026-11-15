#!/usr/bin/env bash
# Builds the repo the reviewer works in: main has the spec before the change, and the branch
# show-cost has the change, which adds FR-10.
set -eu
here=$(dirname "$0")
git init -q -b main
git config user.name "Eval"
git config user.email "eval@example.com"
cp -R "$here/files/base/." .
git add -A
git commit -q -m "Add the functional spec"
git checkout -q -b show-cost
cp -R "$here/files/change/." .
git add -A
git commit -q -m "Show members that bookings cost nothing"
