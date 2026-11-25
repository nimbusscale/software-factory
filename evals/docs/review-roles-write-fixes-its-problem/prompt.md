---
tags: [write, review-roles]
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

You've just made the app email a member when it cancels their booking because nobody checked in. The change, a new requirement in the functional spec and the code for it, is in this working tree. Get it ready to commit.
