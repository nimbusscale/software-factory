# Blueprints

The standards for a blueprint: what it holds, and how it changes. The questions in "Which doc a
fact goes in", in `project-docs.md` in this folder, decide which facts go in one.

Read by the agents building the code it describes. It holds whatever is useful to build from
before the code exists, and nothing is ruled out. It can link to other docs, but other docs don't
link to it, since it's archived once the code is built. It's edited freely until then. It never
names a skill, since skills change and are used in other projects.

## Status

A blueprint opens with front matter that says whether it's still the plan to build from:

```yaml
---
status: active
retired:
---
```

`status` is `active` until the blueprint retires, then `retired`. `retired` is empty until then,
then the date it retired, such as `2026-11-18`.

The status is about the doc only. It never tracks progress through the work, such as "phase 3
done". Progress is about the work in progress, so it goes in the commit message, as question 1 in
"Which doc a fact goes in" says.

## Retiring

The task that builds the code also retires the blueprint. It's retired when all of these hold:

- Each item that new code elsewhere could break is in the technical spec, sorted by the questions
  in "Which doc a fact goes in" in `project-docs.md`.
- Each rule about one object is a code comment or a test.
- Each rule a check can enforce is a check, such as a lint rule for imports.
- Its data and settings, such as a list of items and their weights, are in the files the code
  reads.
- The doc is archived, frozen, with `status: retired` and the date in `retired`.
