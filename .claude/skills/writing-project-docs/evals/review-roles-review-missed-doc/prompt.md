---
plugins: ["../.."]
tags: [review, review-roles, passes-without-skill]
model: opus
runs: 1
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

/writing-project-docs Review the change on this branch against main.
