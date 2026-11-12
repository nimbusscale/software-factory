# Docs for agent-built projects: findings from road-trip-agent

2026-11-12. A record of the docs retrospective on road-trip-agent, as of this date. It isn't kept up
to date.

This file says what docs road-trip-agent had, how they grew and were used, what worked and what
didn't, and what the next project should do instead. The `project-docs` skill carries its
recommendations as a method for writing and reviewing docs. The `code-comments` skill does the same
for code comments.

## Takeaways

1. **Most of the doc text was written before the code, and then kept as a second copy of it.**
   Docs written to build from are worth it. Once the code exists, they're retired, not kept.
2. **Every fact gets one home, and other places point to it.** Prompts are code, so the prompt
   file is the home of prompt text. A doc says what the system should do, or why. It doesn't
   repeat what the code or prompt says.
3. **Agents follow a doc whether it's right or wrong.** A rule went wrong when a fact it depended
   on changed somewhere else, and nothing pointed back to the rule. So every rule states the
   condition it depends on.
4. **There was no clear plan for where history goes, so it went into the docs.** The next project
   needs one that keeps history out of the docs, so they don't grow with it. The one proposed here:
   notes in a scratchpad file while working, then the commit message.
5. **Agents read a doc by listing its headings and reading one section.** So each section has to
   stand on its own, and rules need IDs that other places can cite.
6. **Rules were free-form prose, so nothing could check how they were written.** One paragraph held
   several rules, conditions were left off, and reasons were often missing. Code has a style guide
   and lint, and docs had nothing like them. The next project writes rules in GEARS, a named sentence
   pattern for requirements. An agent can be told to follow it, and a script can check it.
   Decisions are one line and a reason.
7. **Corrections in chat became memories, which most agents never see.** In the next project, a
   correction that's a project rule becomes an offered doc change, and the owner decides.
8. **Code comments are where most reasons will live, and they had one line of guidance.** In a
   sample, under six in ten comments would be missed if they were gone. The rest repeated a name,
   gave only a section number, or said what a type could say. Comments had the docs' problems too:
   history, copies, and pointers that break. The next project gives comments their own skill.

## 1. Spec-driven development, as a frame

### What a spec is

A spec is a description of what software should do, written in plain language before the code, to
guide a coding agent. In the tools that use them, an agent usually drafts the spec and a person
approves it. A spec covers only the change being made.

Birgitta Böckeler separates specs from a **memory bank**: lasting rules and descriptions of the
product or codebase that apply to every session. Kiro calls this "steering", with `product.md`,
`tech.md` and `structure.md` by default. spec-kit calls it a "constitution". In Claude Code, it's
CLAUDE.md and the docs it points to.

### Three levels

Böckeler sorts spec-driven development by how long the spec lives:

| Level | What happens after the change | Source of truth |
|---|---|---|
| Spec-first | The spec isn't kept up. The next change gets a new spec. | The code |
| Spec-anchored | The spec is kept and changes with the feature | Both, kept in step |
| Spec-as-source | People edit only the spec, and the code is generated from it | The spec |

She judges Kiro and spec-kit spec-first in practice, though GitHub's messaging for spec-kit aims at
spec-anchored. Tessl aims for spec-anchored and is exploring spec-as-source.

The question that sorts these is: which file do you edit the next time something changes? A second
copy only causes trouble when the code also states the same thing in full. Reasons, constraints and
judgment rules aren't copies, because code can't hold them.

### Where road-trip-agent's docs fit, and where the next project's go

Road-trip-agent's functional spec, domain model and technical spec layered the way Kiro and
spec-kit do for each change: requirements, then design. But they were kept for the whole product.
So the set was spec-anchored, which Böckeler found most tools only aim for. The trouble was that
the design docs stayed spec-anchored after the code existed, when the code already said most of
what they said.

In the next project, the functional spec and the technical spec are spec-anchored. Blueprints, such
as a domain model, are spec-first: written to build from, then retired. So is an issue, which is
done when it closes. Prompt files are the source, and no doc repeats them. The `project-docs` skill
has the full list.

### The agent twist

For an agent app, the system prompt is code, written in English. A doc that describes the agent's
behavior is either the source of the prompt, or a second copy of it. English copies drift quietly,
since nothing fails when they disagree. Road-trip-agent's technical spec 5.2 was a second copy: 40%
of it was word for word in the prompt files.

The answer agreed here: the prompt file is the one home of the prompt's text. A view for people to
read can be made from it, like today's `*.view.md` files. The functional spec says what the agent
should do, in requirements with IDs. The prompt says how, and a comment next to a prompt rule can
cite the requirement it meets. So no doc copies the prompt, and no doc is the source it's built
from.

### Formats worth knowing

**EARS** (Easy Approach to Requirements Syntax) gives requirements five sentence patterns:
ubiquitous, event-driven, state-driven, optional feature, and unwanted behavior. Kiro writes its
acceptance criteria in EARS. An example of the event-driven pattern: "WHEN a user submits a form
with invalid data THE SYSTEM SHALL display validation errors next to the relevant fields." EARS fixes
how a requirement is phrased. It doesn't make the requirement run, so tests are still needed.

**GEARS** generalizes EARS for AI-assisted development, with one pattern instead of five:

> [Where \<fixed precondition\>] [While \<state at run time\>] [When \<trigger\>] The \<subject\>
> shall \<behavior\>.

Every part but the last is optional. The subject can be any part of the system, not only "the
system". It maps onto Given-When-Then: Where and While become Given, When stays When, and shall
becomes Then. So a requirement and its test share one shape. This is the form chosen in section 5.

**OpenSpec** is the closest thing found to a spec-anchored format that agents write and a tool can
check.

