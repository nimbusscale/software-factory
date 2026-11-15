---
plugins: ["../.."]
tags: [terms, review]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

/writing-project-docs Review the change on this branch against main. It adds terms to the functional spec in docs/functional-spec.md. Fix any problems you find by editing the file. Don't commit.
