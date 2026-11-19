#!/usr/bin/env bash
# Builds the repo the reviewer works in: main has both specs before the change, and the branch
# tasks has the change, which adds three terms, TR-2, TR-3 and TD-2 to the technical spec.
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
git commit -q -m "Add the functional and technical specs"
git checkout -q -b tasks
cp -R "$here/files/change/." .
git add -A
git commit -q -m "Define the app's parts and failed tasks, run the tasks that came due while the worker was stopped, and keep a failed task's error"
