# Adding or changing an item

Use these steps to add, change, replace or delete an item or a section, in a doc or a code
comment, and when a code change makes a doc out of step. Work through them in order. Each one depends on the one before. Steps 1, 3 and 6 are sections of
SKILL.md, and step 8 is `references/reviewing.md`. They're listed here so the order is clear.

## 1. Find the docs

Follow "Find the docs" in SKILL.md.

## 2. Check whether it's already written down

Before adding anything, search for it. Grep the docs for its key terms, list the headings of the
doc it would go in, and read the sections that look close. Also grep the code for comments on it.

If it's already there, you're changing, replacing or deleting an item, not adding one. Go to
step 4. If something close is there, decide whether yours is the same item said better, or a
different one.

## 3. Decide what kind of fact it is

Ask the questions in "Which doc a fact goes in" in SKILL.md.

## 4. Decide whether to change, replace or delete the item

This step is for an item step 2 found already written down. For a new fact, go on to step 5.

**If the meaning stays the same, change it in place and keep its ID.** Sharpening the wording,
adding an example, or adding a condition that was always meant are all changes. Everything that
cites the item still agrees with it. Rewrite the whole paragraph so it reads as if written in one
go. Don't append an exception to the end. A rule that collects exceptions turns into a paragraph
nobody can cite.

**If the meaning changes, replace it.** It's now a different requirement or decision, such as
showing times in each stop's time zone instead of the browser's. Delete the old item and add the
new one with a new ID. Every place that still cites the old ID is now flagged by the doc checks,
so you visit each one and update it to fit the new meaning. If you kept the old ID, those places
would look fine but describe or test the old behavior.

**If the item isn't needed at all, delete it.** The doc checks flag each place that still cites
it. Remove or update each one.

## 5. Decide where it goes in the doc

- **Put it in the section whose readers need it.** Each section serves one kind of task.
- **Add a section** when no section's readers would look there.
- **Split a section** when it serves two tasks, and readers of one part never need the other. Don't
  split because it's long. Agents read one section at a time, so length costs them little.
- **Splitting retires the old section ID.** Both new sections get new IDs, and every reference to
  the old one changes in the same PR. Renaming or moving a section keeps its ID.

## 6. Write it

Follow "How to write an item" in SKILL.md.

## 7. Follow the change

- **If your edit makes something true that wasn't, or untrue that was,** search every doc for
  items whose Where or While depends on it. This holds for adding a new item too, not only for
  changing, replacing or deleting one. Search by its terms, not by ID. Items that depend on the
  same fact often don't cite each other, so no check links them. For example, a new item says
  signup sets the user's time zone from their address. An older item says "While the user hasn't
  set a time zone, the app shall show times in the browser's time zone." Neither cites the other,
  but the older one no longer applies to new users. For each item that no longer holds, decide
  whether to change, replace or delete it, as in step 4.
- **If you replaced or deleted an item,** search open issues for its old ID and update each one.
  The doc checks find it in the docs and the code, but not in issues.
- **Change the code and the doc in the same PR.** When they disagree, CLAUDE.md says which one wins.

## 8. Check the change

Do every check in `references/reviewing.md`.
