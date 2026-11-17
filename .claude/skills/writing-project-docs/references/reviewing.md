# Checking a change

Do these checks in two cases. When you change a doc, or change code a doc describes, check your own
change before you count the work as done. When you review someone else's change, check that
change.

## Your change or someone else's

- **Your own change:** fix each problem the change caused, then check again. You're done when
  nothing the change caused is left. Leave older problems alone, and don't mention them, even when
  the check script still flags them. They aren't part of your change, so a report on your change
  has nothing to say about them. When you report what the script found, say it found nothing from
  your change, and stop there. A decision with no Why, whose reason you asked for in your report,
  isn't yours to fix: the script flags it until the reason is known. Say in your report which flag
  goes with which question.
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

These checks cover the docs, and whether the code does what the docs say. A bug in the code that
doesn't make a doc wrong isn't part of them. Leave it out, and don't mention it.

A problem belongs to the change only if the change caused it. To tell, look at the same place on the
branch the change will merge into. If the problem is there too, it's older than the change. For
example, if a change to the code leaves a doc saying something the code no longer does, the change
caused that, even though it never touched the doc. If a requirement was already untestable before
the change, it's older, even when the change rewrote the paragraph around it.

Copy this checklist into your task list and tick off each check:

```
- [ ] Run the doc check script and decide each SIGNAL line
- [ ] Each item follows the rules for its kind of doc
- [ ] Nothing was dropped
- [ ] Nothing was added that the source didn't settle
- [ ] The rewrite stayed in scope
- [ ] No history got in
- [ ] One name for each thing
- [ ] No term states a rule
- [ ] Each citation in Terms earns its place
- [ ] One item for each fact
- [ ] Each requirement can be tested from its own text
- [ ] Each scenario earns its place
- [ ] Each requirement's Why passes both tests
- [ ] Every new item is in the right home
- [ ] Everything else in changing-a-doc.md holds
```

## Run the script

From the repo root, run this skill's `scripts/check-docs.sh` with the docs folder and the branch
the change will merge into, such as `bash <this skill's folder>/scripts/check-docs.sh docs main`.
It checks the specs and blueprints, and the spec IDs cited anywhere in the repo. It prints one line
per thing it flags. A `RULE` line is a broken rule, so it's always a problem. A
`SIGNAL` line is only something to look at. For each `SIGNAL` line, look at the line and decide
whether it's a real problem. It checks:

- **History,** as a signal: dates, issue and PR numbers, marker words (`settled`, `decided`,
  `drafted`, `assumption`, `for now`, `to come`, `in progress`), and words about the doc's past
  (`was` with `now`, `no longer`, `the new`, `used to`). Each can also be a real use, such as "no
  longer" in a requirement's While. It looks only at lines the change added, so a line kept on
  purpose isn't flagged again. It looks only at the specs, and leaves out scenarios.
- **References:** every link in a spec or a blueprint resolves. Every section ID and item ID
  cited anywhere in the repo resolves, such as in the code, CLAUDE.md or a skill. IDs are unique
  within a doc, and each prefix is in its own doc. No ID range is cited. The functional spec has
  no links out, and neither spec links to a blueprint. As a signal only, it lists each requirement that nothing cites
  now but something cited on the base branch, since it may have lost its code or its test. A
  requirement written before the code that meets it isn't flagged. With `--uncited`, it lists
  every requirement nothing cites instead, for a look at the docs and the code as a whole. A
  citation from a Terms section doesn't count for either, since a term only explains a word. It
  doesn't look outside the repo. "A changed item keeps its ID only if its meaning stayed the same"
  in `references/changing-a-doc.md` covers that.
- **Item shape:** each requirement follows GEARS, with one "shall", and has an ID. Each paragraph
  under a requirement starts with a label, such as `*Why:*`, or is a table the requirement's text
  points to. Each decision has a Why line right after it.
- **Copies,** as a signal: runs of eight or more words that a spec or a blueprint shares with
  another one, or with any other text file, such as a prompt or a README. Research docs are left
  out.
- **Size,** as a signal: a spec or a blueprint near the Read tool's 25,000-token limit, since past
  that an agent can't read it whole in one call.

## Then check by reading