- `openspec/specs/` holds the lasting specs. `openspec/changes/` holds one folder per change in
  progress.
- A change writes its edits as deltas, under headings for added, changed, removed and renamed
  requirements.
- Requirements use SHALL, and each needs at least one scenario, written as WHEN/THEN bullets.
- `openspec validate` reports problems with the structure. Archiving a change merges its deltas
  into the main specs and moves the change folder into a dated archive.

Two of its ideas carry over without the tool. Rules have IDs, with their scenarios next to them.
And the main spec always reads as the present, which is what the "rewrite the whole paragraph" rule
in the `project-docs` skill does by hand. Its limits: a change's reasons stay with the change, so
lasting reasons need another home. Its archive keeps history in the repo, where the commit would
do. And requirements suit behavior, not method content such as "how a trip is planned".

### Critiques that apply to all of these

From Böckeler's trials:

- **One size doesn't fit all.** Kiro turned a small bug into 4 user stories with 16 acceptance
  criteria.
- **Reviewing them is a burden.** spec-kit produced long, repetitive Markdown she'd rather not
  review than the code.
- **They give a false sense of control.** Agents still ignored instructions, or followed some too
  eagerly, despite the specs.

The next project answers the first two by keeping the lasting docs small and putting one change's
detail in its issue. The third is why the docs are backed by script checks, tests and evaluations,
not trusted on their own.

## 2. What road-trip-agent had

### The docs

The docs in scope were `design/` (including the data source docs), DEVELOPMENT.md, the repo
CLAUDE.md, the simulated users README, `research/`, and the memory files. Today they hold 111,952
words. The biggest design docs:

| Doc | Words | What it was |
|---|---|---|
| Domain model | 26,667 | Objects, rules, and where each rule lives |
| Technical spec | 24,171 | Decisions, plus the coordinator's behavior rules |
| Tool design | 13,614 | Each tool's inputs, refusals and replies |
| Persistence design | 9,236 | How trips are stored and locked |
| DEVELOPMENT.md | 7,200 | Process, code standards, tests and commands |
| Systems | 5,097 | The server, accounts and outside services |

### How the evidence was gathered

- **Growth:** git history, for each doc's size over time, and a sample of commits sorted by what
  they added.
- **Use:** the local Claude Code transcripts, for which docs and sections agents opened, and how.
- **Results:** issues, PRs, CI review findings and research docs, for cases where a doc helped or
  hurt.

There are gaps. CI runs on GitHub leave no local transcripts, and the first two days of sessions
are missing. CLAUDE.md and memory load without a tool call, so the transcripts undercount them.

### Most of the text was written before the code

- The docs held 62,171 words by October 16, which is 56% of today's total. The first code commit was
  on October 15.
- The domain model was 23,000 words before any class existed. About 8,500 of those words were
  copies of what the code would hold. Its tables now match the code field for field, and each field
  is listed twice: once in the class diagram and once in a table.
- Agents opened design docs 1,219 times in the week of October 23. In the last week, they opened
  them 44 times.

### The same fact was written in more than one place

- 40% of technical spec 5.2, the coordinator's instructions, is word for word in the prompt files.
  41 of 54 commits that changed a prompt also changed the technical spec.
- The tool design doc copied a field list from the code 30 seconds after the code was committed.
- Rules sat in two or more docs, such as CLAUDE.md and DEVELOPMENT.md, or the domain model, the tool
  design and the technical spec.
- 36 CI findings said a design doc was wrong or out of step, on 23 PRs. That's about 30% of the
  labeled findings, the reviewer's biggest category. Most came from a PR that updated one copy and
  missed another. 14 of 24 inline notes of this kind got no reply, and some are still wrong today.

### Agents treat a doc as the authority, in both directions

- Some bugs could only be found with a doc rule. The code dropped Google's name for any place of
  type `premise`. Google gives that type to named buildings, such as hotels, so their cards showed
  no name. The code looked fine on its own. Only the doc rule "a card shows Google's name whenever
  Google has one" made it a bug.
- When the doc was wrong, the code followed it faithfully. For a stop after midnight, the doc said
  to show the next day's opening hours. Google lists late hours on the day a place opens, so a bar
  open Friday 11 AM to 2 AM looked closed at 1 AM Saturday. In another case, the weather doc called
  the share of days with any precipitation the "chance of rain". Snow counted too, so a mountain
  town in January showed rain almost every day.
- A fixer declined a real finding because the technical spec "accepts" the gap, with no reason
  given (section 3).
- 72 of 207 distinct CI findings name a doc, and 15 of the 30 "fix" findings do. Findings cite a
  section number and quote the sentence, since rules had no IDs.

### The docs only grew

- Every big cut was a move to another doc or file. DEVELOPMENT.md lost 367 words in 57 commits.
- Rules collected exceptions in place. The technical spec's bullet on broken feasibility rules went
  from 24 words to 448. One table cell in the tool design reached about 400 words. "Maximum trip
  length" appears 11 times in the domain model.
- Technical spec 5.2 went from 2,524 to 6,763 words in the week the workers were built.

### History went into the docs

- 204 lines across the docs carry a date, an issue number, or a Settled, Decided, Drafted or
  Assumption marker. By words that's small, 4% of the technical spec. Most are tails on rule
  sentences, like "Settled on 2026-10-30 in chat, for #230."
- DEVELOPMENT.md section 9 says that when a question is settled, "strike it out in the body, add
  when and how, and write the answer into the design doc". The "when and how" was meant for the
  issue, but the sentence is easy to read as putting it in the doc. Decisions comments say "written
  into" a doc 229 times.
- Later corrections all pushed detail out to issues, such as one run's results going in its issue.
  None became a rule about what a design doc may hold.

### How agents actually read docs

