---
name: writing-project-docs
description: Writes, changes and reviews a project's docs (functional spec, technical spec, skills, research docs, blueprints), and decides whether a fact goes in a doc, a code comment, a check or an issue. Use when adding, changing or removing a requirement, a decision or a reason in any doc or code comment, creating a doc, or reviewing a change that touches docs, even if the task only says "update the spec", "write down why" or "document this", or is a code change that makes a doc out of step.
disable-model-invocation: true
---

# Writing project docs

Most readers of these docs are agents. They list a doc's headings, read one section, and act on
it. So every item has to be findable by its heading, make sense on its own, and say exactly what
it means. Every fact has one home, and other places point to it by ID. A second copy drifts, and
an agent can't tell which copy is right.

## What to read for your task

This file holds what every task needs: where the docs are, which doc a fact goes in, and how to
write any doc. The files below hold the rest. Before you start, read every file that applies to
your task. Most tasks need more than one.

- **Adding, changing, replacing or deleting an item or a section,** in a doc or a code comment,
  or changing code that a doc describes: read
  [references/changing-a-doc.md](references/changing-a-doc.md). It gives the steps in order.
- **Writing in a doc, creating one, or checking a change to one:** read the file for that kind of
  doc. It says what the doc holds and keeps out, how it changes, and how to write any kind of item
  only that doc has. Every doc opens with one line saying what kind of doc it is, so a reader knows
  which of these apply.
  - Functional spec or technical spec: [references/specs.md](references/specs.md). It also says
    how to write each kind of item, the Terms section and IDs.
  - Research doc: [references/research-doc.md](references/research-doc.md)
  - Blueprint: [references/blueprint.md](references/blueprint.md)
  - Skill: [references/skill.md](references/skill.md)
  - CLAUDE.md: [references/claude-md.md](references/claude-md.md)
- **Checking a change,** your own before you count the work as done, or someone else's: read
  [references/reviewing.md](references/reviewing.md) and do every check in it. Also read the
  file above for each kind of doc the change touches.

## Find the docs

CLAUDE.md's doc map says where each kind of doc is. Use it when it names a path. When it doesn't,
look in the defaults:

| Doc | Default path |
|---|---|
| Functional spec | `docs/functional-spec.md` |
| Technical spec | `docs/technical-spec.md` |
| Research docs | `docs/research/` |
| Blueprints | `docs/blueprints/` |
| Skills | `.claude/skills/<name>/SKILL.md` |

If a spec isn't at its default, search for its section IDs. They only appear in its own headings,
so they find the right file even though other docs cite its item IDs:

```bash
grep -rlE '^#+ F-SEC-[0-9]+' --include='*.md' .   # functional spec
grep -rlE '^#+ T-SEC-[0-9]+' --include='*.md' .   # technical spec
```

If a research or blueprints folder doesn't exist, create it in the same folder as the specs. If a
doc doesn't exist yet, create it at its default path from the template in `assets/`, and say in
your report that you created it.

## Which doc a fact goes in

CLAUDE.md's table gives the short version. These questions are the long version. Ask them in this
order, and stop at the first yes.

1. **Is it about the past or the work in progress?** When something was decided, by whom, what
   was tried in a session, status, open items. It goes in the commit, the PR or an issue, never a
   doc. Keep notes in a file in the session's scratchpad while you work, and write the commit
   message from them.
2. **Is it how to do one task?** It's a skill.
3. **Is it a record of something tried and measured?** It's a new research doc.
4. **Is it a plan for how to build something,** such as the order to build the parts in? It's a
   blueprint.
5. **Is it a quirk of an outside service,** such as an API that returns an empty list where you'd
   expect an error? It's a comment on the code that handles it, not a doc.
6. **Does a type, a lint rule or a setting already enforce it, and is breaking it a quick fix?**
   A file naming rule is one: when the check fails, you rename the file. The check is its
   documentation, so it isn't written in a doc. If its reason isn't obvious, a comment at the check
   gives it.
7. **Would a user notice if it changed?** It's a functional requirement (`FR`), in the user's
   terms. A user uses the app through its own screens, as it's meant to be used. What stops someone
   who tampers with the app, such as by changing what their browser sends, isn't something a user
   sees. It's a technical requirement. See "One item for each fact" in
   [references/specs.md](references/specs.md) for how the two cite each other.
