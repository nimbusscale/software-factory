#!/usr/bin/env bash
# Builds the repo the reviewer works in: main has the spec before the change, and the branch
# room-use has the change, which adds FR-6 and FR-7.
set -eu
here=$(dirname "$0")
git init -q -b main
git config user.name "Eval"
git config user.email "eval@example.com"
cp -R "$here/files/base/." .
git add -A
git commit -q -m "Add the functional spec"
git checkout -q -b room-use
cp -R "$here/files/change/." .
git add -A
git commit -q -m "Show each room's booked hours, and keep cancelled bookings for 30 days"
