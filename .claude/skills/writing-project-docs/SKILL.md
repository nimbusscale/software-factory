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
write an item. The files below hold the rest. Before you start, read every file that applies to
your task. Most tasks need more than one.

- **Adding, changing, replacing or deleting an item or a section,** in a doc or a code comment,
  or changing code that a doc describes: read
  [references/changing-a-doc.md](references/changing-a-doc.md). It gives the steps in order.
- **Writing in a doc, or creating one:** read the file for that kind of doc. It says what the doc
  holds and keeps out, how it changes, and how to write any kind of item only that doc has. Every
  doc opens with one line saying what kind of doc it is, so a reader knows which of these apply.
  - Functional spec: [references/functional-spec.md](references/functional-spec.md)
  - Technical spec: [references/technical-spec.md](references/technical-spec.md)
  - Research doc: [references/research-doc.md](references/research-doc.md)
  - Blueprint: [references/blueprint.md](references/blueprint.md)
  - Skill: [references/skill.md](references/skill.md)
  - CLAUDE.md: [references/claude-md.md](references/claude-md.md)
- **Checking a change,** your own before you count the work as done, or someone else's: read
  [references/reviewing.md](references/reviewing.md) and do every check in it.

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
the PR that you created it.

## Which doc a fact goes in

CLAUDE.md's table gives the short version. These questions are the long version. Ask them in this
order, and stop at the first yes.

1. **Is it about the past or the work in progress?** When something was decided, by whom, what
   was tried in a session, status, open items. It goes in the commit, the PR or an issue, never a
   doc. Keep notes in a file in the session's scratchpad while you work, and write the commit
   message from them.
2. **Is it how to do one task?** It's a skill.
3. **Is it a record of something tried and measured?** It's a new research doc.
4. **Is it something to build from before the code exists,** such as an implementation plan for a
   part of the system that isn't built yet? It's a blueprint.
5. **Is it a quirk of an outside service,** such as an API that returns an empty list where you'd
   expect an error? It's a comment on the code that handles it, not a doc.
6. **Does a type, a lint rule or a setting already enforce it, and is breaking it a quick fix?**
   A file naming rule is one: when the check fails, you rename the file. The check is its
   documentation, so it isn't written in a doc. If its reason isn't obvious, a comment at the check
   gives it.
7. **Would a user notice if it changed?** It's a functional requirement (`FR`), in the user's
   terms.
8. **Is it something the system must achieve that a user wouldn't see,** with no implementation
   in it? It's a technical requirement (`TR`). For example, "backups meet a set recovery point".
   Test it by imagining a redesign: if the redesign would still have to meet it, it's a
   requirement.
9. **Otherwise it's a decision:** how the system meets its requirements. Then:
   - **Not made yet?** It's an issue, such as a spike. **Rejected?** It goes nowhere. Name it in a
     code comment only if an agent would likely change the code back to it.
   - **Is there one place in the code that every case of it goes through, now and in the future?**
     Then it's a comment in that place. If new code could follow or break it without touching that
     place, it goes in the technical spec. "Every database write runs in a transaction" is a
     comment on the one function every write goes through. "Services never call each other" goes
     in the spec, since a new service could call another without touching any shared place.
   - **If a check also enforces it,** the check's comment cites the decision's ID. "Services never
     call each other" stays in the spec even when lint enforces it, since breaking it can mean
     redesigning a change, not a quick fix.

When you're sorting a long passage that mixes several kinds of text, read
[references/worked-examples.md](references/worked-examples.md). It sorts real passages with these
questions.

## How to write an item

For every sentence, in any doc:

- **Would a first-time reader do anything differently if it were gone?** If not, cut it.
- **Write the present only.** No dates, issue numbers, session names, "was X, now Y", or "the new
  check". Turn an incident into a general scenario, with no detail that only one session had. The
  evidence stays. The history goes.
- **Make each section stand on its own.** The reader may not have read the section before it.
- **Point, don't restate.** Cite another item's ID instead of repeating what it says.

When the questions in "Which doc a fact goes in" made the fact's home a code comment, the
`code-comments` skill says how to write it.

