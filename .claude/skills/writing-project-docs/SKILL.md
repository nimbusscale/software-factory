---
name: writing-project-docs
description: How to write, change and review a project's docs (functional spec, technical spec, skills, research docs, blueprints) and decide what goes in a doc, a code comment, a check, or an issue instead. Use this whenever you're about to add a requirement, a decision or a reason to any doc or code comment, change one, create a new doc, or review a PR that touches docs, even if the task only says "update the spec", "write down why", "document this", or is a code change that makes a doc out of step.
---

# Project docs

Most readers of these docs are agents. They list a doc's headings, read one section, and act on
it. So every item has to be findable by its heading, make sense on its own, and say exactly what
it means. Every fact has one home, and other places point to it by ID. A second copy drifts, and
an agent can't tell which copy is right.

Work through the steps in order. Each one depends on the one before. The last section, "What each
doc holds", says what goes in each kind of doc and what stays out.

## 1. Find the docs

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

## 2. Check whether it's already written down

Before adding anything, search for it. Grep the docs for its key terms, list the headings of the
doc it would go in, and read the sections that look close. Also grep the code for comments on it.

If it's already there, you're changing, replacing or deleting an item, not adding one. Go to
step 4. If something close is there, decide whether yours is the same item said better, or a
different one.

## 3. Decide what kind of fact it is

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
   - **Does it shape the whole system, so a change would touch most of it?** It's an architecture
     decision (`AD`), such as "TypeScript for the whole app". Otherwise it's a design decision
     (`TD`), such as which library checks outside data.
   - **If a check also enforces it,** the check's comment cites the decision's ID. "Services never
     call each other" stays in the spec even when lint enforces it, since breaking it can mean
     redesigning a change, not a quick fix.

When you're sorting a long passage that mixes several kinds of text, read
`references/worked-examples.md`. It sorts real passages with these questions.

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

For every sentence, in any doc:

- **Would a first-time reader do anything differently if it were gone?** If not, cut it.
- **Write the present only.** No dates, issue numbers, session names, "was X, now Y", or "the new
  check". Turn an incident into a general scenario, with no detail that only one session had. The
  evidence stays. The history goes.
- **Make each section stand on its own.** The reader may not have read the section before it.
- **Point, don't restate.** Cite another item's ID instead of repeating what it says.

When step 3 made the fact's home a code comment, the `code-comments` skill says how to write it.

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

A decision can cite the requirement it meets, but it doesn't have to. There's no full map from
every decision to a requirement.

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

### Decisions

A decision is a one-line statement of the choice, in prose, and always has a Why.

> **AD-1.** TypeScript for the whole app.
>
> *Why:* the back end and the UI share one definition of the data model. In two languages, every
> field change would be made twice.

- Use `AD` when the decision shapes the whole system, so a change would touch most of it, such as
  the language, the agent framework or the database. Use `TD` otherwise.
- A line that makes two choices is two decisions. "TypeScript, with React for the UI" is two.

### Lines under an item

- **Why:**
  - On a requirement, it works like a code comment: the reason behind the rule. Add one only when
    the reason isn't clear from the rule itself, and knowing it would change how someone applies or
    changes the rule. FR-41 needs one, since without it an agent might shorten the period to save
    storage. FR-12 doesn't, since its reason is clear from the rule.
  - On a decision, it says why this option was chosen. Every decision has one.
  - A Why never states a fact about the rest of the system today, such as "no check uses this yet".
    That kind of fact goes stale when other items change. A condition goes in the Where or While.
- **Scenario:** Given, when, then. Add one under each behavior requirement in the functional spec,
  since they become evaluation cases. Elsewhere, add one only for a case a reader would get wrong.
- **Accepted gap:** a gap the item knowingly leaves, and the reason it's accepted. Without the
  reason, a reviewer can't judge whether the gap still fits.
- **Examples:** a list of cases, for decisions about how code is written, where a list helps more
  than a scenario.

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

When you change a doc, or change code a doc describes, do these checks before you count the work
as done. When you review someone else's change, do them on that change.

**Run the script.** From the repo root, run this skill's `scripts/check-docs.sh` with the docs
folder and the branch the change will merge into, such as
`bash <this skill's folder>/scripts/check-docs.sh docs main`. It prints one line per thing it
flags. A `RULE` line is a broken rule. A `SIGNAL` line is only something to look at. For each
`SIGNAL` line, look at the line and decide. Fix it if it's a real problem, and leave it if it
isn't. How a reviewer reports what it found is up to the project's workflow. It checks:

- **History,** as a signal: dates, issue and PR numbers, marker words (`settled`, `decided`,
  `drafted`, `assumption`, `for now`, `to come`, `in progress`), and words about the doc's past
  (`was` with `now`, `no longer`, `the new`, `used to`). Each can also be a real use, such as "no
  longer" in a requirement's While. It looks only at lines the change added, so a line kept on
  purpose isn't flagged again. Code, scenarios, research docs and blueprints are left out.
