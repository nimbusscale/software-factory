---
name: writing-project-docs
description: Writes, changes and reviews a project's functional spec, technical spec and blueprints, and decides whether a fact goes in one of them, a code comment or a check. Use when adding, changing or removing a requirement, a decision or a reason in a spec, a blueprint or a code comment, creating a spec or a blueprint, or reviewing a change that touches them, even if the task only says "update the spec", "write down why" or "document this", or is a code change that makes a spec out of step.
disable-model-invocation: true
---

# Writing project docs

The functional spec, the technical spec and blueprints are the input an agent turns into code.
This skill is how to do work on them: change a doc, check a change, and report what you found.
What the docs are and how they're written is in the project's doc standards, a folder of files
kept apart from this skill. Every task here follows them.

## What to read for your task

Before you start, find the standards and the docs, as "Find the docs" below says. Then read every
file that applies to your task. Most tasks need more than one.

- **Every task:** the standards' `project-docs.md`. It says which doc a fact goes in, and how to
  write any doc.
- **Writing in a doc, creating one, or checking a change to one:** the standards' file for that
  kind of doc. Every doc opens with one line saying what kind of doc it is, so you know which of
  these apply.
  - Functional spec or technical spec: `specs.md`. It also says how to write each kind of item,
    the Terms section and IDs.
  - Blueprint: `blueprints.md`.
- **Adding, changing, replacing or deleting an item or a section,** in a doc or a code comment,
  or changing code that a doc describes: follow "Adding or changing an item" below. It says what
  must hold when you're done.
- **Checking a change,** your own before you count the work as done, or someone else's: read
  [references/reviewing.md](references/reviewing.md) and do every check in it.
- **Sorting a long passage that mixes several kinds of text:** read
  [references/worked-examples.md](references/worked-examples.md). It sorts real passages with the
  questions in "Which doc a fact goes in".

## Find the docs

CLAUDE.md's doc map says where each kind of doc is, and where the standards are. Use it when it
names a path. When it doesn't, look in the defaults:

| Doc | Default path |
|---|---|
| Doc standards | `docs/standards/` |
| Functional spec | `docs/functional-spec.md` |
| Technical spec | `docs/technical-spec.md` |
| Blueprints | `docs/blueprints/` |

If the standards aren't at their default, search for them by file name:

```bash
find . -name project-docs.md -not -path './.git/*'
```

If you can't find them, stop, and say in your report that the project has no doc standards. Don't
write the docs from memory of them.

If a spec isn't at its default, search for its section IDs. They only appear in its own headings,
so they find the right file even though other docs cite its item IDs:

```bash
grep -rlE '^#+ F-SEC-[0-9]+' --include='*.md' .   # functional spec
grep -rlE '^#+ T-SEC-[0-9]+' --include='*.md' .   # technical spec
```

If the blueprints folder doesn't exist, create it in the same folder as the specs. If a
doc doesn't exist yet, create it at its default path from its template in the standards'
`templates/` folder, and say in your report that you created it.

## Adding or changing an item

Use this to add, change, replace or delete an item or a section, in a doc or a code comment, and
when a code change makes a doc out of step. Each heading below is something that must hold when
you're done. Two of them have to come in order. Search for the fact before you write anything,
since what you find decides whether you add an item or change one. Check the change last.

Copy this checklist into your task list, and tick off each one once it holds:

```
- [ ] The fact is written down once
- [ ] A changed item keeps its ID only if its meaning stayed the same
- [ ] It's in the section whose readers need it
- [ ] Everything that depended on it still holds
- [ ] The code and the docs agree
- [ ] The change passes every check
```

To find the docs and the standards, follow "Find the docs" above. To decide what kind of
fact it is, ask the questions in "Which doc a fact goes in" in the standards' `project-docs.md`. To
write it, follow "How to write any doc" there, and for an item in a spec, "Spec items" in the
standards' `specs.md`.

### The fact is written down once

Before adding anything, search for it. Grep the docs for its key terms, list the headings of the
doc it would go in, and read the sections that look close. Also grep the code for comments on it.

If it's already there, you're changing, replacing or deleting that item, not adding one. If
something close is there, decide whether it's the same fact, by the test in "One item for each
fact" in the standards' `specs.md`. If it is, you're changing that item. If not, yours is a new item.

