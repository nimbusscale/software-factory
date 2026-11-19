# Adding or changing an item

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

CLAUDE.md's doc map says where each doc is. To decide what kind of fact it is, ask the questions in
"Which doc a fact goes in" in `project-docs.md`. To write it, follow "How to write any doc" there,
and for an item in a spec, "Spec items" in `specs.md`.

## The fact is written down once

Before adding anything, search for it. Grep the docs for its key terms, list the headings of the
doc it would go in, and read the sections that look close. Also grep the code for comments on it.

If it's already there, you're changing, replacing or deleting that item, not adding one. If
something close is there, decide whether it's the same fact, by the test in "One item for each
fact" in `specs.md`. If it is, you're changing that item. If not, yours is a new item.

A new item's ID is one more than the highest number with that prefix in the doc:

```bash
grep -oE '\bFR-[0-9]+' docs/functional-spec.md | grep -oE '[0-9]+$' | sort -n | tail -1
```

An ID that was retired and deleted can come back this way. That's accepted, since a retired ID
shouldn't be cited anywhere. Use only the doc's current text, not its git history.

## A changed item keeps its ID only if its meaning stayed the same

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

## It's in the section whose readers need it

- **Put it in the section whose readers need it.** Each section serves one kind of task.
- **Add a section** when no section's readers would look there.
- **Split a section** when it serves two tasks, and readers of one part never need the other. Don't
  split because it's long. Agents read one section at a time, so length costs them little.
- **Splitting retires the old section ID.** Both new sections get new IDs, and every reference to
  the old one changes in the same change. Renaming or moving a section keeps its ID.

## Everything that depended on it still holds

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

## The code and the docs agree

Change the code and the doc in the same change. When they disagree, "When a doc and the code
disagree" in `project-docs.md` says which one wins. Change the other to match. If you can't,
because the fix is outside your task or the code suggests the doc is wrong, leave both as they
are, and say so in your report. Name the item ID and the code.

## The change passes every check

Do every check in `reviewing.md`, last. Add its checklist to your task list under this one.