- **Each item follows the rules for its kind of doc.** Each kind of doc has a file of its own
  rules, listed in "What to read for your task" in SKILL.md, such as
  `references/specs.md`. Read the file for each kind of doc the change touches. An item
  written the way that file asks isn't a problem, even when a rule in SKILL.md seems to say a part
  of it could go.
- **Nothing was dropped.** Compare each rewritten paragraph, old against new. `git diff
  --word-diff` on the doc shows them side by side. When the source is something else, such as
  another doc, an issue or notes from a conversation, go through it the same way. Every rule,
  condition and reason is still there, unless the task calls for cutting it. The task is what the
  change was made for, such as the issue it closes or the prompt that asked for it. It isn't the
  author's account of the change, such as a commit message or a PR description. A cut the task
  doesn't call for is a problem, whatever reason the author gives. If you weren't told the task,
  every cut is one. For each example, find the rule it shows, including any exception in it, such
  as "a gift card order earns no points". That rule must be in a requirement's text. The example
  itself can be cut even if the task doesn't mention it. It stays only as a scenario that earns its
  place.
- **Nothing was added that the source didn't settle.** For each rule the change adds or changes,
  find what settles it: the task, the source the change was written from, or the docs already
  there. A rule, or a part of one, that none of them settles is a problem, such as a time limit the
  source never states, or a meaning for a word the source never defines. So is a Why that none of
  them gives. A decision with no Why is fine when none of them gives a reason, as "No reason in the
  source?" in `references/specs.md` says. The author's account of
  the change settles nothing, even when it lists the point as open. The suggested rewrite cuts
  what wasn't settled and raises it as a question, as "Not settled by the source?" in SKILL.md
  says. If you weren't given the task or the source, skip this check, and say in your report that
  you skipped it and why.
- **The rewrite stayed in scope.** It touches only the paragraphs the task needed. A rewrite that
  spreads further belongs in a separate change.
- **No history got in.** The script catches fixed patterns. Look for what it can't, such as "the
  check now runs first". Every line describes the present.
- **One name for each thing.** For each term, and each name an item introduces, grep for it and
  for likely variants, such as "checkout step" and "checkout". Every use is the one name, with no
  variants. For each word two names share, grep for it on its own. Every use is the full name, not
  the bare word, unless the shared word is a term that lists the kinds it covers. Then a bare use
  means every kind, so check that what the sentence says is true of every kind. Every word that
  names a thing is in Terms or carries a citation. Then grep for each term's word and its other
  forms, such as "turned" and "turning" for "turn". Every use has the term's meaning, or no reader
  could take it for the term. A set phrase whose meaning has nothing to do with the term is fine,
  such as "in order to" when Order is a customer's purchase. A use a reader could take for the
  term is a problem, and needs a different word. Most often, the word stands on its own, or says
  something about the same things the term does. For example, "the player may turn a tile" when
  Turn is a player's go.
- **No term states a rule.** For each part of each definition, apply the test in "The Terms
  section" in `references/specs.md`: if a requirement changed, would this part have to change too? A part that
  would is a problem, such as "the one" in a term when a requirement allows only one. So is a part
  the app must do or check that no requirement holds.
- **Each citation in Terms earns its place.** A term cites a requirement only when its meaning
  depends on that requirement's rule. Cover each requirement citation and read the term. If the
  word's meaning is still clear, the citation is a problem. A requirement that creates the thing,
  or decides who fills a role, such as who a loan's borrower is, isn't a reason to cite it. A
  term cites a section only when that section holds the rules for the thing it names. Any other
  citation on a term is a problem.
- **One item for each fact.** For each pair of items that limit the same action or share a trigger,
  apply the test in "One item for each fact" in `references/specs.md`. A pair that's one fact is a problem.
  Apply it as well to the triggers of each requirement with more than one. Triggers that are two
  facts in one requirement are a problem. So is a list of triggers that repeats the members of a
  set another requirement defines.
- **Each requirement can be tested from its own text and the Terms.** You could write a test from
  it alone.
- **Each scenario earns its place:** its result comes from several requirements together, it can
  happen under the other requirements, and it holds no rule that isn't in a requirement.
- **Each requirement's Why passes both tests** in "Lines under an item" in `references/specs.md`. A Why that
  fails either test is a problem.
- **Every new item is in the right home,** by the questions in "Which doc a fact goes in" in
  SKILL.md.
- **Everything else in `references/changing-a-doc.md` holds.**