- Agents almost never used the Read tool on docs. Of 4,029 opens, 3,823 were shell commands: `grep
  -n '^#'` to list the headings (434 times), then `sed -n` to read a slice.
- Big docs were read in slices. The technical spec was read whole in 15 of 152 transcripts, and the
  domain model in 4 of 106. The domain model is over the Read tool's 25,000-token limit, so it
  can't be read whole in one call.
- Small docs were read whole. The design README was read whole in 141 of 146 transcripts.
- The README route mostly worked. 74 of 104 top-level sessions read it before another design doc.
- Agents edited docs mostly with Python string-replace scripts (578 of 878 edits), not the Edit
  tool.

### DEVELOPMENT.md mixed four kinds of text

- Build work opened it in 77 of 82 transcripts. Its most read sections were process: tracking work,
  rules for Claude Code, and branches and PRs.
- About 3,000 of its 7,200 words were manuals for single evaluations. Some repeated script header
  comments line for line.
- It kept one run's results as if they were standards: "There are 46, from 13 sessions."

### Research docs

- Research worked as a landing spot for a spike, before its result went into a design doc.
- It hurt where it kept status lines, or was linked from design docs as if current. 14 design doc
  links pointed into research, while CLAUDE.md said building never needs it.
- Most research files were opened by 1 to 4 transcripts after they were written.

### Memory

- Of 55 memory files, 34 are project rules. 24 of those are in no repo doc, and 10 copy one.
- Memory loads only in the owner's main sessions, so CI agents and subagents never saw those 24
  rules. One memory gives a different answer from the simulated users README.
- Only 16 are about how the owner likes to work, which is what memory is for. 5 are history or
  workflow state.

### Code comments

These counts cover `src/`, leaving out tests and fakes.

- There were 1,735 comment blocks, about 3,700 lines. 1,123 of the 2,239 top-level declarations,
  about half, had a comment right above them.
- The only rule was one line in DEVELOPMENT.md, there from the first day of code: "Comments say
  why, not what. The code says what it does. A comment explains a choice the code can't show, often
  by pointing to a design doc section." The review rubric said nothing about comments.
- A random sample of 60 blocks, each sorted by the most useful thing it carries:

  | Carries | Blocks |
  |---|---|
  | A reason, or a quirk of an outside service | 23 |
  | A contract a caller needs, such as an order or what null means | 22 |
  | Only what the name already says | 7 |
  | Only a pointer to a doc section | 4 |
  | Only an example of the text the code builds | 3 |
  | Only history | 1 |

  The 22 contract comments were then sorted again with a stricter test: imagine the comment gone,
  and ask what the next reader would get wrong. 12 pass, and nearly all of those pass because they
  hold a reason or an outside quirk, such as "A comment on a whole file has no line" in GitHub's
  data. The other 10 say what a type, a better name or a clear error could say, or copy a comment
  where the value is defined. The 23 reasons and quirks weren't sorted again. So at most 35 of the
  60, under six in ten, earn their place. One person sorted all of them, with no second labeler.
- The weak ones are mostly one short line above a type or function. 227 blocks are one sentence of
  12 words or fewer, right above a declaration, such as "One worker's recorded calls." above
  `interface WorkerRecord`.
- **Pointers:** 622 blocks cite a doc, mostly by section number. 154 cite the domain model, the kind
  of doc this retro calls a blueprint, which is archived once its code is built. Some comments are
  only a pointer, such as "Domain model section 2." above a list of weather labels.
- **History:** 134 blocks have an issue number, a date, or a word such as "settled" or "so far". For
  example: "Technical spec 6.1, settled on 2026-10-27 for #60."
- **Copies:** 351 blocks share a run of eight or more words with a design doc. 52 start with "Such
  as" and give an example of the text the code builds. At least one of those is word for word in a
  test.
- **Doc terms:** some comments only make sense with a doc open. "It needs no business rule, but
  stays are via service" uses a marker from the domain model's class diagram.
- **The good ones** give a reason or a quirk the code can't show, such as why Node needs its own
  SIGTERM handler in a container, or why a read limit of 40,000 characters stays under Claude
  Code's 25,000-token cutoff, with the date it was measured.

### The three main docs, compared

| Doc | Lines | Lines with history markers |
|---|---|---|
| Functional spec | 373 | 0 |
| Domain model | 1,356 | 1 |
| Technical spec | 544 | 51 |

**The functional spec held up best.** It states its boundary in its first line: functional behavior
only. It has acceptance scenarios, the most checkable text in the set, and no history. Its problems:

- Section 10.1 broke its boundary, covering the coordinator, trace IDs, Phoenix, and links that only
  work on one machine.
- Its five "Assumption" markers said to confirm them before development. Development happened, so
  the markers became workflow state.
- The technical spec named it 48 times and then restated it. The driving hours cell is a full
  paragraph, and technical spec 5.2 repeats all of it.
- Its 13 scenarios don't cover option cards, rejections, or most of the agent's judgment rules. S8 to
  S13 aren't covered by any trip file.

**The domain model had the strongest contract.** Its "How to read this" section set naming rules,
type notation and markers. Its "Left out on purpose" section said what isn't there and where it is.
Its reasons were its most valuable part. Its problem was being a second copy of the code (section 3).

**The technical spec decayed.** It mixed at least five kinds of text: decisions with reasons,
behavior rules for the model, restatements of code, incidents that justify a rule, and history.
Its rules had no IDs, so a finding could only point at a paragraph. Its opening said what it
covers, but not what stays out. It's where agent behavior lives, and each fix to the coordinator was
written down with its story, date and issue.

## 3. What went wrong, and what to do instead

### The design docs outlived their job