### Kinds of item

| Kind | Prefix | Doc | Form | Why line |
|---|---|---|---|---|
| Functional requirement | `FR` | Functional spec | GEARS | When the reason isn't clear from the rule itself |
| Technical requirement | `TR` | Technical spec | GEARS | When the reason isn't clear from the rule itself |
| Architecture decision | `AD` | Technical spec | One line of prose | Always |
| Design decision | `TD` | Technical spec | One line of prose | Always |

A requirement says what the system must achieve. A decision says how the system meets its
requirements, and why this way:

| Requirement | A decision that meets it |
|---|---|
| When data enters the program, the data shall be checked against a defined schema, with no extra keys. | Outside data is parsed with a schema library where it enters the program. |
| The services shall each be usable on their own. | Services never call each other. Code two services need goes in a shared module each is given. |

How to write a decision, and whether it's an `AD` or a `TD`, is in
[references/technical-spec.md](references/technical-spec.md).

### Requirements: GEARS

Every requirement uses this pattern. Every part but the last is optional:

> [Where \<fixed precondition\>] [While \<state at run time\>] [When \<trigger\>] The \<subject\>
> shall \<behavior\>.

- Where, While and When each appear at most once, in that order.
- The requirement starts with Where, While, When, or The.
- One behavior per requirement, so exactly one "shall". Two behaviors are two requirements.
- One trigger per requirement. A paragraph with several triggers becomes several requirements.
- The subject is a part of the system, or the code or data the rule is about. A plural subject
  keeps the "The" form: "The services shall each be usable on their own."
- State the condition a requirement depends on in its Where or While, even when it's always true
  today. A requirement written when a value was always empty breaks the day that value gets a
  default, unless "while it's empty" is in the requirement.

> **FR-12.** While the user hasn't set a time zone, the app shall show times in the time zone of
> the user's browser.

> **FR-30.** Where the account is a team account, the app shall ask an admin to approve each new
> member.

> **FR-41.** When a user deletes their account, the app shall keep their order history for seven
> years.
>
> *Why:* tax law requires order records for seven years.

### Lines under an item

- **Why:**
  - On a requirement, it works like a code comment: the reason behind the rule. Add one only when
    the reason isn't clear from the rule itself, and knowing it would change how someone applies or
    changes the rule. FR-41 needs one, since without it an agent might shorten the period to save
    storage. FR-12 doesn't, since its reason is clear from the rule.
  - A Why never states a fact about the rest of the system today, such as "no check uses this yet".
    That kind of fact goes stale when other items change. A condition goes in the Where or While.
- **Scenario:** Given, when, then. Add one under each behavior requirement in the functional spec,
  since they become evaluation cases. Elsewhere, add one only for a case a reader would get wrong.
- **Accepted gap:** a gap the item knowingly leaves, and the reason it's accepted. Without the
  reason, a reviewer can't judge whether the gap still fits.

### IDs

- **Item IDs** are a prefix and a plain number, such as `FR-42`, `TR-7`, `AD-2` or `TD-3`. The
  number says nothing about where the item sits, so it never goes stale when the item moves. Don't
  put a topic in an ID, such as `TD-CS-4`. It goes wrong the day the item moves to another
  section.
- **Section IDs** have a different shape, so they can't be mistaken for item IDs: `F-SEC-3` in the
  functional spec and `T-SEC-3` in the technical spec. They go in the heading:
  `## T-SEC-4. Outside services`.
- **A new ID** is one more than the highest number with that prefix in the doc:

  ```bash
  grep -oE '\bFR-[0-9]+' docs/functional-spec.md | grep -oE '[0-9]+$' | sort -n | tail -1
  ```

  An ID that was retired and deleted can come back this way. That's accepted, since a retired ID
  shouldn't be cited anywhere.
- **Citing:** to point to a group of items, cite the section ID. It means whatever the section
  holds now. To point to specific items, list each ID. Never cite a range, such as "FR-12 to
  FR-18". A new item placed among them gets the next free number, so a range can't say whether
  it's included.
