---
name: standards
description: Says which of the software factory's standards to read for a task, and holds them and the doc check script. Load it before you write, change or review a doc, code a doc describes, a code comment, a test, an issue or a PR's description. Then read only the files your task needs.
---

# Doc standards

The functional spec, the technical spec and blueprints are the input an agent turns into code.
These files say what each doc is, how it's written, how to change it, and how to check a change.
`code-comments.md` does the same for code comments, which hold the facts one place in the code
owns. CLAUDE.md's doc map says where each doc is.

Every file these standards name, such as `templates/blueprint.md` or `check_docs.py`, is in the
folder this file is in.

Three files here aren't about docs, and the list below leaves them out. `github.md` is about GitHub
work, and CLAUDE.md points to it on its own. `review-rubric.md` is the rubric the quality reviewer
labels its findings with, and the quality reviewer's prompt points to it. `tests.md` is about a
project's tests. Whoever writes or changes a test reads it, and CLAUDE.md points to it on its own.
The implementer's and the quality reviewer's prompts point to it too.

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
- **Adding, changing or deleting a code comment,** moving code that has comments, or checking a
  change that does: `code-comments.md`. It says when a comment is needed and how it's written.
- **Checking a change,** your own before you count the work as done, or someone else's:
  `reviewing.md`. Do every check in it.
- **Sorting a long passage that mixes several kinds of text:** `worked-examples.md`. It sorts real
  passages with the questions in "Which doc a fact goes in" in `project-docs.md`.

## A doc that doesn't exist yet

If a doc or a folder in the doc map doesn't exist yet, create it at the path the doc map gives.
Start a doc from its template in `templates/`. Say in your report that you created it.
