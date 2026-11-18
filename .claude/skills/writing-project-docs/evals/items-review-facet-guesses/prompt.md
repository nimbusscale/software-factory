---
plugins: ["../.."]
tags: [review, items]
model: opus
runs: 1
max_turns: 60
timeout_seconds: 1500
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

/writing-project-docs Review the change on this branch against main. The task was: write the functional spec for Facet, a self-hosted personal site, from its design doc in source/DESIGN.md. The design doc links to other Facet docs and a source file that aren't in this repo, so don't look for them. Facts that belong in a technical spec or anywhere other than the functional spec are left out on purpose, so leaving them out isn't a problem.
