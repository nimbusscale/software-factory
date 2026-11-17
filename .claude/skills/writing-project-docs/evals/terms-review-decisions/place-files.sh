#!/usr/bin/env bash
# Builds the repo the reviewer works in: main has both specs before the change, and the branch
# task-terms has the change, which adds three terms and TR-3 to the technical spec.
set -eu
here=$(dirname "$0")
git init -q -b main
git config user.name "Eval"
git config user.email "eval@example.com"
cp -R "$here/files/base/." .
git add -A
git commit -q -m "Add the functional and technical specs"
git checkout -q -b task-terms
cp -R "$here/files/change/." .
git add -A
git commit -q -m "Define the app's parts and failed tasks, and keep a failed task's error"
