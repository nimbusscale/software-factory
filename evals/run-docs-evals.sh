#!/usr/bin/env bash
# Runs the doc eval cases in evals/docs, with the flags every run uses. Any other flags, such as
# --case, --tag or --runs, are passed on to claude plugin eval.
#
# Before the run, it sets three things in every case from one shared copy, so every case matches:
# - The plugins line in prompt.md, which loads the factory plugin from this repo's plugin/.
# - append_system_prompt in prompt.md, from docs/project-claude.md. plugin eval loads no
#   CLAUDE.md, so this is how the agent gets the test project's.
# - graders/00-loads-standards.md, from docs/loads-standards-grader.md.
set -eu
evals=$(cd "$(dirname "$0")" && pwd)
python3 -I - "$evals/docs" <<'PY'
import glob, os, sys
root = sys.argv[1]
text = open(os.path.join(root, "project-claude.md")).read().rstrip("\n").split("\n")
block = ["append_system_prompt: |"] + [("  " + l) if l else "" for l in text]
plugins = "plugins: [../../../plugin]"
grader = open(os.path.join(root, "loads-standards-grader.md")).read()


def write_if_changed(path, new):
    old = open(path).read() if os.path.exists(path) else None
    if new != old:
        open(path, "w").write(new)
        print(f"updated {os.path.relpath(path, root)}")


for path in sorted(glob.glob(os.path.join(root, "*", "prompt.md"))):
    lines = open(path).read().split("\n")
    if lines[0] != "---":
        sys.exit(f"{path} has no front matter")
    end = lines.index("---", 1)
    fm = [l for l in lines[1:end] if not l.startswith("plugins:")]
    at = len(fm)
    if block[0] in fm:
        at = fm.index(block[0])
        stop = at + 1
        while stop < len(fm) and (fm[stop].startswith("  ") or fm[stop] == ""):
            stop += 1
        fm = fm[:at] + fm[stop:]
    fm = fm[:at] + [plugins] + block + fm[at:]
    write_if_changed(path, "\n".join(["---"] + fm + lines[end:]))
    write_if_changed(os.path.join(os.path.dirname(path), "graders", "00-loads-standards.md"), grader)
PY
# Run from the repo's root, since plugin eval loads a case's plugins only from inside the folder
# it runs on.
cd "$evals/.."
exec claude plugin eval . --eval-dir evals/docs --scaffold --allow-tools Write,Edit,Bash \
  --judge-model sonnet -j 8 --ablation none --trust-plugin "$@"
