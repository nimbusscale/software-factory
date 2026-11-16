#!/usr/bin/env bash
# Builds the repo the reviewer works in: main has the spec, and the branch no-projectors has the
# change, which takes projectors out of the spec and also drops FR-4's same-day exception.
set -eu
here=$(dirname "$0")
git init -q -b main
git config user.name "Eval"
git config user.email "eval@example.com"
cp -R "$here/files/base/." .
git add -A
git commit -q -m "Add the functional spec"
git checkout -q -b no-projectors
cp -R "$here/files/change/." .
git add -A
git commit -q -F - <<'MSG'
Take projectors out of the spec

The office no longer lends projectors, so the Projector term, FR-5 and FR-6
go. Also drop FR-4's same-day exception. Hardly anyone books on the day,
and the limit is easier to explain as a flat 3.
MSG