8. **Is it something the system must achieve that a user wouldn't see,** with no implementation
   in it? It's a technical requirement (`TR`). For example, "backups meet a set recovery point".
   Test it by imagining a redesign: if the redesign would still have to meet it, it's a
   requirement.
9. **Otherwise it's a decision:** how the system meets its requirements. Then:
   - **Not made yet?** It's an issue, such as a spike. Name it in your report, so whoever can
     open issues adds it. **Rejected?** It goes nowhere. Name it in a code comment only if an
     agent would likely change the code back to it.
   - **Is there one place in the code that every case of it goes through, now and in the future?**
     Then it's a comment in that place. If new code could follow or break it without touching that
     place, it goes in the technical spec. "Every database write runs in a transaction" is a
     comment on the one function every write goes through. "Services never call each other" goes
     in the spec, since a new service could call another without touching any shared place.
   - **If a check also enforces it,** the check's comment cites the decision's ID. "Services never
     call each other" stays in the spec even when lint enforces it, since breaking it can mean
     redesigning a change, not a quick fix.

**Is the code not written yet?** When a fact's home is in code that doesn't exist yet, such as a
code comment, a check, a setting or a data file the code reads, the fact goes in a blueprint until
the code is written. The blueprint's retirement steps then move it to its home. Requirements, and
decisions the technical spec holds, go in the specs even before any code exists.

**Not settled by the source?** When you'd have to choose part of a rule yourself, because the
source leaves it open, write no rule for that part. Don't copy the source's vague wording into the
doc either. Raise it as a question in your report: quote the source text, say what's unclear, and
suggest an answer. The task says what happens to the question next. Still write the parts the
source does settle. For example, notes say the shop emails a customer when their order ships,
"and again if it's running late", and never say when an order counts as late. Write the rule for
the shipping email, and ask when an order is late. A guess written as a rule looks settled to every later
reader, and nothing in the doc can mark it as a guess.

When you're sorting a long passage that mixes several kinds of text, read
[references/worked-examples.md](references/worked-examples.md). It sorts real passages with these
questions.

## How to write any doc

For every sentence, in any doc:

- **Would a first-time reader do anything differently if it were gone?** If not, cut it.
- **Write the present only.** No dates, issue numbers, session names, "was X, now Y", or "the new
  check". Turn an incident into a general scenario, with no detail that only one session had. The
  evidence stays. The history goes.
- **Make each section stand on its own.** The reader may not have read the section before it.
- **Point, don't restate.** Cite another item's ID instead of repeating what it says.

When the questions in "Which doc a fact goes in" make the fact's home a code comment, follow the
project's guidance for writing code comments.

### Names

- **One name for each thing.** Before naming a part of the app, a step or a state, search the docs
  for what they already call it, and use that exact name. A new name gets one home: a term in the
  Terms section, or the item that introduces it. When names come as a set, such as the steps of a
  process, list every name in that home. Never give a rule for making names, such as "each step is
  named for what happens in it".
- **One meaning for each term.** A word defined in Terms means only that, everywhere in the docs.
  When another meaning is needed, use a different word. For example, if "order" is defined as a
  customer's purchase, write "sort", not "order", for how a list is arranged. This is about
  meaning, not spelling. A set phrase that no reader could take for the term is fine, such as "in
  order to".
- **A name says what kind of thing it is,** even when it's the only thing of its kind: "order
  status", not "status". A short name breaks when a second thing of that kind is added.
- **Never use a shared word alone, unless it's a term.** When two names share a word, such as
  "user account" and "admin account", always write the full name. "Account" alone could mean
  either. To use the bare word for every kind, as in "each account", define it as a term that says
  which kinds it covers: "Account. A user account or an admin account." The term lists the kinds.
  It doesn't say what the word means in general. Otherwise write the full names, or reword so the
  word isn't needed.
- **Cite where a word's meaning lives.** A word defined in a Terms section needs no citation. Any
  other word whose meaning lives in another item gets that item's ID or section ID the first time
  an item uses it. The test: could a reader of this item alone find what the word means?

### Citing IDs

To point to a group of items, cite the section ID. It means whatever the section holds now. To
point to specific items, list each ID. Never cite a range, such as "FR-12 to FR-18". A new item
placed among them gets the next free number, so a range can't say whether it's included.