The domain model was worth writing before the code. Opus war-gamed sample trips against it, and
that found a lot to fix before any code existed. Keeping it as a reference afterward was the
mistake. Its field lists, types and signatures belong in the code, where an agent reads them more
easily than a prose copy. Nine of ten sampled rules in its prose were already code comments. The
second copy caused bugs rather than catching them. One rule change missed four stale copies of the
rule, in three docs. Another rule contradicted the doc's own worked example: it put breakfast near the start town
after a 5-hour drive away from it.

The same held for the technical spec, the tool design and the persistence design. Most of each
described how the code works, which the code shows once it exists.

What's worth keeping is what code can't say:

- Rules that span files, such as "services never call each other". That rule was only in the
  domain model, the doc being retired, so the retire step has to move it.
- Decisions and their reasons, such as "TypeScript for the whole app, since in two languages every
  field change would be made twice".
- Constraints from outside, such as a reason the read limit is safe.

Merged and trimmed, the five design docs would come to about 9,000 words, down from 78,785. Diagrams
of the code are useful, but they can be generated, so they aren't a reason to keep a doc.

So the next project calls a doc written to build from a **blueprint**, and retires it once the code
is built. The retire step is listed in the "Done when" of the issue that builds the code. The
`project-docs` skill lists it.

### Every fact needs one home

Most of the CI reviewer's doc findings came from a PR updating one copy of a fact and missing
another. The reviewer found the copies without any work aimed at that. The weak part was acting on
them: the review rubric made an out-of-step doc a note, not a fix. That was a corner cut on purpose,
for a short project.

The main fix is in how docs are written. Each fact gets one home, and other places point to it by
ID. CLAUDE.md holds a table saying which home each kind of fact has (section 4).

Some homes aren't docs:

- **Prompts and tool descriptions** are code. The prompt file holds the text.
- **Settings and config are documentation.** A rule a setting can enforce, such as "merge commits,
  never squash", is written as that setting, and nothing restates it. This project's lint config
  already bans disable comments and `@ts-expect-error`, so no doc needs to say it.
- **Quirks of an outside service**, such as hours past midnight being listed on the opening day,
  live in the code that handles them. A comment says why, in general terms. A test with a saved
  response, named after the quirk, keeps it handled. The late hours bug and the snow bug both had a
  saved response nearby. But the right case wasn't saved, or no test tied it to a rule.

### A rule went wrong when a fact it depended on changed

A driving hours rule said: when user memory holds the user's usual driving hours, set the trip
brief to them. It had no condition, because the brief's driving hours were always empty when the
rule was written. Later the brief could already hold a value, such as a one-off "only 4 hours this
time". Nothing pointed back to the rule, so it overwrote that value in every new session. The rule
was in the technical spec and the prompt, and both copies were wrong together.

The fix is in how rules are written:

- Every rule states the condition it depends on, even when it's always true today. "While the trip
  brief's driving hours are empty, when user memory holds the user's usual driving hours, the
  coordinator shall set the trip brief's driving hours to them."
- When a change alters a fact, the writer searches the docs for rules whose conditions mention it.

GEARS helps with the first part, since its Where and While slots make the writer ask "in what state
does this apply?" Nothing yet does the search for the writer.

An accepted gap needs its reason. A reviewer found that when a driving warning's text changed, the
reply left it out. The fixer declined the finding, because the technical spec said the code does
what the design asks. The fixer had only "accepted" to go on. With a reason, a reviewer can judge
whether the gap still fits it.

### The docs only grew

Size on its own doesn't hurt agents much. They read by headings and slices, so a big doc with clear
sections that stand alone costs them little. There's no hard size limit. The one real limit is the
Read tool's 25,000 tokens.

What hurt was how docs grew. A change appended an exception to the nearest bullet, so a rule ended
up with its reason, example and history in one long paragraph. The "Today's date" bullet in
technical spec 5.2 reached about 900 words, covering five kinds of text. So the writing rule is:
when a change adds to a paragraph, rewrite the whole paragraph so it reads as if written in one go.

That rule has two risks, and the guide checks both. A rewrite can drop something, so the writer
compares old and new side by side. And a rewrite can spread past the paragraphs the task needed, so
a script lists the changed paragraphs.

Docs are split by the task that reads them, not by length. The data source docs were the model: one
service, one kind of task, read whole most of the time.

### History needs somewhere else to go

The project had no clear plan for where history goes. Early on, the docs were the only place to
log things, since issues came later. A later rule meant to put "when and how" in the issue was easy
to read as putting it in the doc. And agents lean toward logging what they did.

A script can find a history marker, but it can't just delete the sentence. A tail often mixes the
rule, the evidence for it, and history such as session names, dates and issue numbers. The writer
keeps the evidence and drops the history by turning the incident into a general scenario. Scenarios
also make good evaluation cases.

The test for every sentence: would a first-time reader do anything differently if it were gone? If
not, cut it. That test works against history, and against copying.

Agents tend to log what they did as they go. This retro's own notes picked up a correction log,
even with the rules against it. We think this is a common habit of Claude agents. So the next
project directs it, not just bans it. While working, an agent keeps its history notes in a file in
the session's scratchpad, and writes the commit message from them. The commit is the ledger, and no
doc is. That directing it works better than banning it is a guess. It hasn't been tested.

Whatever the outlet, expect history to still get into docs, since the habit is common. So the
checks after a doc is written matter most. The script checks point at the fixed patterns, such as
dates, issue numbers and marker words, in the lines a change adds. Someone still judges each one,
since a pattern can't tell history from a real use. The doc review catches what a pattern can't
find at all, such as "the check now runs first" with no date or marker.

### Agents read sections, so references need IDs

Agents list a doc's headings fresh each time, then read a slice. So each section has to make sense
on its own. What has to stay stable is not the headings, but the references to them from other
docs, code comments, issues and review findings.

