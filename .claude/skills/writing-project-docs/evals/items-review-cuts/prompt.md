---
plugins: ["../.."]
tags: [review, items, passes-without-skill]
model: opus
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

/writing-project-docs Review the change on this branch against main. The task was: the office no longer lends projectors, so take projectors out of the spec.
