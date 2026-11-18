---
plugins: ["../.."]
tags: [write, items]
model: opus
runs: 1
max_turns: 60
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

/writing-project-docs Write the functional spec for this app from the planning notes in notes/personal-site.md. Don't commit.
