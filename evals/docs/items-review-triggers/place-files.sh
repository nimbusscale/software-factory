#!/usr/bin/env bash
# Builds the repo the reviewer works in: main has the spec before the change, and the branch
# add-requirements has the change, which adds FR-13 and FR-14.
set -eu
here=$(dirname "$0")
git init -q -b main
git config user.name "Eval"
git config user.email "eval@example.com"
# The doc standards, the doc check script and a CLAUDE.md that points to them.
source "$here/../add-doc-standards.sh"
cp -R "$here/files/base/." .
git add -A
git commit -q -m "Add the functional spec"
git checkout -q -b add-requirements
cp -R "$here/files/change/." .
git add -A
git commit -q -m "Offer another room when a member can't book one, and email confirmations"
