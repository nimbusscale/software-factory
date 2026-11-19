#!/usr/bin/env bash
# Builds the repo the reviewer works in, from a real run of the skill on Facet's design doc. main
# has the design doc, and the branch functional-spec adds the spec a writer wrote from it, with
# that writer's commit message. The spec states some points as settled that the design doc leaves
# open, and the commit message lists them as open questions.
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
git commit -q -m "Add Facet's design doc"
git checkout -q -b functional-spec
cp -R "$here/files/change/." .
git add -A
git commit -q -F "$here/commit-message.txt"
