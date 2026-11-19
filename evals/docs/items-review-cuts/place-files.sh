#!/usr/bin/env bash
# Builds the repo the reviewer works in: main has the spec, and the branch no-projectors has the
# change, which takes projectors out of the spec and also drops FR-4's same-day exception. The
# commit message ties that cut to the projectors, but the task doesn't call for it.
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
git checkout -q -b no-projectors
cp -R "$here/files/change/." .
git add -A
git commit -q -F - <<'MSG'
Take projectors out of the spec

The office no longer lends projectors, so the Projector term, FR-5 and FR-6
go. FR-4's same-day exception goes with them. It was only there so members
could book a room with a projector at short notice, when the office set one
up that day. Without projectors it has no purpose, so FR-4 becomes a flat 3.
MSG
