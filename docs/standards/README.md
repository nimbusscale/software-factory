# Doc standards

The functional spec, the technical spec and blueprints are the input an agent turns into code.
These files say what each doc is, how it's written, how to change it, and how to check a change.
CLAUDE.md's doc map says where each doc is.

Two files here are about GitHub work, not docs: `github.md` and `board-statuses.yaml`. CLAUDE.md
points to them on their own, and the list below leaves them out.

## What to read for your task

Read every file that applies to your task. Most tasks need more than one.

- **Every task:** `project-docs.md`, which says which doc a fact goes in and how to write any doc.
  And `reports.md`, which says what goes in your report.
- **Writing in a doc, creating one, or checking a change to one:** the file for that kind of doc.
  Every doc opens with one line saying what kind of doc it is, so you know which of these apply.
  - Functional spec or technical spec: `specs.md`. It also says how to write each kind of item,
    the Terms section and IDs.
  - Blueprint: `blueprints.md`.
- **Adding, changing, replacing or deleting an item or a section,** in a doc or a code comment,
  or changing code that a doc describes: `changing-items.md`. It says what must hold when you're
  done.
- **Checking a change,** your own before you count the work as done, or someone else's:
  `reviewing.md`. Do every check in it.
- **Sorting a long passage that mixes several kinds of text:** `worked-examples.md`. It sorts real
  passages with the questions in "Which doc a fact goes in" in `project-docs.md`.

## A doc that doesn't exist yet

If a doc or a folder in the doc map doesn't exist yet, create it at the path the doc map gives.
Start a doc from its template in `templates/`. Say in your report that you created it.