A new item's ID is one more than the highest number with that prefix in the doc:

```bash
grep -oE '\bFR-[0-9]+' docs/functional-spec.md | grep -oE '[0-9]+$' | sort -n | tail -1
```

An ID that was retired and deleted can come back this way. That's accepted, since a retired ID
shouldn't be cited anywhere. Use only the doc's current text, not its git history.

### A changed item keeps its ID only if its meaning stayed the same

**If the meaning stays the same, change it in place and keep its ID.** Sharpening the wording,
adding an example, or adding a condition that was always meant are all changes. Everything that
cites the item still agrees with it. Rewrite the whole paragraph so it reads as if written in one
go. Don't append an exception to the end. A rule that collects exceptions turns into a paragraph
nobody can cite.

**If the meaning changes, replace it.** It's now a different requirement or decision, such as
showing times in a time zone the user picks, instead of the browser's. Delete the old item and add
the new one with a new ID. Every place that still cites the old ID is now flagged by the doc
checks, so you visit each one and update it to fit the new meaning. If you kept the old ID, those
places would look fine but describe or test the old behavior.

**If the item isn't needed at all, delete it.** The doc checks flag each place that still cites
it. Remove or update each one.

**If you replaced or deleted an item,** name its old ID in your report. The doc checks find
citations in the docs and the code, but not in anything outside the repo, such as a planned task
that cites the ID.

### It's in the section whose readers need it

- **Put it in the section whose readers need it.** Each section serves one kind of task.
- **Add a section** when no section's readers would look there.
- **Split a section** when it serves two tasks, and readers of one part never need the other. Don't
  split because it's long. Agents read one section at a time, so length costs them little.
- **Splitting retires the old section ID.** Both new sections get new IDs, and every reference to
  the old one changes in the same change. Renaming or moving a section keeps its ID.

### Everything that depended on it still holds

- **If your edit makes something true that wasn't, or untrue that was,** search every doc for
  items whose Where or While depends on it. This holds for adding a new item too, not only for
  changing, replacing or deleting one. Search by its terms, not by ID. Items that depend on the
  same fact often don't cite each other, so no check links them. For example, a new item says
  signup sets the user's time zone from their address. An older item says "While the user hasn't
  set a time zone, the app shall show times in the browser's time zone." Neither cites the other,
  but the older one no longer applies to new users. For each item that no longer holds, decide
  whether to change, replace or delete it, as "A changed item keeps its ID only if its meaning
  stayed the same" says.
- **If you added a name that shares a word with an existing one,** grep the docs and code comments
  for the shared word on its own, and change each use to the full name in the same change.

### The code and the docs agree

Change the code and the doc in the same change. When they disagree, "When a doc and the code
disagree" in the standards' `project-docs.md` says which one wins. Change the other to match. If
you can't, because the fix is outside your task or the code suggests the doc is wrong, leave both
as they are, and say so in your report. Name the item ID and the code.

### The change passes every check

Do every check in [references/reviewing.md](references/reviewing.md), last. Add its checklist to your task list under this
one.

## What goes in your report

The questions in "Which doc a fact goes in" sort some facts out of the docs. Each of those goes in
your report, so whoever gave you the task can decide what happens to it next:

- **About the past or the work in progress** (question 1). Keep notes in a file in the session's
  scratchpad while you work, and write the commit message from them. Name any work left to do.
- **About something other than what the app does and how it's built** (question 2), including
  commands and pointers kept out of the technical spec. Name it, with where it likely belongs,
  such as a skill, a research doc or a README.
- **A decision not made yet.** Name it as a decision still to make, such as one that needs a spike
  to settle.
- **Not settled by the source,** including an option named with "may", "could" or "such as".
  Raise it as a question: quote the source text, say what's unclear, and suggest an answer. When a
  sentence only makes sense under one option, ask about the two together. For example, when notes
  say an app "may keep a copy of the orders on the phone" and that the order list "syncs to the
  phone", ask whether the app keeps a copy, and say the sync depends on the answer.
- **A decision with no reason in the source.** Ask for the reason: quote the decision, and suggest
  a reason if you have one. If you can't tell whether anyone had another option, ask that too: was
  another way weighed, and if so, why this one? The check script flags the missing Why until the
  reason is known. A fact with no other option isn't a decision, so don't ask for its reason. Say
  where its home is instead.
