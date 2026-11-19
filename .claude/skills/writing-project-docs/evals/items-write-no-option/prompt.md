---
plugins: ["../.."]
tags: [write, items]
model: opus
max_turns: 60
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

/writing-project-docs Write the technical spec for this app from the architecture notes in notes/architecture.md. Don't commit.
