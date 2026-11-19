---
tags: [write, items]
model: opus
runs: 1
max_turns: 60
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Write, Edit, Bash]
append_system_prompt: |
  # CLAUDE.md

  ## Doc map

  | Doc | Path |
  |---|---|
  | Doc standards | `docs/standards/` |
  | Functional spec | `docs/functional-spec.md` |
  | Technical spec | `docs/technical-spec.md` |
  | Blueprints | `docs/blueprints/` |
  | Doc check script | `tools/check-docs.sh` |

  Before you write, change or review a doc, or code that a doc describes, read
  `docs/standards/README.md`. If you can't find the standards, stop and say so in your report.
  Don't write the docs from memory of them.
---

Write the functional spec for this app from the planning notes in notes/room-booking.md. Don't commit.
