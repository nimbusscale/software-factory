#!/usr/bin/env bash
# Builds the repo the reviewer works in: main has the spec and the planning notes, and the branch
# booking-rules has the change, which writes FR-4, FR-5 and FR-6 from the notes.
set -eu
here=$(dirname "$0")
git init -q -b main
git config user.name "Eval"
git config user.email "eval@example.com"
cp -R "$here/files/base/." .
git add -A
git commit -q -m "Add the functional spec and the planning notes"
git checkout -q -b booking-rules
cp -R "$here/files/change/." .
git add -A
git commit -q -m "Add the booking limit, check-ins and confirmation emails from notes/booking-rules.md"
