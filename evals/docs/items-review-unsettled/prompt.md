---
tags: [review, items]
model: opus
max_turns: 40
timeout_seconds: 900
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
  | Doc check script | `docs/standards/check_docs.py` |

  Before you write, change or review a doc, or code that a doc describes, read
  `docs/standards/SKILL.md`. If you can't find the standards, stop and say so in your report.
  Don't write the docs from memory of them.
---

Review the change on this branch against main. The task was: add waitlists to the spec, from the planning notes in notes/waitlists.md.
