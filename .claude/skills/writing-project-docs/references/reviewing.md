# Checking a change

Do these checks in two cases. When you change a doc, or change code a doc describes, check your own
change before you count the work as done. When you review someone else's change, check that
change.

## Your change or someone else's

- **Your own change:** fix each problem you find, then check again.
- **Someone else's change:** edit nothing, and report each problem you find. Put each problem in
  one of two lists. **Problems in this change** go back to whoever made it. **Older problems** were
  there before the change. Each problem in either list says four things:
  - Where it is: the file and line, or the item ID.
  - What's wrong, and which check it fails.
  - A suggested rewrite.
  - Why the rewrite fixes it.

  The task says how to deliver the two lists, such as in chat, as JSON or through a tool, and what
  happens to the older problems. When it doesn't say, give both lists in your reply.

## What to check

Check what the change added or changed since the branch it will merge into. For a new doc, that's
the whole doc. Some checks also look past the change, such as grepping every doc for a term's other
uses. When the change touches code, grep the docs for the names of what it touched, such as a
function, a setting or a behavior. Read each item that comes up, and check it still holds.

A problem belongs to the change only if the change caused it. To tell, look at the same place on
the branch the change will merge into. If the problem is there too, it's older than the change.
In your own change, leave it alone and don't mention it. For example, if a change to the code leaves a doc saying
something the code no longer does, the change caused that, even though it never touched the doc.
If a requirement was already untestable before the change, it's older, even when the change
rewrote the paragraph around it.

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
It prints one line per thing it flags. A `RULE` line is a broken rule, so it's always a problem. A
`SIGNAL` line is only something to look at. For each `SIGNAL` line, look at the line and decide
whether it's a real problem. It checks:

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
  spreads further belongs in a separate change.
- **No history got in.** The script catches fixed patterns. Look for what it can't, such as "the
  check now runs first". Every line describes the present.
- **One name for each thing.** For each term, and each name an item introduces, grep for it and
  for likely variants, such as "checkout step" and "checkout". Every use is the one name, with no
  variants. For each word two names share, grep for it on its own. Every use is the full name, not
  the bare word. Every word that names a thing is in Terms or carries a citation. Then grep for
  each term's word and its other forms, such as "turned" and "turning" for "turn". Every use has
  the term's meaning. A use with another meaning needs a different word.
- **Each citation in Terms earns its place.** A term cites a requirement only when its meaning
  depends on that requirement's rule. It cites a section only when that section holds the rules for
  the thing it names. Any other citation on a term is a problem.
- **One item for each fact.** For each pair of items that limit the same action or share a trigger,
  apply the test in "One item for each fact" in SKILL.md. A pair that's one fact is a problem.
- **Each requirement can be tested from its own text and the Terms.** You could write a test from
  it alone.
- **Each scenario earns its place:** its result comes from several requirements together, it can
  happen under the other requirements, and it holds no rule that isn't in a requirement.
- **Each requirement's Why passes both tests** in "Lines under an item" in SKILL.md. A Why that
  fails either test is a problem.
- **Every new item is in the right home,** by the questions in "Which doc a fact goes in" in
  SKILL.md.
- **Every other step in `references/changing-a-doc.md` holds.**
