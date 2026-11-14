# Checking a change

When you change a doc, or change code a doc describes, do these checks before you count the work
as done. When you review someone else's change, do them on that change.

## Run the script

From the repo root, run this skill's `scripts/check-docs.sh` with the docs folder and the branch
the change will merge into, such as `bash <this skill's folder>/scripts/check-docs.sh docs main`.
It prints one line per thing it flags. A `RULE` line is a broken rule. A `SIGNAL` line is only
something to look at. For each `SIGNAL` line, look at the line and decide. Fix it if it's a real
problem, and leave it if it isn't. How a reviewer reports what it found is up to the project's
workflow. It checks:

- **History,** as a signal: dates, issue and PR numbers, marker words (`settled`, `decided`,
  `drafted`, `assumption`, `for now`, `to come`, `in progress`), and words about the doc's past
  (`was` with `now`, `no longer`, `the new`, `used to`). Each can also be a real use, such as "no
  longer" in a requirement's While. It looks only at lines the change added, so a line kept on
  purpose isn't flagged again. Code, scenarios, research docs and blueprints are left out.
- **References:** every doc link, section ID and item ID cited in the docs or the code resolves.
  IDs are unique within a doc, and each prefix is in its own doc. No ID range is cited. The
  functional spec has no links out. No research doc links to another doc, and no other doc links
  to a research doc or a blueprint. As a signal only, it lists requirement IDs that nothing cites, since they may
  be unbuilt or untested. It doesn't look in open issues. Step 7 of `references/changing-a-doc.md`
  covers those.
- **Item shape:** each requirement follows GEARS, with one "shall", and has an ID. Each decision
  has a Why line right after it.
- **Copies,** as a signal: runs of eight or more words that a doc shares with a source file, such
  as a prompt, or with another doc.
- **Size,** as a signal: a doc near the Read tool's 25,000-token limit, since past that an agent
  can't read it whole in one call.

## Then check by reading

- **Nothing was dropped.** Compare each rewritten paragraph, old against new. `git diff
  --word-diff` on the doc shows them side by side. Every rule, condition, reason and example is
  still there, or the PR says it was cut on purpose.
- **The rewrite stayed in scope.** It touches only the paragraphs the task needed. A rewrite that
  spreads further goes in a separate change.
- **No history got in.** The script catches fixed patterns. Look for what it can't, such as "the
  check now runs first", and rewrite it as the present.
- **Every new item is in the right home,** by the questions in "Which doc a fact goes in" in
  SKILL.md, and every other step in `references/changing-a-doc.md` holds.

A doc that's wrong or out of step with the code is a fix in the PR, not a review note.
