#!/usr/bin/env bash
# Runs the doc eval cases in evals/docs, with the flags every run uses. Any other flags, such as
# --case, --tag or --runs, are passed on to claude plugin eval.
#
# plugin eval loads no CLAUDE.md, so each case gives the agent the test project's CLAUDE.md through
# append_system_prompt in its prompt.md. That text lives in docs/project-claude.md. This script
# copies it into every case's prompt.md before the run, so every copy matches it.
set -eu
evals=$(cd "$(dirname "$0")" && pwd)
python3 -I - "$evals/docs" <<'PY'
import glob, os, sys
root = sys.argv[1]
text = open(os.path.join(root, "project-claude.md")).read().rstrip("\n").split("\n")
block = ["append_system_prompt: |"] + [("  " + l) if l else "" for l in text]
for path in sorted(glob.glob(os.path.join(root, "*", "prompt.md"))):
    old = open(path).read()
    lines = old.split("\n")
    if lines[0] != "---":
        sys.exit(f"{path} has no front matter")
    end = lines.index("---", 1)
    fm = lines[1:end]
    at = len(fm)
    if block[0] in fm:
        at = fm.index(block[0])
        stop = at + 1
        while stop < len(fm) and (fm[stop].startswith("  ") or fm[stop] == ""):
            stop += 1
        fm = fm[:at] + fm[stop:]
    new = "\n".join(["---"] + fm[:at] + block + fm[at:] + lines[end:])
    if new != old:
        open(path, "w").write(new)
        print(f"updated {os.path.relpath(path, root)}")
PY
cd "$evals"
exec claude plugin eval . --eval-dir docs --scaffold --allow-tools Write,Edit,Bash \
  --judge-model sonnet -j 8 --ablation none --trust-plugin "$@"
