---
plugins: ["../.."]
tags: [review, items]
model: opus
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

/writing-project-docs Review the change on this branch against main. The task was: add waitlists to the spec, from the planning notes in notes/waitlists.md.