So there are two kinds of ID. Section IDs say "read this area". Rule IDs mark the statements a
reviewer would cite, and the rule's reason and scenario sit under it. A rule ID is a prefix and a
plain number, such as `FR-42`. A section ID has a different shape, such as `T-SEC-4`, so the two
can't be mixed up (section 5).

### DEVELOPMENT.md held four docs

Its 7,200 words were code standards (about 1,200), process (about 1,600, the most read), tests
(about 3,400, mostly manuals for single evaluations), and commands (about 840). Each has a different
home in the next project:

- Code standards become a section of the technical spec. Its items are design decisions like any
  other, and every implementer and reviewer reads that section.
- Manuals for one task become skills, which only the agent doing that task loads.
- Process moves into the workflow's code and each role's prompt.
- Commands are in `package.json` and the scripts.

### Research docs worked, with two changes

Research docs were useful, and agents read them only when told to. The next project keeps them,
with two changes. A research doc opens with its date and a line saying it isn't kept up to date, and
has no status lines or open items. And no links go in either direction. A design doc states the
reason itself, such as "a busy 14-day trip reads at about 34,500 tokens", rather than pointing to
research.

### Corrections became memories

When the owner corrected an agent in chat, the correction became a memory, not a doc change. So
rules sat where CI agents and subagents couldn't see them.

But turning every correction into a doc change has its own risk. A memory written right after a
correction tends to turn one incident into a general rule, or to collect unrelated rules. One bad
test became a rule against testing that a prompt lacks a string. So in the next project, when the
owner corrects something that is a project rule, the agent offers a change to the right doc or
skill, and the owner decides. The change has to pass the first-time reader test. Memory keeps only
how the owner likes to work, plus working notes for the main session.

### Comments had one line of guidance

The next project moves many reasons out of docs and into comments, next to the code they explain
(section 4). So comments need as much guidance as docs. Road-trip-agent had one line.

The line was right, but agents kept its second half and lost the first. "Often by pointing to a
design doc section" read as a shortcut: a short "what" with a section number on the end passed as
a "why". "The leg scout's own model and effort settings (technical spec section 10)" is one. It
names the two fields, and gives no reason.

Comments also had the docs' problems:

- Section numbers move when a doc is reorganized, and blueprints are archived. A pointer to either
  breaks, and nothing flags it.
- History got into comments the same way it got into docs, as tails on good sentences.
- An example of output in a comment is a copy of the test that checks it. When the format changes,
  the test is fixed and the comment goes stale.

One problem is new. A comment can repeat the code, which no doc did.

The `code-comments` skill sets the guidance:

- **The default is no comment.** One test decides it: imagine the comment gone, and ask what the
  next reader would get wrong. A better name, a smaller function, a type, an error with a clear
  name, or a test comes first.
- **What passes is nearly always a reason, a quirk of an outside service, or the ID of the item the
  code carries out.** Anything else has to pass the test on its own.
- **No "contract" kind.** A draft had one, for what a caller needs to know. Three examples of it
  failed the test when looked at closely. One was a rule about no repeats, which a set could hold.
  One was a copy of a field's comment, on a function that passes the value along. One described an
  error the API already handled. As a kind, it let an agent label a comment a contract and keep
  it.
- **No "guide" kind.** A draft had labels for the phases of a long function. A smaller function
  with a clear name does that better, since its name can't drift from what it does the way a label
  can. A label that matters usually matters for a reason, such as an order, and reasons are already
  allowed. None of the 60 sampled comments was one.
- **The same rules as docs.** No history, no copies, and IDs, not section numbers. Never a pointer
  to a blueprint or a research doc. A citation doesn't replace a reason that fits in a sentence.
- **Only what can be shown.** Each kind has its own source. A reason comes from where the choice
  was made, such as a spec item's Why, the task, or the owner. A quirk comes from the service's docs
  or a saved response. An ID comes from the spec. The code backs up only the parts of a claim that
  describe the code. The risk is highest when an agent comments code it didn't write, since it has
  no source and can easily write a reason that sounds right and isn't.
- **A measured number keeps its date.** That date is evidence, not history. A reader needs it to
  judge whether the number still holds.

## 4. The docs for the next project

The `project-docs` skill holds the list of docs, the contract for each one, and the method for
writing and reviewing them. This section keeps what the skill doesn't: the places that aren't docs,
why the contracts are a table in CLAUDE.md, and CLAUDE.md's own contract.

### Places that aren't docs

These places aren't docs, but each is the one home for facts that are easy to put in a doc by
mistake:

| Home | What it holds |
|---|---|
| Code and prompt files | What the code does. Tool descriptions and schemas. Prompt text. The handling of each outside service quirk the code depends on. |
| Code comments | The reason for one rule, next to it. The requirement ID it meets. The quirk that a piece of code handles, and why. |
| Tests with saved responses | A check that the code still handles each quirk, using a saved response that shows it. The test is named after the quirk. |
| Settings and config | Any rule a setting can enforce, such as "merge commits, never squash" |
| Issues and git | When and by whom something was decided. Status. Open items. |
| Memory | How the owner likes to work, and working notes for the main session |

A roadmap isn't one of the docs. Where it's kept is up to the project.

The `project-docs` skill decides whether a fact's home is a comment. The `code-comments` skill says
how to write it.

Rejected ideas go nowhere. If one is forgotten, it probably didn't matter. A code comment names one
only when an agent would likely change the code back to it.

### Why the contracts are a table in CLAUDE.md

CLAUDE.md holds the table of where each kind of fact goes, which is every doc's contract in short.
The skill's questions for sorting a fact are the long version. No doc repeats its contract at its
top. Agents read one section of a doc, so a contract at the top would often be missed. CLAUDE.md is
read whole every session, so an agent that adds a fact while coding sees the table too, not only an
agent that loaded the skill. Agents built on the Agent SDK must load project settings, or they get
no CLAUDE.md.

