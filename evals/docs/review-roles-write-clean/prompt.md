---
tags: [write, review-roles]
model: opus
runs: 1
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Write, Edit, Bash]
plugins: [../../../plugin]
append_system_prompt: |
  # CLAUDE.md

  ## Doc map

  | Doc | Path |
  |---|---|
  | Functional spec | `docs/functional-spec.md` |
  | Technical spec | `docs/technical-spec.md` |
  | Blueprints | `docs/blueprints/` |

  Before you write, change or review a doc, or code that a doc describes, load the
  `software-factory:standards` skill. It holds the doc standards and the doc check script. If you
  can't load it, stop and say so in your report. Don't write the docs from memory of them.
---

You've just made the app email a member when it cancels their booking because nobody checked in, to tell them that's why it was cancelled. The change, a new requirement in the functional spec and the code for it, is in this working tree. Get it ready to commit.
