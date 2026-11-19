---
name: writing-project-docs
description: Writes, changes and reviews a project's functional spec, technical spec and blueprints, and decides whether a fact goes in one of them, a code comment or a check. Use when adding, changing or removing a requirement, a decision or a reason in a spec, a blueprint or a code comment, creating a spec or a blueprint, or reviewing a change that touches them, even if the task only says "update the spec", "write down why" or "document this", or is a code change that makes a spec out of step.
disable-model-invocation: true
---

# Writing project docs

The functional spec, the technical spec and blueprints are the input an agent turns into code.
Most of their readers are agents. They list a doc's headings, read one section, and act on it. So
every item has to be findable by its heading, make sense on its own, and say exactly what it
means. Every fact has one home, and other places point to it by ID. A second copy drifts, and an
agent can't tell which copy is right.

## What to read for your task

This file holds what every task needs: where the docs are, which doc a fact goes in, and how to
write any doc. The files below hold the rest. Before you start, read every file that applies to
your task. Most tasks need more than one.

- **Adding, changing, replacing or deleting an item or a section,** in a doc or a code comment,
  or changing code that a doc describes: read
  [references/changing-a-doc.md](references/changing-a-doc.md). It says what must hold when
  you're done.
- **Writing in a doc, creating one, or checking a change to one:** read the file for that kind of
  doc. It says what the doc holds and keeps out, how it changes, and how to write any kind of item
  only that doc has. Every doc opens with one line saying what kind of doc it is, so a reader knows
  which of these apply.
  - Functional spec or technical spec: [references/specs.md](references/specs.md). It also says
    how to write each kind of item, the Terms section and IDs.
  - Blueprint: [references/blueprint.md](references/blueprint.md)
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
| Blueprints | `docs/blueprints/` |

If a spec isn't at its default, search for its section IDs. They only appear in its own headings,
so they find the right file even though other docs cite its item IDs:

```bash
grep -rlE '^#+ F-SEC-[0-9]+' --include='*.md' .   # functional spec
grep -rlE '^#+ T-SEC-[0-9]+' --include='*.md' .   # technical spec
```

If the blueprints folder doesn't exist, create it in the same folder as the specs. If a
doc doesn't exist yet, create it at its default path from the template in `assets/`, and say in
your report that you created it.

## Which doc a fact goes in

Ask these questions in order, and stop at the first yes.

1. **Is it about the past or the work in progress?** When something was decided, by whom, what
   was tried in a session, status. It goes in the commit message, never a doc. Keep notes in a
   file in the session's scratchpad while you work, and write the commit message from them. Name
   any work left to do in your report.
2. **Is it about something other than what the app does and how it's built?** For example, how
   to do one task, a record of something tried and measured, or who the project is for. It
   doesn't go in a spec or a blueprint. Name it in your report, with where it likely belongs,
   such as a skill, a research doc or a README. The task says what happens to it next.
3. **Is it a plan for how to build something,** such as the order to build the parts in? It's a
   blueprint.
4. **Is it a quirk of an outside service,** such as an API that returns an empty list where you'd
   expect an error? It's a comment on the code that handles it, not a doc.
5. **Does a type, a lint rule or a setting already enforce it, and is breaking it a quick fix?**
   A file naming rule is one: when the check fails, you rename the file. The check is its
   documentation, so it isn't written in a doc. If its reason isn't obvious, a comment at the check
   gives it.
6. **Would a user notice if it changed?** It's a functional requirement (`FR`), in the user's
   terms. A user uses the app through its own screens, as it's meant to be used. What stops someone
   who tampers with the app, such as by changing what their browser sends, isn't something a user
   sees. It's a technical requirement. See "One item for each fact" in
   [references/specs.md](references/specs.md) for how the two cite each other.
7. **Is it something the system must achieve that a user wouldn't see?** It's a technical
   requirement (`TR`), such as "backups meet a set recovery point". It may name a part an
   architecture decision created. For example, an architecture decision picks an outside service
   to sign users in, and a `TR` says the user IDs the app stores are its own, never change and are
   never reused, whatever IDs that service gives. Test it by asking whether it leaves the how open.
   If several ways of building it could each meet it, it's a requirement. If it picks one of those
   ways, it's a decision.
8. **Otherwise it's a decision about how the system is built:** an architecture decision, a design
   decision or a code standard. "Kinds of item" in [references/specs.md](references/specs.md) says
   which. Then:
   - **Is there no other option?** A decision picks one way out of several. If the only reason
     anyone can give for it is that the rules or the domain work that way, nobody chose it, so
     it isn't a decision. Two kinds come up most. One says what a type holds, when the rules
     leave it nothing else to hold, such as a playing card that has a suit and a rank. The other
     follows from how a term or a rule defines something, such as that e4 and f5 lie on one
     diagonal, when a chess board's squares are named by a column letter and a row number.
     Its home is the code: the type, or the function that works it out. Until that code
     exists, it goes in a blueprint.
   - **Not made yet?** It goes in no doc. Name it in your report as a decision still to make, such
     as one that needs a spike to settle. **Rejected?** It goes nowhere. Name it in a code comment
     only if an agent would likely change the code back to it.
   - **Is there one place in the code that every case of it goes through, now and in the future?**
     Then it's a comment in that place. If new code could follow or break it without touching that
     place, it goes in the technical spec. "Every database write runs in a transaction" is a
     comment on the one function every write goes through. "Services never call each other" goes
     in the spec, since a new service could call another without touching any shared place.
   - **If a check also enforces it,** the check's comment cites the decision's ID. "Services never
     call each other" stays in the spec even when lint enforces it, since breaking it can mean
     redesigning a change, not a quick fix.

**Is its home a code comment?** These questions decide when a fact goes in a comment instead of a
spec. The project's guidance for code comments, such as a code-comments skill, says how to write
the comment. It may also find a better home in the code, such as a clearer name or a type. Either
way, the fact stays out of the specs.

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

Words such as "may" and "could" often leave a part open. When they say what the system might do,
or what the people building it might choose, they name options, not a decision. Choosing among them
is a decision not made yet, so raise it as a question, and don't write the "may" into the doc, or
the same option in other words, such as "can". The same goes for a "such as" that names a choice
still to make, as in "a database such as PostgreSQL". Still write everything the source says that
holds whichever option is chosen, even when it's in the same sentence as the option. For example,
notes say a phone app shows a customer their past orders, keeps no other customer data, and "may
keep a copy of the orders on the phone so it works offline". Write the rules for showing past
orders and keeping no other data, since they hold either way, and ask whether the app keeps a copy.
When you reword a sentence that holds either way, check that your wording still does. "Keeps no
other customer data" holds whether or not the app keeps a copy of the orders. "Keeps only the
orders on the phone" doesn't, since it says the app keeps them there. A sentence that sounds
settled can still depend on the option. If it only makes sense when one option is chosen, it's part
of the same question: leave it out too, and ask about the two together. If the same notes say the
order list "syncs to the phone", that only makes sense if the app keeps a copy, so it goes in the
question. Two uses of these words do settle something. A "may" that says what a person is allowed
to do is a rule: "a member may cancel a booking before it starts" means the app lets them. A "such
as" that gives an example of a rule is an example, not an option.

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

### Names

- **One name for each thing.** Before naming a part of the app, a step or a state, search the docs
  for what they already call it, and use that exact name. A new name gets one home: a term in the
  Terms section, or the item that introduces it. A part an architecture decision creates, such as
  a worker, always gets a term, since other items name it without citing the decision. When names
  come as a set, such as the steps of a process, list every name in that home. Never give a rule
  for making names, such as "each step is named for what happens in it".
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
