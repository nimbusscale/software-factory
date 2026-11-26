---
tags: [write, items]
model: opus
max_turns: 60
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Write, Edit, Bash]
plugins: [../../../plugin]
append_system_prompt: |
  # CLAUDE.md

  Before you write, change or review a doc, or code that a doc describes, load the
  `software-factory:standards` skill. It holds the doc standards and the doc check script. If you
  can't load it, stop and say so in your report. Don't write the docs from memory of them.
---

Add tags to notes, so I can tag a note and list all the notes with a given tag. Keep the tags in their own tags.json file, not inside each note. Don't commit.
