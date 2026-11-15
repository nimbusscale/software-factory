#!/usr/bin/env bash
# Builds the repo the reviewer works in: main has the spec before the change, and the branch
# booking-rules has the change, which adds FR-4, FR-5 and FR-6.
set -eu
here=$(dirname "$0")
git init -q -b main
git config user.name "Eval"
git config user.email "eval@example.com"
cp -R "$here/files/base/." .
git add -A
git commit -q -m "Add the functional spec"
git checkout -q -b booking-rules
cp -R "$here/files/change/." .
git add -A
git commit -q -m "Limit bookings to building hours, email invites, and say when a room is taken"