### CLAUDE.md

**What goes in:**

- Rules every agent needs every time: what the project is, how much care each kind of work gets,
  and exceptions to that, such as security.
- One line per doc saying when to read it.
- The map from each kind of doc to its path. Use the same kind names across projects, such as
  "functional spec" or "technical spec". Skills name the kind. A skill can also hold a default
  path, for when the map doesn't name one.
- The rule that every fact has one home. Other places point to it by ID, and never restate it.
- The table of where each kind of fact goes, such as "something a user would notice if it changed:
  the functional spec". This table is the contract for every doc kind. No doc repeats it at its top.
- Which one wins when a doc and the code disagree: the doc says what's intended. The agent fixes
  the code, or asks the owner to change the doc. It never changes the doc to match the code on its
  own.
- Where history goes: while working, notes go in a scratchpad file, and the commit message is
  written from them. No doc is a ledger.
- The rule on corrections: when the owner corrects something that is a project rule, the agent
  offers a change to the right doc or skill. The owner decides. The agent never applies it on its
  own, and never saves it as a memory.

**What stays out, and where it goes:**

- Rules for some roles only, such as how a reviewer posts comments: that role's prompt or skill.
- Process: the workflow's code and role prompts.
- Commands: `package.json` and the scripts.

**How it changes:** only with the owner's approval. Every agent reads every word, so each new line
must pass the first-time reader test: would an agent act differently if the line were gone?

**The table, as CLAUDE.md would hold it:**

| If the fact is ... | Its home |
|---|---|
| Something a user would notice if it changed | The functional spec |
| Something the system must achieve that a user wouldn't see, such as a backup recovery point | The technical spec, as a technical requirement |
| A choice that shapes the whole system, where a change would touch most of it | The technical spec, as an architecture decision |
| A choice that new code could follow or break without passing through one shared place in the code | The technical spec, as a design decision |
| A choice that every case of goes through one place in the code, or a reason for one piece of code | A comment in that place |
| A rule a type, a lint rule or a setting enforces, where breaking it is a quick fix, such as a file naming rule | That check, with a comment giving the reason if it isn't obvious. A decision a check enforces, where breaking it is costly, stays in the technical spec, and the check's comment cites its ID. |
| A quirk of an outside service | The code that handles it, with a comment explaining the quirk. A test with a saved response checks the handling. |
| How to do one task | A skill |
| What was tried and measured | A new research doc |
| When or by whom something was decided, status, open items | The commit, the PR, or an issue |
| A deferred decision | An issue |
| A rejected idea | Nowhere. Name it in a code comment only if an agent would likely change the code back to it. |

## 5. The language of each doc kind

### Forms

| Doc kind | Form | IDs | Why | Scenario |
|---|---|---|---|---|
| Functional spec requirements (`FR`) | GEARS | Yes | When the reason isn't clear from the rule itself, and knowing it would change how someone applies or changes the rule | On behavior rules. They become evaluation cases. |
| Technical requirements (`TR`) | GEARS | Yes | When the reason isn't clear from the rule itself, and knowing it would change how someone applies or changes the rule | Only for a case a reader would get wrong |
| Architecture decisions (`AD`) and design decisions (`TD`) | A one-line statement of the choice, in prose | Yes | Always | No. Decisions about how code is written can have examples. |
| Skills | Numbered steps, each with its reason | No | In the step | No |
| CLAUDE.md, research docs, blueprints | Plain prose | No | In the sentence | No |

### GEARS

The pattern, with every part but the last optional:

> [Where \<fixed precondition\>] [While \<state at run time\>] [When \<trigger\>] The \<subject\>
> shall \<behavior\>.

- Where, While and When each appear at most once, in that order.
- The rule starts with Where, While, When, or The.
- One behavior per rule: exactly one "shall". Two behaviors are two rules.
- One trigger per rule. A cell that holds several triggers becomes several rules.
- The subject is a part of the system, or the code or data the rule is about. A plural subject
  ("The services shall each be usable on their own") keeps the "The" form.

Example: "When data enters the program, the data shall be checked against a defined schema, with
no extra keys."

Why GEARS: it's clearer and less ambiguous than prose. Prose could match it, but there's no standard
way to write prose like that. GEARS is a named standard, so an agent can be told to write in it. Its
condition slots also put the condition a rule depends on at the front, where it's hard to leave out.

### IDs

- Every requirement and every decision gets an ID: a prefix for its kind and a plain number, such
  as `FR-42`, `TR-7`, `AD-2` or `TD-3`.
- Every section gets a section ID with a different shape, so it can't be mistaken for an item ID:
  `F-SEC-3` in the functional spec and `T-SEC-3` in the technical spec. It goes in the heading, such
  as "## T-SEC-4. Outside services".
- A plain number never goes stale when a rule moves. The section heading already says where a rule
  sits.
- A new ID is one more than the highest number with that prefix in the doc. A deleted ID can come
  back this way, which is accepted, since a retired ID shouldn't be cited anywhere.

### Why lines

- On a decision, a Why says why this option was chosen. Every decision has one.
- On a requirement, a Why works like a code comment: it gives the reason behind the rule. It's added
  only when the reason isn't clear from the rule itself, and knowing it would change how someone
  applies or changes the rule.
- A Why never states a fact about the rest of the system today, such as "no check uses this yet".
  That kind of fact goes stale when other rules change.
- A condition the rule depends on goes in its Where or While, not in its Why.
- A requirement that knowingly leaves a gap gets an "Accepted gap" line with the reason.

### Requirements and decisions in the technical spec

