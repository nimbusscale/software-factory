#!/usr/bin/env bash
# Builds the repo the reviewer works in: main has both specs before the change, and the branch
# missed-tasks has the change, which adds TR-2 and TD-1 to the technical spec.
set -eu
here=$(dirname "$0")
git init -q -b main
git config user.name "Eval"
git config user.email "eval@example.com"
cp -R "$here/files/base/." .
git add -A
git commit -q -m "Add the functional and technical specs"
git checkout -q -b missed-tasks
cp -R "$here/files/change/." .
git add -A
git commit -q -m "Run the tasks that came due while the worker was stopped"