- **References:** every doc link, section ID and item ID cited in the docs or the code resolves.
  IDs are unique within a doc, and each prefix is in its own doc. No ID range is cited. The
  functional spec has no links out. No research doc links to another doc, and no other doc links
  to a research doc or a blueprint. As a signal only, it lists requirement IDs that nothing cites, since they may
  be unbuilt or untested. It doesn't look in open issues. Step 7 covers those.
- **Item shape:** each requirement follows GEARS, with one "shall", and has an ID. Each decision
  has a Why line right after it.
- **Copies,** as a signal: runs of eight or more words that a doc shares with a source file, such
  as a prompt, or with another doc.
- **Size,** as a signal: a doc near the Read tool's 25,000-token limit, since past that an agent
  can't read it whole in one call.

**Then check by reading:**

- **Nothing was dropped.** Compare each rewritten paragraph, old against new. `git diff
  --word-diff` on the doc shows them side by side. Every rule, condition, reason and example is
  still there, or the PR says it was cut on purpose.
- **The rewrite stayed in scope.** It touches only the paragraphs the task needed. A rewrite that
  spreads further goes in a separate change.
- **No history got in.** The script catches fixed patterns. Look for what it can't, such as "the
  check now runs first", and rewrite it as the present.
- **Every new item is in the right home,** by step 3, and every other step in this skill holds.

A doc that's wrong or out of step with the code is a fix in the PR, not a review note.

## What each doc holds

Step 3 decides which doc a fact goes in. This section says what else each doc holds and keeps out,
and how it changes. Every doc opens with one line saying what kind of doc it is, so a reader knows
which of these apply.

### Functional spec

Read by anyone changing what the app should do, and anyone writing evaluations. Kept current, and
changed in the same PR as the code or prompt change.

- **Also holds** the limits that always hold, each with its reason, such as "US only, because the
  payment provider only works there". It defines the terms a user would recognize, once each.
- **Keeps out** the prompt's or the code's level of detail. A requirement says what the user gets,
  not how a prompt words it. It also keeps out what's in the current release, which is a roadmap.
- **Never links out.** Prompts, code and other docs point to its IDs.

### Technical spec

Read by every implementer and reviewer, each reading the sections their task needs. Kept current,
and changed in the same PR as the code that changes one of its items. Split it only when different
tasks read different parts of it.

- **Technical requirements are rare.** Most rules turn out to be functional requirements or
  decisions.
- **Decisions about a whole kind of part** go here, such as "every endpoint returns errors in one
  shape".
- **A code standards section** holds the decisions about how all code is written. For example, a
  fix for a bug comes with a test that fails without the fix. Each outside service quirk the code
  depends on has a test with a saved response that shows it. Patterns for how code is shaped go
  here too, each with the reason that stops a wrong change.
- **An outside services section** holds choices about a service that span files or have no code
  to attach to, such as a monthly spending limit.
- **Pointers,** such as "settings are in `settings.json`", and where commands are defined, plus
  the one command that says work is done. It also defines the terms a user wouldn't recognize.
- **Keeps out** process, statuses and merge rules. Those are in the workflow's code and its role
  prompts.

### Skills

Read by only the agent doing that task. Kept current, and changed when the task's steps change.
Skills for one project live in that project.

- **One task per skill,** such as running an evaluation, writing an issue, or restoring a backup.
- **Numbered steps,** each with its reason in the step.
- **Facts about the outside tools the task drives,** such as an observability tool's API or a
  CLI's flags, each with the version it was checked on.
- **Default paths,** for when CLAUDE.md's doc map doesn't name one.
- **Keeps out** facts about how the system works. Cite their one home. If a sentence came out and
  the steps would be done the same way, cut it. Rules other tasks also need go in CLAUDE.md or the
  technical spec.
- **Keeps out** how to run a script whose top comment already says it. Give just the command.
- **Keeps out** paths relative to the skill's own folder, for anything outside the skill.

### Research docs

Read by only agents told to read them. Frozen once written. A new finding goes in a new research
doc.

- **Holds** a record of what was tried and measured, and what was found. Unlike every other doc,
  history is its point. It opens with its date and a line saying it's a record from that date and
  isn't kept up to date.
- **Keeps out** status lines and open items. Those go in issues.
- **No links either way.** It doesn't link to the rules its findings fed, since keeping those
  current would mean editing it. Other docs don't link to it. They state the reason themselves,
  such as a measured size.

### Blueprints

Read by the agents building the code it describes. It holds whatever is useful to build from
before the code exists, and nothing is ruled out. It can link to other docs, but other docs don't
link to it, since it's archived once the code is built. It's edited freely until then. When it's
retired, the issue that builds the code lists these steps in its "Done when":

1. Move items that new code elsewhere could break into the technical spec, sorted by step 3.
2. Check that each rule about one object is a code comment or a test.
3. Turn rules a check can enforce into checks, such as a lint rule for imports.
4. Archive the doc, frozen, with its date and a line saying it isn't kept up to date.

### CLAUDE.md

Read by every agent, every session. It changes only with the owner's approval, so propose changes
rather than making them.

It holds the rules every agent needs every time, the doc map, the table of where each kind of fact
goes, which wins when a doc and the code disagree, and where history goes. Every line must pass the
first-time reader test, since every agent reads every word.
