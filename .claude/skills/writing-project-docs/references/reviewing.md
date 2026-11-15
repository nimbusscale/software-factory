# Checking a change

When you change a doc, or change code a doc describes, do these checks before you count the work
as done. When you review someone else's change, do them on that change.

Copy this checklist into your task list and tick off each check:

```
- [ ] Run the doc check script and decide each SIGNAL line
- [ ] Nothing was dropped
- [ ] The rewrite stayed in scope
- [ ] No history got in
- [ ] One name for each thing
- [ ] Each citation in Terms earns its place
- [ ] One item for each fact
- [ ] Each requirement can be tested from its own text
- [ ] Each scenario earns its place
- [ ] Each requirement's Why passes both tests
- [ ] Every new item is in the right home
- [ ] Every other step in changing-a-doc.md holds
```

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
  be unbuilt or untested. A citation from a Terms section doesn't count for this, since a term
  only explains a word. It doesn't look in open issues. Step 7 of `references/changing-a-doc.md`
  covers those.
- **Item shape:** each requirement follows GEARS, with one "shall", and has an ID. Each decision
  has a Why line right after it.
- **Copies,** as a signal: runs of eight or more words that a doc shares with a source file, such
  as a prompt, or with another doc.
- **Size,** as a signal: a doc near the Read tool's 25,000-token limit, since past that an agent
  can't read it whole in one call.

## Then check by reading

- **Nothing was dropped.** Compare each rewritten paragraph, old against new. `git diff
  --word-diff` on the doc shows them side by side. When the source is something else, such as
  another doc, an issue or notes from a conversation, go through it the same way. Every rule,
  condition, reason and example is still there, or the PR says it was cut on purpose.
- **The rewrite stayed in scope.** It touches only the paragraphs the task needed. A rewrite that
  spreads further goes in a separate change.
- **No history got in.** The script catches fixed patterns. Look for what it can't, such as "the
  check now runs first", and rewrite it as the present.
- **One name for each thing.** For each term, and each name an item introduces, grep for it and
  for likely variants, such as "checkout step" and "checkout". Make every variant the one name. For
  each word two names share, grep for it on its own and change each bare use to the full name.
  Every word that names a thing is in Terms or carries a citation. Then grep for each term's word
  and its other forms, such as "turned" and "turning" for "turn". Check that every use has the
  term's meaning, and change any use with another meaning to a different word.
- **Each citation in Terms earns its place.** A term cites a requirement only when its meaning
  depends on that requirement's rule. It cites a section only when that section holds the rules for
  the thing it names. Remove any other citation from a term.
- **One item for each fact.** For each pair of items that limit the same action or share a trigger,
  apply the test in "One item for each fact" in SKILL.md. Merge any pair that's one fact.
- **Each requirement can be tested from its own text and the Terms.** If you couldn't write a test
  from it alone, rewrite it.
- **Each scenario earns its place:** its result comes from several requirements together, it can
  happen under the other requirements, and it holds no rule that isn't in a requirement.
- **Each requirement's Why passes both tests** in "Lines under an item" in SKILL.md. Cut any that
  fails.
- **Every new item is in the right home,** by the questions in "Which doc a fact goes in" in
  SKILL.md.
- **Every other step in `references/changing-a-doc.md` holds.**

A doc that's wrong or out of step with the code is a fix in the PR, not a review note.
