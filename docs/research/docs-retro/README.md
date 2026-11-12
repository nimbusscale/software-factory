# docs-retro

The output of a retrospective on the docs of road-trip-agent, an earlier project where agents
built a multi-agent road trip planner. The project was a way to learn how to build agent systems,
and most of its docs were written and read by agents. The retrospective asked which docs helped,
which hurt, and what the next project should do instead.

All of it is research: references for the development loop and the skills built for it, not
things to use as they are. Whatever is taken from them gets fitted to the loop's workflow, and will
change on the way. The two skills are drafts of how docs and code comments could be written and
reviewed. The findings are the evidence and reasons behind them.

## project-docs/

A draft Claude Code skill for writing, changing and reviewing a project's docs. It's written to be
loaded whenever an agent is about to add or change a requirement, a decision or a reason, in a doc
or a code comment, or reviews a change that touches docs. It hasn't been tried on a real project
yet.

- `SKILL.md` holds the method, as steps in order: find the docs, check whether the fact is already
  written down, decide what kind of fact it is, decide whether to change, replace or delete an
  existing item, place it, write it, follow the change, and check it. The kind of fact decides its
  home: the functional spec, the technical spec, a code comment, a check, a skill, a research doc,
  a blueprint, or an issue. The last section, "What each doc holds", is the contract for each kind
  of doc.
- It sets the forms. Requirements are written in GEARS, a sentence pattern for requirements, with
  `FR` and `TR` IDs. Decisions are one line and a Why, with `AD` and `TD` IDs. Sections have
  `F-SEC` and `T-SEC` IDs.
- `references/worked-examples.md` sorts real passages from road-trip-agent with the skill's
  questions.
- `scripts/check-docs.sh` checks a change: history in the lines it added, IDs and links that don't
  resolve, items that don't fit their form, text copied between docs and code, and docs too big to
  read in one call. It only prints what it finds.
- `assets/` holds templates for each doc.

The skill assumes the project's CLAUDE.md holds a map of where each doc is and a table of where
each kind of fact goes.

## code-comments/

A draft Claude Code skill for writing, changing and reviewing code comments. It's written to be
loaded whenever an agent adds, changes or deletes a comment, moves code that has comments, or
reviews a change that touches comments. `project-docs` decides whether a fact goes in a comment or
a doc. This skill decides whether a comment is needed, and how to write it. It's a separate skill
because it's needed on almost every code change, and `project-docs` is too long to load for one
comment. It hasn't been tried on a real project yet.

- `SKILL.md` holds the method, as steps in order: decide whether to write a comment, decide what it
  holds, check each claim, place it, write it, keep it true when the code changes, and check the
  change.
- `references/worked-examples.md` sorts real comments from road-trip-agent with the skill's steps.

It draws on two outside skills, listed in the findings' sources, and on the same rules about
history, copies and IDs as `project-docs`.

## findings.md

A dated record of the retrospective. It isn't kept up to date. It holds:

- the evidence: what docs road-trip-agent had, how they grew, how agents read them, and where they
  helped or hurt, measured from git history and Claude Code transcripts
- what went wrong, and what the next project should do instead
- what road-trip-agent's code comments held, from a sorted sample
- the reasons behind the skills' choices, such as why GEARS, why IDs, why history is kept out of
  docs, and why comments get their own skill
- open items, several of them for the design of the development loop, such as what the workflow
  does with what the doc checks flag

Read it to understand or question a choice in either skill.
