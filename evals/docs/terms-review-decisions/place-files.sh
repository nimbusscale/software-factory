#!/usr/bin/env bash
# Builds the repo the reviewer works in: main has both specs before the change, and the branch
# tasks has the change, which adds three terms, TR-2, TR-3 and TD-2 to the technical spec.
set -eu
here=$(dirname "$0")
git init -q -b main
git config user.name "Eval"
git config user.email "eval@example.com"
# A CLAUDE.md that says to load the doc standards.
source "$here/../add-claude-md.sh"
cp -R "$here/files/base/." .
git add -A
git commit -q -m "Add the functional and technical specs"
git checkout -q -b tasks
cp -R "$here/files/change/." .
git add -A
git commit -q -m "Define the app's parts and failed tasks, run the tasks that came due while the worker was stopped, and keep a failed task's error"
