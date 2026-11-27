---
tags: [review, items]
model: opus
runs: 1
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Write, Edit, Bash]
plugins: [../../../plugin]
append_system_prompt: |
  # CLAUDE.md

  Before you write, change or review a doc, or code that a doc describes, load the
  `software-factory:standards` skill. It holds the doc standards and the doc check script. If you
  can't load it, stop and say so in your report. Don't write the docs from memory of them.
---

Review the change on this branch against main.