- A requirement says what the system must achieve, with no implementation in it. A redesign of the
  code would still have to meet it. A functional requirement is one a user would notice. A technical
  requirement is one a user wouldn't, such as "backups meet a set recovery point".
- A decision says how the system meets its requirements, and why this way. A decision can cite the
  requirement it meets, but there's no full map from every decision to a requirement.
- An architecture decision shapes the whole system, and changing it would touch most of it, such as
  "TypeScript for the whole app". A design decision could change without touching most of the
  system, such as "use Zod for outside data". The writer picks `AD` or `TD` when writing it.
- Where a decision lives: is there one place in the code that every case of it goes through, now
  and in the future? If yes, it's a comment there. If new code could follow or break it without
  touching that place, it stays in the technical spec. "Every write runs the same four steps" is a
  comment, since every write goes through one function. "Services never call each other" stays,
  since a new service could call another without touching any shared place.
- A decision stays in the technical spec even when lint enforces it. The lint rule's comment cites
  its ID.

### Skills and prose docs

- A skill says what to do, not how the system behaves, so it uses numbered steps, not GEARS. Nobody
  cites a skill step, so it has no IDs.
- A skill is held to the same bar as the other docs. It doesn't repeat a fact about how the system
  works. If a sentence came out and the steps would be done the same way, it's cut.
- CLAUDE.md is a short list of plain rules, read whole every time. Research docs and blueprints are
  frozen once written. None of them is cited by ID, so plain prose fits.

### What the rewrites showed

These forms came from rewriting six real passages, side by side:

- **The driving hours cell** in the functional spec, 175 words, became eight GEARS rules. Most of the
  gain came from splitting it into separate rules, each of which can be cited and tested on its
  own. GEARS also put the missing condition up front: "While the user hasn't said how long they like
  to drive, the planner shall not ask until the user can see a day's drive."
- **The "Today's date" bullet** in technical spec 5.2, about 900 words, had four rules in it. None
  turned out to be a technical requirement. One is a functional requirement, since a user would
  notice which date counts as today: "Where the trip has a start place, the planner shall treat
  today as the date in that place's time zone." Two are design decisions that stay in the technical
  spec, because new code could break them from anywhere. One, the UTC default, is a comment on the
  one function that picks the trip's time zone. The rest of the bullet had better homes: comments
  where the date line is built, the prompt file, a test with a saved example, commit messages, and
  the functional spec.
- **The decisions.** Only two of the six decisions worth keeping had a full reason written down.
  "Each agent sees only its own tools" had none. Neither did the rule "services never call each
  other". The Why line made each gap visible.
- **A decision carried out in one place in the code** reads better as a comment there. "The
  coordinator runs from a definition that lists its tools" became a comment on the code that starts
  it, saying why and citing the decision it carries out.

## 6. The writing guide

The writing guide became the `project-docs` skill. Its steps are the method. The reasons behind its
shape:

- **One skill for writing and review.** Most review checks are the skill's own rules, so a separate
  rubric would be a second copy that drifts. The writer needs the same checks before counting the
  work done. The skill holds rules, not the writer's reasons, so reading it doesn't bias a reviewer.
- **A full skill, not a short guide.** The first guide was short, and leaned on this file for its
  reasons and examples. A new project won't have this file, so the skill holds the whole method:
  the questions that sort a fact, the forms, each doc's contract, and worked examples.
- **Default paths.** The skill names a default path for each doc, and finds a spec by its section
  ID headings when it isn't there. The earlier rule was that only CLAUDE.md names paths. Defaults
  let the skill work in a project whose CLAUDE.md has no doc map yet.
- **It points to CLAUDE.md rather than repeating it:** the table of homes, which wins when a doc and
  the code disagree, and where history goes.
- **It decides where a fact lives, but not how to write a check or a test.** That's code work.
- **Comments get their own skill.** Comment guidance is needed on almost every code change.
  `project-docs` is meant for changes to requirements and decisions, and is too long to load for
  one comment. So `project-docs` decides whether a fact goes in a comment, and `code-comments` says
  how to write it. It took its shape from two outside skills (Sources). PostHog's gave the default
  of no comment, the one question that decides it, and the rule on measured numbers. abhinav's gave
  the two readers, a caller and a maintainer, a field's meaning going on the field, and the rule
  that a comment claims only what the code shows.

## 7. Checks a script can do

The checks are a script in the `project-docs` skill, and the skill's last step lists them. The
reasons behind their shape:

- **The script only reports.** Each line is a broken rule or a signal to look at. Whether a flag
  holds up a merge is up to the workflow, which isn't designed yet (section 9).
- **The history checks are signals, and look only at lines the change added.** A pattern can't
  tell history from a real use. "No longer" can be part of a requirement's While, and a date can be
  an example. Checking only added lines means a line kept on purpose is judged once and never
  flagged again. That avoids marking accepted exceptions in the doc. Such a marker would work like
  a lint disable comment: an agent under pressure to pass the check learns to add one.
- **The structure checks are rules, over every doc.** Undefined IDs, cited ranges, GEARS shape and
  broken links almost never misfire.
- **Research docs and blueprints are left out of the history checks,** and no other doc links to
  either. History is a research doc's point, and it's frozen. Nothing is ruled out of a blueprint
  while it's in use, and it's archived once its code is built.
- **No check for reused IDs.** A new ID is one more than the highest in the doc, so a retired,
  deleted ID can come back. A retired ID shouldn't be cited anywhere, so that's accepted, and no
  script has to read git history.
- **Copies are signals.** A shared run of eight words can be a quote on purpose.

Run over road-trip-agent's `design/` folder as a whole, the checks flagged 145 dates and 169 issue
or PR numbers. The technical spec shared 2,335 eight-word runs with one prompt file.

