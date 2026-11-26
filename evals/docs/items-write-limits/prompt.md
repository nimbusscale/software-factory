---
tags: [write, items]
model: opus
runs: 1
max_turns: 60
timeout_seconds: 1200
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

Write the functional spec for this app from the planning notes in notes/room-booking.md. Don't commit.
