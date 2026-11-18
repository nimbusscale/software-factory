---
plugins: ["../.."]
tags: [write, review-roles, passes-without-skill]
model: opus
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

/writing-project-docs You've just made the app email a member when it cancels their booking because nobody checked in. The change, a new requirement in the functional spec and the code for it, is in this working tree. Get it ready to commit.