## 8. What changed from the earlier recommendations

An earlier notes file made recommendations before this retro. Here's where each one ended up.

| Earlier recommendation | Where it ended up |
|---|---|
| Decide each doc type's lifespan | Kept. Section 1 gives each doc its level. |
| Write a contract at the top of every doc | Changed. The contracts are a table in CLAUDE.md in short, and in full in the `project-docs` skill, since agents read one section, not the top. |
| Treat the domain model as spec-first | Kept, and made general as blueprints with a retire step. |
| Agent behavior rules as the prompt's source, or not at all | Settled. The prompt file is the home of the prompt. The functional spec owns what the agent does, and the prompt points to its IDs. |
| Give rules IDs and scenarios | Kept. IDs on every rule and decision. Scenarios on functional spec behavior rules, and elsewhere only where a reader would get a case wrong. |
| Turn incidents into scenarios | Kept, in the `project-docs` skill. |
| Keep history and workflow state out of docs | Kept, and given an outlet: scratchpad notes, then the commit message. |
| One source for each fact, across docs | Kept, as the table of homes. The functional spec never links out. |
| A script checks the domain model's tables against the code | Dropped. Blueprints are retired once the code exists, so there's nothing to check. |
| A script or reviewer checks behavior rules against the prompt | Dropped. Nothing restates the prompt. |
| A rubric reviewer for doc changes | Folded into the `project-docs` skill's last step, "Check the change". |
| Test each section by deleting it and rerunning a task with a fresh agent | Not taken up. Still a way to test whether a section earns its place. |

## 9. Open items

- **The full-scale test.** Joe decides whether to rewrite road-trip-agent's docs to these contracts,
  in new sessions using the `project-docs` skill, to test the approach with fresh context. The forms
  in section 5 were chosen by comparing rewrites side by side, without giving fresh agents each
  version. This test would stand in for that.
- **The development loop's design.** Three questions belong there:
  - where skills shared across projects live, and how the loop reaches a project's own skills and
    commands without bundling them into its agents. A single loop that fits every project may not
    exist.
  - what the workflow does with what the doc checks flag. The checks only output them for now.
  - whether to add a per-project review bar later. The loop starts with stock review skills.
- **Reasons as code comments, or in a doc.** Joe is reading up on this. From the transcripts: in 233
  of 272 edits to a `src/` file, the agent had read that file earlier in the session. About 60% of
  source reads saw the top of the file. So a comment right above a function is almost always in
  view. The data can't show whether an agent acted on what it saw.
- **Whether the comment skill cuts the weak comments.** Not tried yet. Sorting a sample of 60
  comments from the next project's code with the same test would show it, ideally with two
  labelers.
- **Python string-replace edits.** Agents made 578 of 878 doc edits with Python scripts rather than
  the Edit tool. Not discussed yet.
- **Whether the history outlet works.** Directing agents to log in a scratchpad file, rather than
  only banning history in docs, is a guess. Whether to test it with an evaluation is open.
- **What keeps a kept doc in step.** The skill's checks, the script and a scheduled
  doc curator each catch some drift. None has been tested yet.
- **How much agent-written doc change to allow without a person reading it.** On road-trip-agent,
  the technical spec grew once agents updated it freely. Whether the guide and checks hold without
  a person reading every doc change is unknown.
- **Which decisions deserve an ID.** It's a judgment call. So is whether a decision is architecture
  or design, though the writer makes that call once, when choosing `AD` or `TD`.
- **Issues and PRs.** What makes a good issue, the template, PR descriptions and decisions comments
  get their own analysis, tied to the loop design. The facts collected so far, from road-trip-agent's
  issues:
  - Issue #199 (296 words) worked with only "please do this issue". It had a one-line wait, a
    three-sentence Why, a Design list naming exact doc sections, no open questions, four Do items
    pointing at sections, and Done-when items a test can show. Its PR got no fix findings.
  - Length tracked how much new text the work needed, not quality. Issue #156 was 3,378 words, and
    right for a wording fix. 110 of 120 issues have a Design section pointing to doc sections.
  - Issue #199's PR still listed 8 decisions the implementer made, 6 of which went into a design
    doc. That's the decision reviewer's job in the new loop. Whether they should have been settled
    before the issue was written is the issue checker's job.
  - Two parts stay with this retro: the line between issues and docs, and issues citing section and
    item IDs. Section 3 covers both.
- **Two side ideas:** a regular pass to prune memory, like the doc curator but run in the main
  session. And size limits on code, which this retro has no data on.

## Sources

- [Understanding Spec-Driven Development: Kiro, spec-kit, and Tessl](https://www.martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html),
  Birgitta Böckeler, martinfowler.com
- [Kiro steering docs](https://kiro.dev/docs/steering/)
- [Kiro Specs Explained: EARS, Spec Mode, and the Trade-offs](https://codemyspec.com/blog/kiro-specs-explained)
  (written by a competing vendor)
- [Examine the GitHub Spec Kit](https://learn.microsoft.com/en-us/training/modules/spec-driven-development-github-spec-kit-enterprise-developers/3-examine-github-spec-kit),
  Microsoft Learn
- [GEARS: The Spec Syntax That Makes AI Coding Actually Work](https://dev.to/sublang/gears-the-spec-syntax-that-makes-ai-coding-actually-work-4f3f)
- [OpenSpec docs](https://openspec.dev/llms-full.txt)
- [writing-code-comments skill](https://github.com/PostHog/posthog/blob/823e2cc7ef325db05c685682be0d8b61b361bcd7/.agents/skills/writing-code-comments/SKILL.md),
  PostHog
- [code-comments skill](https://github.com/abhinav/home/tree/master/.agents/skills/code-comments),
  abhinav, with its references on implementation comments and interface documentation
