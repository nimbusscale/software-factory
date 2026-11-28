---
status: active
retired:
---

# Factory spec notes

A blueprint that collects decisions made while building the factory, each with its reason, until
the specs cover them. When a part of the factory gets its sections of the functional and technical
specs, the entries about that part are sorted into them following the doc standards in
`plugin/skills/standards/`. Once every entry is sorted, this file is retired.

Each entry gives the rule, why, where it was decided, and a guess at its home: `FR`, `TR`, a
decision (`AD`, `TD`) or a code standard (`CS`). The guess is only a starting point. "Why unknown" means no reason was given.

Reasons behind the earlier doc standard, such as why GEARS and why IDs, are in
`docs/research/docs-retro/findings.md`, not here.

## Docs the factory writes

**A new item ID is one more than the highest ID in the doc's current text. Avoiding reuse of a
retired ID is a best effort, not a guarantee.**
- Why: searching git history needs a full clone, and CI and review tools often make shallow ones.
  Reuse needs the highest ID to have been deleted, which is rare. A retired ID shouldn't be cited
  anywhere, so a reused one does little harm.
- Decided in: #14.
- Likely home: `FR` that IDs aren't reused as a best effort; `TD` for how a new ID is found.

**Item IDs only need to be unique. Their order in a doc doesn't matter, so a higher ID can sit
before a lower one, and a spec is never renumbered to put them back in order.**
- Why: Joe: IDs are labels. They count up only because that's easy, and they could as well be
  UUIDs.
- Decided in: #1, reviewing Joe's interactive Dust Law session (nimbusscale/dust-law#17).
- Likely home: `FR`.

**A blueprint's front matter holds its status, `active` or `retired`, and its retired date. The
status is about the doc, never about progress through the work.**
- Why: Joe wants the doc itself to show whether it's retired, even though GitHub tracks status
  too. Why the doc and not only GitHub is unknown. The status stays about the doc because the
  status of work goes in commit messages, never a doc.
- Decided in: #1, reviewing Joe's interactive Dust Law session. Built in #62.
- Likely home: `FR`.

**The blueprint template keeps an empty `retired:` line while the blueprint is active. Retiring
sets `status: retired` and fills in the date, in place of a line saying the doc isn't kept up to
date. The check script flags a blueprint whose front matter is missing or doesn't fit.**
- Why: Claude's choice in #62. An empty line shows the field exists to a writer who never reads
  the standards. The check is cheap, since the front matter has only two fields.
- Decided in: #62.
- Likely home: `TD` for the format; a check for the rest.

**A blueprint never names a skill.**
- Why: a skill changes, and it's used in other projects. The template's line pointing to a file in
  the docs skill ended up in both of Dust Law's blueprints.
- Decided in: #62, from Joe's interactive Dust Law session (nimbusscale/dust-law#17).
- Likely home: `FR`.

**A build plan blueprint retires once the GitHub issues for its phases are created.**
- Why unknown. Claude pointed out that a plan kept both in a blueprint and in issues would drift
  apart. Joe didn't say whether that's his reason.
- Decided in: #1, reviewing Joe's interactive Dust Law session. Built in #63.
- Likely home: `FR`.

**When a doc and the code disagree, the doc wins, unless CLAUDE.md says otherwise. If the agent
can't fix the code within its task, it leaves both and reports the disagreement in its final
report, naming the item ID and the code. In the implementation loop, the report reaches the PR's
description (FR-19).**
- Why: the docs say what the system should do. An agent with no default does whatever it thinks
  best. A headless agent can't ask the user, and opening issues is outside writing docs, so the
  report goes in output the agent already produces.
- Decided in: #18, while splitting the skill.
- Likely home: `FR`.

**Every doc opens with one line saying what kind of doc it is. In the specs, the line also gives
the rules a writer needs, such as GEARS and no links out.**
- Why: an agent or a person may change a doc without reading the standards. The line is how they
  learn what the doc is and how it's written.
- Decided in: #14.
- Likely home: `FR`.

**Requirements are written in GEARS, unchanged.**
- Why: the owner found the Dust Law functional spec read well in GEARS, and where a requirement was
  unclear, it was easy to tell. A tip to make "the app" the subject was dropped, since in a
  technical spec it hides the real subject.
- Decided in: #6.
- Likely home: `TD`.

**A limit is a requirement with its own ID, stated as an absolute: "The game shall run only in a
desktop browser, not on phones or tablets."**
- Why: "shall run in a desktop browser" doesn't rule out running elsewhere. Saying what it does
  only, then what that rules out, is clearer. An ID lets a doc or test cite one limit.
- Decided in: #5.
- Likely home: `FR`.

**The specs describe the app as it is. A limit, non-goal or trade-off the source states holds as
written, whether the source says "for now" or "never". A plan for later stays out.**
- Why: the specs aren't a roadmap. Joe: "they're concerned with only what is of today and not what
  is going to be in the future." This replaces #5's rule that something not built yet goes in an
  issue.
- Decided in: #39.
- Likely home: `FR`.

**The specs are there for the agents that build the app. They aren't the whole description of the
app. Docs for people can live outside them.**
- Why: Joe: "they're there to serve the development process. They're inputs to the software
  factory, but they are not the entirety of the definition of the application." A rule that
  guides no building decision, such as "analytics are shown only as information, not with goals",
  shapes which issues get written, not how the code is built.
- Decided in: #39.
- Likely home: `FR`.

**A limit goes in the spec only when it passes two checks. First, the source says what the app
does, as well as where it stops. Second, where it stops lets the builder design something simpler.
A ban with nothing the app does in it, such as "no advertising", stays out. Whether a rule counts
as a limit decides only whether it goes in the spec, not how it's written.**
- Why: the spec says what the app does, not the endless list of what it doesn't. "No ads" gives a
  builder nothing to build or leave out. "Only one person signs in" lets a builder leave out
  accounts and roles. A limit is kept by designs that respect it more than shown by a test, so
  being hard to test doesn't make it wrong. In the Dust Law and Facet runs, all five agents were
  unsure what counted as a limit, and how to write a ban. Without the last sentence, a reviewer
  flagged an ordinary requirement written with "only ... not" as "written as a limit".
- Decided in: #39, after a trial on a branch.
- Likely home: `FR`.

**A limit goes in the section for the feature whose design it shapes. There's no Limits section.**
- Why: under the two checks, a limit is about the design of one thing the app builds, so it sits
  where that thing's builder reads. With a separate section, writers and reviewers couldn't agree
  which "only" rules belonged in it. This reverses #5's Limits section.
- Decided in: #39, after a trial on a branch.
- Likely home: `FR`.

**The doc standards don't tell the agent to take outside actions, such as opening or commenting on
an issue or a PR. They say what goes in the doc.**
- Why: the same standards are used by a writer, a reviewer and an implementer, and in interactive
  sessions where the owner talks through how to handle things. The factory may not let a given
  agent take those actions.
- Decided in: #39.
- Likely home: `TD`.

**A limit gets a Why under the same rule as any other requirement. There's no Why shared by a
section.**
- Why: one rule for when a Why is written, with no special case.
- Decided in: #5.
- Likely home: `TD`.

**A term defines a word and never states a rule a requirement holds. It cites the requirement
instead.**
- Why: a rule stated in two places can change in one and not the other, and an agent can miss one.
- Decided in: #14.
- Likely home: `TD`.

**A term cites a requirement only when its meaning depends on that requirement's rule. It may
cite a section when that section holds the rules for the thing it names. Otherwise it's a plain
definition, with no citation. The check script doesn't count a citation from Terms when it warns
that nothing cites a requirement.**
- Why: two Dust Law runs cited terms in different ways, because the skill didn't say when a
  reader needs the rule. A citation that only says where a thing comes from adds nothing, and
  Terms starts to read like an index of rules. A requirement cited only from Terms also escaped
  the warning that nothing builds or tests it. Joe preferred the first run's way of citing.
- Decided in: #23.
- Likely home: `TD`.

**To test a term's citation, cover it and read the term. If the word's meaning is still clear, the
citation goes. A requirement that decides who fills a role, such as who a loan's borrower is,
isn't a reason to cite it.**
- Why: in an evaluation, writers cited the requirements that decide who a booking's organizer is
  in 2 of 6 runs, though the skill already said to leave out a citation that only says where a
  thing comes from. With the test and the borrower example, 3 of 3 runs cited nothing on organizer.
- Decided in: #27.
- Likely home: `TD`.

**A term never states a rule a decision holds, as well as a requirement. The test asks whether a
change to either would force a change to the term.**
- Why: in the first Dust Law technical spec run, the Engine term copied the words of the
  architecture decision that created the engine, "holds the game rules and game state". The skill's
  test only asked about requirements, so it didn't cover that.
- Decided in: #51.
- Likely home: `TD`.

**A term never cites an architecture decision, or the section that holds them.**
- Why: the same reason a technical requirement can name a part an architecture decision created
  without citing it. Changing an architecture decision means looking at the whole system again
  anyway, so the citation adds nothing. In the first Dust Law technical spec run, the writer cited
  the architecture decisions that created the engine and the server on those two terms, because the
  skill only talked about requirements. Both
  reviewers flagged the citations.
- Decided in: #51.
- Likely home: `TD`.

**A term may cite a design decision its meaning depends on, the same way it cites a requirement.
For example, "Failed task. A task that still fails after its last try," citing the decision that
sets how many tries a task gets.**
- Why: a design decision can change on its own, like a requirement. Without the citation, the term
  either leaves the reader unable to tell what it means, or copies the decision's rule, which then
  goes stale when the decision changes.
- Decided in: #51.
- Likely home: `TD`.

**A term for a part an architecture decision created names the part's main job and says no more.
It doesn't copy the decision's details. "Worker. The part of the app that runs tasks" is fine.
Adding "and the only part that runs them" copies the decision that the web server runs no task.**
- Why: any definition of a part echoes the decision that made it, so a strict rule would leave
  only "a part of the code", which doesn't tell a reader which part. Copying every detail makes
  two copies of the decision. Naming the main job lets a reader tell the parts apart, and a change
  to an architecture decision means rereading Terms anyway. Joe chose this over a strict rule and
  a loose one.
- Decided in: #51.
- Likely home: `TD`.

**A part an architecture decision creates always gets a term. The decision uses the name but
isn't its home.**
- Why: items name the part without citing the decision. If the decision were the name's home,
  "cite where a word's meaning lives" would make every one of them cite it.
- Decided in: #51.
- Likely home: `TD`.

**To tell a term's definition from a rule, ask of each part of the definition: if a requirement
changed, would this part have to change too? If so, it states that requirement's rule and is cut.
A count or a time can be either. A part the app must do or check, that no requirement holds, is a
missing requirement.**
- Why: the skill said a term never states a rule but gave no test, so terms ended up repeating
  rules. In the third Dust Law run, the writer found the rule hard to apply, and reviewers found
  terms that repeated a requirement's count, or when something is paid or ends. The missing
  requirement case matches the skill's rule that a rule found only in a scenario is a missing
  requirement.
- Decided in: #41.
- Likely home: `TD`.

**"One item for each fact" decides whether a requirement with several triggers, such as "When A
or B", gets split. Triggers that are two facts become two requirements. Triggers that are one fact
stay one requirement. When they list the members of a set another requirement defines, the
requirement cites that one in place of the list. The test counts only a change with a reason of
its own, one someone could really ask for.**
- Why: "One trigger per requirement" and "One item for each fact" pulled against each other, and
  reviewers couldn't tell which won. Facet's FR-34 listed three cases that all answer "not found"
  for one reason. Split, it would be three items for one fact. As a list, it repeated FR-30's and
  FR-33's conditions, so a new kind of hidden view would have to be added in two places. Citing
  FR-30 and FR-33 fixes both. Without the "reason of its own" bar, nearly any two triggers could be
  called two facts by imagining some change.
- Decided in: #40.
- Likely home: `TD`.

**The doc standards' examples come from a different domain than their evaluations.**
- Why: with an organizer example in the docs skill, every writer copied its wording into the spec,
  so a pass showed only that it could copy. With a borrower example, the writers' wording varied and
  they still passed.
- Decided in: #27.
- Likely home: `TD`.

**A word defined in Terms means only that, everywhere in the docs. Another meaning gets a
different word. The review greps for each term and its other forms to check every use. A set
phrase that no reader could take for the term is fine, such as "rounded down" when Round is a
term. Whether a reader could is left to the reviewer's judgment.**
- Why: in the second Dust Law run, Terms defined "Turn" as one player's go, and a requirement
  then used "turn" to mean rotating a tile. A reader who checks Terms gets the wrong meaning. The
  skill said each thing gets one name but not that each name keeps one meaning, so nothing
  stopped the writer. The reviewer caught it only by chance. In the third Dust Law run, the rule
  caught "rounded down" and "turns a person away", which no reader would mix up with Round or
  Turn. One reviewer flagged both, and the other flagged only one. The rule is meant to protect
  meaning, not ban words. A human reviewer would make this call, so an agent reviewer does too.
- Decided in: #25, #42.
- Likely home: `TD`.

**A name says what kind of thing it is, even when it's the only thing of its kind. When two names
share a word, the shared word is never used alone, unless it's a term that lists the kinds it
covers. When a new name shares a word with an existing one, every bare use of the word is changed
to the full name in the same change.**
- Why: in road-trip-agent, "brief" was fine while the trip brief was the only one. When the worker
  brief was added, every bare "brief" became unclear, even in sections about both. In Dust Law,
  "shape" and "catalog" read much better as "tile shape" and "tile catalog", and would break the
  same way if a second catalog were added. In the Facet spec, "each field" meant every fact field
  and framing field, and the rule failed it anyway. A bare word can mean every kind only when the
  reader can tell which kinds those are, and a term that lists them says so. A reviewer only has to
  check that Terms has the word. The term lists kinds, not a dictionary meaning, so Terms doesn't
  fill up with common words.
- Decided in: #16, #42.
- Likely home: `TD`.

**A requirement gets a Why only when both hold: the reason isn't clear from the rule, and knowing
it would change how someone applies or changes the rule. The review checks every requirement's Why
against both.**
- Why: the Dust Law writer and the owner both missed the second test when it was one sentence, and
  the spec got Whys that changed nothing, such as "an outpost pays for being remote".
- Decided in: #13.
- Likely home: `TD`.

**A Why can keep a rule that looks unneeded, such as one that never fires under the other rules,
from being deleted. It says what goes wrong without the rule, not a fact about the system today.**
- Why: an agent cleaning up may delete a rule that seems to do nothing. A Why that says "no other
  rule triggers this yet" goes stale. A rule whose point is obvious, such as never charging twice,
  needs no Why at all.
- Decided in: #13.
- Likely home: `TD`.

**A scenario goes under a requirement only when the result comes from several requirements
working together, and a reader of one of them and the Terms would likely get it wrong. A scenario
never holds a rule of its own, and a vague requirement is rewritten, not given a scenario.**
- Why: a scenario under every requirement gave Dust Law 101 scenarios for 84 requirements. Most
  restated the requirement, implied things nobody meant, hid a vague requirement, or held rules no
  requirement stated. Asking whether a test could be written from the requirement alone found most
  of the real gaps.
- Decided in: #12.
- Likely home: `TD`.

**Under a requirement go only a Why, a Scenario, an Accepted gap, and a table the requirement's
text points to. A plain paragraph never does, and the doc check script flags one. There's no
separate label for an example. A worked example from a source doc is cut unless it passes the bar
for a scenario, and the rule it shows goes in a requirement's text.**
- Why: in the third Dust Law spec run, the writer put the source's examples and some clarifying
  lines in plain paragraphs under requirements. Four of them held rules no requirement had. An
  Example label was weighed and turned down:
  - Every one-requirement example in that run either restated its requirement or hid a rule.
  - If a reader would get a one-requirement case wrong, the requirement needs rewriting.
  - A second label would likely bring back the flood of scenarios the scenario bar stopped.
    Joe: "at least for Claude-based models, you have a desire to sort of over-document".
- Why tables are allowed: specs keep needing them, such as Dust Law's edge-matching and bounty
  tables, and Joe found the way the writer used them fine.
- Decided in: #38.
- Likely home: `TD`.

**When a doc is written from a source, each example in the source needs the rule it shows in a
requirement's text. The example itself can be cut without a mention in the PR.**
- Why: the review check asked that every example be kept or listed as cut. That likely pushed the
  writer to keep the source's examples as plain paragraphs, since the scenario bar left them
  nowhere else to go.
- Decided in: #38.
- Likely home: `TD`.

**Tests trace to functional requirements, not to scenarios. Every functional requirement has at
least one test, and counts as met when its tests pass. The requirements an issue's acceptance
criteria name tell the workflow which tests must pass. They don't define the tests. A test an issue
needs may not exist yet, and then it's written as part of the work.**
- Why: each requirement should be testable, or easy to see how to test, from its own text. If it
  isn't, the requirement needs refining. Tracing tests to scenarios made scenarios carry rules and
  hide vague requirements. An earlier idea, in the docs retro findings, was that scenarios become
  evaluation cases. This replaces it.
- Decided in: #12, in discussion with the owner.
- Who writes them: an issue's acceptance tests are written in the planning session, before the
  run, and the run takes them from a branch. The implementer writes the other tests, and each one
  names the spec item or the bug it checks. `docs/blueprints/testing-a-run.md` has the plan.
- Why: Joe chose the planning session. A test written first has to call something, so whoever
  writes it settles the interface. In the planning session, the owner sees that choice.
- Decided in: #101.
- Likely home: `FR` that every requirement has a test; the rest with the workflow's acceptance
  checks.

**Two items are the same fact if changing one would force a change to the other, and are merged.
If each would change for a different reason, both stay, even when they limit the same action.**
- Why: with no test, writers kept two copies of one fact or merged two facts into one item. In
  Dust Law, "only the current player may lay a tile" and "a laid tile comes from the player's own
  hand" both limit laying a tile, but simultaneous turns would change only the first, and a shared
  pool of tiles only the second.
- Decided in: #17.
- Likely home: `TD`.

**The doc standards don't say technical requirements are rare.**
- Why: the claim rested on one rewritten passage from one project. It could push an agent to sort
  a real technical requirement, such as a backup recovery target, as something else.
- Decided in: #18, while reviewing the split skill.
- Likely home: none. It's a reason not to add a rule.

**One agent writes the functional and technical specs together, from all of the source docs. It
doesn't write the technical spec after the functional spec is done.**
- Why: with both specs open, every fact meets one choice, functional or technical, and a wrong
  choice shows up in one place. Written one after the other, the functional spec is fixed before
  the technical spec starts. A technical fact already in it can't move, so it turns into a repeat
  or a gap, which is harder to trace back. If the functional spec gets worse when written together,
  one after the other is the fallback. The Dust Law runs keep TILES.md as a source, since about half
  of it is rules a player sees.
- Decided in: #19, in discussion with the owner.
- Likely home: unclear. It may only be how the standards are tested.

**A blueprint holds a fact whose home is in code that doesn't exist yet, such as a code comment, a
check, a setting or a data file. Requirements and spec decisions go in the specs even before any
code exists.**
- Why: the questions that sort a fact sent some facts to code comments and checks, which a new
  project doesn't have yet. With no home, a writer forces them into a spec or drops them, and a cut
  the task didn't ask for is a problem. The blueprint's retirement steps already move items to
  comments, tests and checks, so it's the natural place to hold them. The old blueprint question,
  "something to build from before the code exists", caught every fact in a new project,
  requirements included, so it now covers only plans for how to build something.
- Decided in: #19, in discussion with the owner.
- Likely home: `TD`.

**When the source gives no reason for a decision, the writer writes the decision with no Why and
asks for the reason in its report. It never writes a reason the source doesn't give. The check
script keeps flagging the missing Why until the reason is known.**
- Why: the rule that every decision has a Why pushed writers to make up reasons, which read as
  just as settled as real ones. "Why: unknown. Ask the owner." is a status, and statuses never go
  in a doc. Keeping the flag means a decision can't merge without its reason unnoticed, so the rule
  that a decision always has a Why needs no exception. Only the writer's own check changes: it
  can't fix that flag, so it names the question that goes with it.
- Decided in: #19, in discussion with the owner. Settles #2.
- Likely home: `TD`.

**A decision with no Why is also a sign the item may not be a decision at all. There's no way to
mark a decision as having no reason. One is added only if a real decision with no reason turns
up.**
- Why: in Joe's interactive Dust Law session, the two decisions with no reason turned out to
  be facts with no other option: the tile type's shape, and how border positions face
  each other. Joe: "maybe this is a smell, right? It's a signal."
- Decided in: #1, reviewing that session (nimbusscale/dust-law#17). Built in #61.
- Likely home: `TD`.

**A fact with no other option isn't a decision. If the only reason anyone can give for it is that
the rules or the domain work that way, its home is the code: the type that holds it, or the
function that works it out. Until that code exists, a blueprint holds it. The writer checks this
before asking the owner for a missing reason, and asks whether another way was weighed when it
can't tell. The reviewer looks twice at each decision with no Why, and doesn't suggest a Why for
one that isn't a decision.**
- Why: asked for the reasons behind those two decisions, Joe's only answer was "that's the way the
  game works." The first is what the tile type looks like in code, and the second follows from how
  the Border position term names the eight positions. Each has one place in the code, so by question
  8 that place is its home. Dust Law's shape-catalog blueprint already held the rotation table, the
  same kind of fact, so the two moved there.
- Decided in: #61.
- Likely home: `TD`.

**A user uses the app through its own screens, as it's meant to be used. What stops someone who
tampers with the app is a technical requirement. When it protects a rule a user sees, it cites
each functional requirement it protects instead of repeating it.**
- Why: "would a user notice if it changed?" had no answer for a cheater. If the server stopped
  checking moves and only honest browsers did, no honest player would notice, so it isn't
  functional. Repeating the functional rule makes one fact in two docs: in Dust Law, open hands
  would change both "each player sees only their own hand" and "each browser is sent only its
  player's hand". Citing the requirement makes them two facts, and shows whoever changes the
  functional requirement which technical requirement depends on it. Citing the whole functional
  spec instead would leave them searching the technical spec for what to change.
- Decided in: #19, in discussion with the owner.
- Likely home: `TD`.

**A list of tests or checks the app must pass, including a goal for the whole app, isn't written
as a list. An entry the requirements already cover adds nothing. One that tests something no
requirement states is a missing requirement.**
- Why: every requirement has at least one test, so a list of what the tests cover repeats the
  requirements. Without this, a writer turns Dust Law's list of engine tests into technical
  requirements that repeat the functional ones, or drops it, which is a cut the task didn't ask
  for. A goal like "two people can play a game to the end" isn't an open item either, so it isn't
  something to suggest an issue for. Each step in it is already a requirement.
- Decided in: #19, in discussion with the owner.
- Likely home: `TD`.

**A source's "may", "could" or "such as" names options, not a decision, when it says what the
system might do or what its builders might choose. Choosing among them is a decision not made yet,
so the writer asks about it. The part the source settles is still written. A "may" that says what
a person is allowed to do is a rule, and a "such as" that gives an example of a rule is an
example.**
- Why: in the first technical spec run, DESIGN said the client "may use" the engine to show legal
  moves, and the writer wrote a design decision that had the client use the engine. The choice may
  be right, but it wasn't the writer's to make. Joe: words that aren't definite "should not be
  looked at as decisions. They should be looked at options that a decision has to be made about."
  The two limits keep the writer from dropping settled text. "A member may cancel a booking" is a
  rule the app has to follow. The same DESIGN passage uses "such as highlighting where a tile fits"
  as an example of a settled rule.
- Decided in: #19, in review of the first run. Built in #47.
- Likely home: `FR`.

**The option can't come back in other words, such as "can". A sentence that sounds settled but
only makes sense when one option is chosen is part of the same question.**
- Why: in #47's case runs, DESIGN says "The engine is shared code" just before the client "may
  use" it. One writer wrote "The engine is shared code, which the server and the client can each
  import", which settles the option. Joe found the passage ambiguous as a whole, even though each
  sentence alone is clear: "shared" only makes sense if the client uses the engine. The skill
  didn't say where the line falls, so this gives the writer a test for it.
- Decided in: #47, in discussion with the owner.
- Likely home: `FR`.

**A reworded sentence that holds whichever option is chosen must still hold either way.**
- Why: in #47's case runs, writers turned "holds no rules logic of its own beyond what it needs to
  show options" into "uses game rules only to show options". Next to an item that puts every game
  rule in the engine, that says the client uses the engine, which settles the option. Dropping "of
  its own" changed a limit on the client's own code into a statement about what it uses.
- Decided in: #47, in discussion with the owner.
- Likely home: `FR`.

**The kinds of item come in this order. The business side writes the functional requirements.
The technical architect makes the architecture decisions, from the functional spec, their
experience and any standards. A technical requirement comes from a functional requirement, an
architecture decision, both, or the architect alone. A design decision says how a part meets a
requirement.**
- Why: this is how Joe sees who owns what. An architecture decision needs no requirement behind
  it: in the end it's there because the architect chose it. A technical requirement often ties a
  functional requirement to the architecture. "The server checks every action" ties the game rules
  a cheater could break to the decision that created the server. It can also be the
  architect's alone, such as "the user IDs the app stores are its own and never change", whatever
  the sign-in service an architecture decision picked gives. The skill had requirements first, so
  a reviewer said a technical requirement shouldn't name the engine, though DESIGN gives the
  engine that job.
- Decided in: #19, in review of the first run, and #48.
- Likely home: `TD`.

**A technical requirement can name a part an architecture decision created without citing that
decision.**
- Why: an architecture decision is wide. Changing one means looking at the whole system again
  anyway, so a citation on every item that names its parts adds nothing.
- Decided in: #48.
- Likely home: `TD`.

**A requirement leaves the how open: several ways of building it could each meet it. A decision
picks one of those ways. This test replaces imagining a redesign.**
- Why: imagining any redesign flagged the technical requirement that named the engine. Imagining
  only redesigns that keep the architecture decisions still failed: a design that keeps the sign-in
  service could use that service's user IDs, so "the app's user IDs are its own" would count as a
  decision, though it's a requirement the architect set. Joe: it's the better test "as long as it's
  relatively easy to apply and understand the outcome".
- Decided in: #48.
- Likely home: `TD`.

**A pick in the tech stack gets the same test as any other architecture decision: would changing
it touch most of the system? The language and a framework the code is built on pass it, and are
named as examples. A tool that could be swapped while the app stays much the same, such as a
linter or a package manager, isn't a spec item. Its config file records it, with any reason in a
comment there.**
- Why: changing most of the tech stack is a wide change. Dust Law's DESIGN lists TypeScript,
  React, Vite and Node together, and the writer made TypeScript an architecture decision and the
  other three design decisions. Naming a framework in the examples keeps a writer from filing one
  like React as a design decision. Joe, on the tools: "some are architecture and some are not. We
  could change ruff or uv for some other tool and generally keep the app the same. We can not do
  that for python." They "are not as fundamental as the coding language." A runtime isn't named,
  since one such as Node can often be swapped for another with few changes, so it depends on the
  app.
- Decided in: #48. Narrowed to one test for every architecture decision in #76.
- Likely home: `TD`.

**A design decision cites the requirement it meets, a functional or a technical one, in its own
line or its Why. The check script flags one that cites none. One that meets no requirement is
either an architecture decision or a code standard, or a requirement is missing.**
- Why: in the first technical spec run, once the tech stack picks became architecture decisions,
  every design decision outside the code standards could be traced to a requirement. Two looked like
  they couldn't. The shape catalog as data held a technical requirement: the weights can change
  without touching the game logic. Drawing tiles in code meets a functional requirement. A script
  check is free, so no reviewer case tests for a missing citation. A citation to a requirement the
  decision doesn't really meet isn't tested until a run shows reviewers miss it.
- Decided in: #48.
- Likely home: `TD`.

**Code standards are their own kind of item, `CS`, in the technical spec's code standards
section. They need no requirement behind them.**
- Why: they say how all code is written, and most meet no requirement. As design decisions, they
  were the one exception to a design decision citing a requirement, marked only by the section
  they sat in. They had been folded into the design decisions to streamline the kinds of item.
  They aren't a separate doc, since sharing standards across projects isn't a goal. Each project's
  standards go in its own technical spec.
- Decided in: #48.
- Likely home: `TD`.

**The technical spec's code standards come third, as T-SEC-3, after the terms and the
architecture decisions. The sections for each area of the system come after them.**
- Why unknown.
- Decided in: #48.
- Likely home: `TD`.

**A code standard gets a Why only under the rule for a requirement's Why: when its reason isn't
clear and knowing it would change how it's applied. The check script doesn't flag a code standard
with no Why.**
- Why: many code standards write down common practice, so most Whys would add little.
- Decided in: #48.
- Likely home: `TD`.

**Recovery point and recovery time objectives stay technical requirements. "Would a user notice
if it changed?" stays the test for a functional requirement.**
- Why: they're business goals a user doesn't see. Joe didn't want a third kind of requirement for
  them, and the test is good enough for the factory's needs.
- Decided in: #48.
- Likely home: `TD`.

**A technical requirement that protects rules spread across several sections cites those
sections, plus the IDs of the protected requirements outside them. Its own wording says which
rules in those sections it covers. It never cites the whole functional spec.**
- Why: citations are there so a change's effects can be traced. Citing the whole functional spec
  loses that, since no one can tell what the technical requirement covers without reading all of
  it. Listing every ID adds little. With sections and IDs, a miss can be seen and discussed, as when
  a reviewer asked why Dust Law's technical requirement on what the server accepts left out two
  functional requirements. Requiring a cited section to hold only protected rules would mean
  listing about 40 IDs in that requirement, or laying out the functional spec around what the
  server checks. That requirement already shows the wording doing the work: it covers what's
  "allowed by the rules in" its sections, so a setup rule like "lay a start tile" in the section on
  setting up a game isn't covered.
- Decided in: #19, in review of the first run, and #49.
- Likely home: `TD`.

**When a change adds an item to a section, or edits one in it, the check script flags each
citation of that section from before the change. A citation added in the same change isn't
flagged. No step was added to the procedure for this.**
- Why: a citation of a section covers whatever the section holds now, so a new rule can fit a
  technical requirement's wording without being one it should cover. Joe's worry was exactly that
  case. The flag tells the writer and the reviewer to check that the citation still fits, and the
  review already says to decide each SIGNAL line, so no new step is needed. A citation written in
  the same change was written against the section as it is now, so flagging it would only add
  noise, such as a flag for every section citation in a new spec.
- Decided in: #49.
- Likely home: `TD`.

**A term in the technical spec never states a decision's choice. It cites a decision only when the
citation passes the cover test.**
- Why: "Engine. The part of the code that holds the game rules and game state", citing the
  decision that created the engine, repeats that decision's choice. Changing the decision would
  mean changing the term too: one fact in two places. That
  was a reviewer's reasoning, and Joe agreed with it.
- Decided in: #19, in review of the first run. Built in #51.
- Likely home: `TD`.

**Commands and pointers, such as the command that says work is done or where the settings file
is, don't go in the technical spec. A choice about them, such as keeping settings in a config file
versioned with the code, is still a design decision. CLAUDE.md works as a directory that tells an
agent where to find them.**
- Why: they're operational, not about how the app works, and the technical spec keeps out process.
  Joe sees CLAUDE.md as a directory to the repo's other docs. It holds little itself, since it's
  shared with other concerns. road-trip-agent's `development.md` held things like this and turned
  into a ledger of development activity, so whatever home is chosen needs rules against that.
- Decided in: #19, in review of the first run. Built in #52. The home is decided in #53.
- Likely home: `TD`.

## Doc standards and skills

**Docs work has no skill. The doc standards in `docs/standards/` hold all of it: what each doc is
and how it's written, how to add or change an item, how to check a change, and what goes in a
report. A project's CLAUDE.md says where the standards are, and to read their README before
writing or reviewing a doc.**
- Why: Joe: "my goal was to try to leverage the skill mechanics to provide progressive disclosure,
  but I don't think we need the skills to do that anyways, as long as we provide reasonable ways
  for the agent to find that data itself or point it to the data itself." Plain files give
  progressive disclosure on their own, since an agent reads only the files its task needs. In early
  eval runs without the skill, Opus found the standards in the case's repo and read the ones its
  task needed, with no CLAUDE.md pointing to them. Joe sees a skill as more useful for handing
  knowledge to sessions whose repo you don't control, such as end users': "I think the skill
  becomes more important when you're trying to distribute that knowledge or details across other
  agent sessions." The factory controls every repo it works in, and its CLAUDE.md.
- Claude looked for other reasons to keep a skill and judged none strong enough. After compaction,
  Claude Code re-attaches the start of each loaded SKILL.md but not files the agent read, but
  SKILL.md had become mostly pointers to the standards. Only the roles given a skill can load it,
  but an agent that reads a standard it doesn't need only wastes tokens. A skill's description
  loads it in an interactive session, but a CLAUDE.md line does the same job and is always in
  context, and no run had tested loading by description.
- Joe raised one risk. A light mention, such as a requirement ID, might load a skill and its
  procedure with it, while a pointer in CLAUDE.md leaves reading the standards to the model's
  judgment. In the loop, each role's prompt is fixed and can be tested. In an interactive session
  it isn't. The `items-write-implied` eval case covers part of this risk. It asks only for a code
  feature, never mentions the docs, and passes when the agent updates both specs and asks for the
  reason behind a technical choice.
- Every eval case passed without the skill, except for one miss in a case that passed its other 4
  runs.
- Decided in: #67, in an interactive session. It replaces #60, which was going to tune the skill's
  description.
- Likely home: `AD`.
- Replaced by AD-14 in the technical spec: the standards are a skill in the factory plugin, so a
  session in any repo, on any machine, gets them the same way. Decided in #103 and #107.

**Nothing checks that a doc change in an interactive session gets a review by a subagent. Docs work
moves on to getting the factory running, and the factory improves its docs work from there.**
- Why: Joe: "we spent a long time trying to perfect or get the doc reviewing and writing sorted
  out, and I just want to move on. I think we're in a good place here." The review of Dust Law's
  specs against the standards (nimbusscale/dust-law#17) found real problems, such as a dropped
  rule that let any bounty be claimed. Joe: "while I'm sure there's ways to improve it, I'd rather
  get us to the point where we're actually have the factory running and we could do potential
  self-improvements that way."
- Decided in: #68, closed as won't do, in an interactive session.
- Likely home: none. It's a choice about the order of work, not about the factory.

**The guide to which standards file a task needs is the standards' `README.md`. CLAUDE.md says
only where the standards are, and to read the README before writing or reviewing a doc.**
- Why: agents read a short README whole. road-trip-agent's design README was read whole in 141 of
  146 transcripts. A table in CLAUDE.md would be copied into every project's CLAUDE.md, and each
  copy would need fixing when the standards' files change. `project-docs.md` is about 2,000 words,
  and agents read big docs in slices. Claude proposed this, and Joe agreed.
- Decided in: #67.
- Likely home: `TD`.

**CLAUDE.md's doc map is the one place that says where each doc is, including the standards and the
doc check script. The standards give no default paths and no search for a doc that isn't there. If
a doc or a folder in the doc map doesn't exist yet, the agent creates it there, a doc from its
template. If an agent can't find the standards, it stops and says so, a rule CLAUDE.md gives next
to its pointer.**
- Why: the defaults let the skill work in a project with no doc map. Without the skill, the doc map
  is how an agent finds the standards at all. The CLAUDE.md template from #54 ships the doc map with
  the usual paths, so a new project still starts with them. The rule for missing standards is in
  CLAUDE.md, since an agent that can't find the standards can't read their README. The doc check
  script is in the doc map too, since the standards give no path of their own. Claude proposed
  naming the script there, and Joe agreed.
- Decided in: #67.
- Likely home: `TD`.
- Replaced by the project contract, in `project-contract.md` in the factory plugin's standards. A
  project's specs and blueprints sit at fixed paths, and every session loads the standards from the
  factory plugin (AD-14). Decided in #103, and built in #105.

**The doc standards cover only the functional spec, the technical spec and blueprints. Research
docs, skills, CLAUDE.md and a README are other concerns.**
- Why: Joe: the specs and blueprints "are effectively the code that we input into an agent to do
  work". They're owned entirely by the agents that use the standards. CLAUDE.md is shared with other
  concerns, and a README is mostly read by people. The skill has also grown large, and its
  procedure is getting heavy on steps.
- Decided in: #19, in review of the first run. Built in #46, under #1.
- Likely home: `TD`.

**The doc standards have no guidance on research docs or skills. Guidance on CLAUDE.md waits in
#54, including that CLAUDE.md holds a short table of where each kind of fact goes. An agent finds
each doc through CLAUDE.md's doc map.**
- Why: dropping research docs and skills was Claude's proposal, since no other skill in the repo
  writes them. Joe hasn't given a reason of his own. Joe didn't want the CLAUDE.md guidance to get
  lost when it left the skill, so it went into an issue right away rather than being dropped.
- Decided in: #46.
- Likely home: `TD`.
- Its last sentence is replaced by the project contract: an agent finds each doc at its fixed path,
  which `project-contract.md` in the factory plugin's standards gives. Built in #105.

**The doc check script checks only the specs and blueprints, and the spec IDs cited
anywhere in the repo. The checks it used to run on other docs, such as history in CLAUDE.md and
links into research docs, wait in #55.**
- Why: Joe wanted the script's scope to match the skill's. He didn't want the checks on other docs
  lost, so they went into an issue right away.
- Decided in: #46.
- Likely home: `TD`.

**The doc standards decide when a fact's home is a code comment instead of a spec. The code comment
standards, `code-comments.md` in the doc standards' folder, say whether a comment is needed and how
to write it. They're a plain file, not a skill, and hold a few short examples, with no examples
file of their own. A decision sent to a comment, or to a blueprint until the code exists, carries
its reason, and an agent asks for a missing one the same way as for a spec decision.**
- Why: Joe wants the doc guidance linked to the code-comment guidance. The guidance is a file of
  standards because the doc guidance became one (#66, #67). Claude proposed it, and Joe agreed. On
  examples, Joe: "I was thinking that this wouldn't be that complicated, that we would need 417
  lines of examples. It seems like a lot." On the reason: a comment's job is the reason, and the
  docs side picks the comment as the home while it still has the source, often before the code
  exists. That's the best time to ask for a missing reason.
- Not decided yet: whether code comments get eval cases. Joe wants to see how the standards work
  first.
- Decided in: #46. Made a file of standards, with the hand-off for reasons, in #65.
- Likely home: `TD`.

**The doc standards' procedures, for changing an item and for checking a change, say what must hold
when the work is done, not how to get there. They
give an order only where it matters: search for a fact before writing it, and check the change
last. Each procedure still has a checklist of those goals for the agent to copy into its task list
and tick off.**
- Why: the procedure was getting heavy on steps. Joe asked to state goals where a step wasn't
  needed. The checklist stays because Anthropic's skill best practices recommend one for complex,
  multistep work, so Claude doesn't skip a check. The evals were also tuned with it in place. Joe
  would rather keep what's known to work than spend time testing with and without it.
- Decided in: #19, in review of the first run. Built in #46.
- Likely home: `TD`.

**The doc standards' `project-docs.md` holds what every doc needs. A rule used by one kind of doc
goes in that doc's file of standards. The two specs share one file, `specs.md`, which also holds the
rules for writing their items: GEARS, the lines under an item, one item for each fact, the Terms
section and IDs. How to add or change an item, how to check a change, what goes in a report, and
the worked examples each have a file of their own. The README names every file directly, so no
file is reached only through another.**
- Why: an agent may only partly read a file it reaches through another file. The two specs are
  usually written and checked together, so a file for each saved little: a spec writer read both.
  Each task file is read only by the tasks that need it.
- Decided in: #18. The shared specs file in #19, in discussion with the owner. The task files moved
  out of the docs skill in #67.
- Likely home: `CS`.

**The doc standards give the standard a doc must meet and trust the model on method. They have no
step-by-step method for turning existing docs into specs. It only checks that nothing in the source
was dropped, whatever the source is.**
- Why: Anthropic's guidance says to assume Claude is capable. The Dust Law conversion went fine
  without a method. Facts come from many sources, such as source docs, issues or a long spoken
  explanation, and the same standard and check fit them all. Guidance gets added only if the Dust
  Law and Facet runs show it's needed.
- Decided in: #20.
- Likely home: `CS`.

**The doc standards don't say what happens to source docs after they're turned into specs. The
task's prompt says it, such as "delete the foundation docs".**
- Why: it won't always be the same. Some projects may keep their source docs.
- Decided in: #18, after the second Dust Law run.
- Likely home: `CS`.

**A skill keeps a reason only when, without it, an agent would likely act differently. Other
reasons go in the specs.**
- Why: a skill's body is read every time it's used, so a sentence that doesn't change what the
  agent does is clutter.
- Decided in: #18, about the ID section.
- Likely home: `CS`.

**Skill names use the gerund form, such as `writing-project-docs`, and don't name the factory.**
- Why: Anthropic recommends the gerund form. The model sees the name next to the description, and
  the name is the command a person types. A project using the skill doesn't need to know where it
  came from.
- Decided in: #18.
- Likely home: `CS`.

**Skill descriptions are written in the third person, such as "Writes and reviews…".**
- Why: Anthropic's guidance says to always write descriptions in the third person.
- Decided in: #18.
- Likely home: `CS`.

**A draft skill sets `disable-model-invocation: true`, so it loads only when typed as a command.
Whether its description loads it is tested once the skill is complete, then the setting is
removed.**
- Why: a draft can load by accident in sessions that write docs and apply rules that aren't
  settled. Testing a description that will be rewritten is wasted work. Loading concerns the whole
  skill, so it's tested once for the whole skill.
- Decided in: #18 and #1.
- Likely home: `TD`.

**A skill points to another skill's guidance by what it covers, not by the skill's name, such as
"follow the project's guidance for writing code comments".**
- Why: a skill may be renamed, and a project may not have it.
- Decided in: #18.
- Likely home: `CS`.

**A procedure with steps in order, or a list of checks, gives a checklist the agent copies into its
task list. Each file of the doc standards an agent may read on its own, such as the review file,
has its own checklist.**
- Why: a skipped step becomes visible, and an evaluation can see from the transcript which steps
  were done. The steps most likely to be skipped are searching first, following the change, and
  checking it. Within checking, the reading checks are skipped most easily, since a script can't
  do them. A reviewer reads only the review file, so it can't use another file's checklist.
- Decided in: #18 and #22.
- Likely home: `CS`.

**A review covers only problems the change caused. A problem is older than the change if the same
problem is on the branch the change merges into. A reviewer lists older problems apart from the
rest. An agent checking its own change leaves older problems alone and doesn't mention them.**
- Why: a reviewer that flags something unrelated to the change sends it to the implementer, which
  then has to fix it or drop it, and a dropped problem gets lost. A change can still cause a
  problem in a line it never touched, such as a doc left out of step with changed code, so the
  scope is what the change caused, not the diff. Older problems belong to the doc curator, which
  looks at the docs as a whole and opens issues for what has drifted. For the implementer, older
  problems aren't its concern, and mentioning them spends tokens.
- Decided in: #33.
- Likely home: `FR`.

**A reviewer reads the file for each kind of doc a change touches, such as the functional spec's
file, as well as the review file.**
- Why: so it knows the rules for how that kind of doc is written. Without them, it judges each item
  only by the general rules, and can flag an item that follows its doc's rules as a
  problem. A reviewer suggested cutting "not later" from a limit, when the functional spec's rules
  ask every limit to say what it rules out.
- Decided in: #35.
- Likely home: `FR`.

**A reviewer judges each cut against the task, not the author's account of the change. The task is
what the change was made for, such as the issue or the prompt. The author's account is the commit
message or PR description. A cut the task doesn't call for is a problem, whatever reason the author
gives. With no task given, every cut is one.**
- Why: the task is written before the work, by someone other than the author. So it shows which
  cuts were planned without the author's reasons, which could sway the review. A reviewer that
  reads them might accept a cut because it's explained, without asking whether it was right, or
  look only where the author points. Without some record of planned cuts, a reviewer can't tell a
  planned cut from a lost fact: in the third Dust Law run, the writer left blueprint facts such as
  the tile weights out on purpose.
- Decided in: #36.
- Likely home: `FR`.

**A fact whose home is outside the specs and blueprints isn't dropped when it's left out of them.
The reviewer decides that from the doc standards, not from the author's account. The writer names
each such fact, and where it likely belongs, in its report.**
- Why: the specs and blueprints aren't a project's only docs. They hold the details that drive
  development. DESIGN's purpose paragraph belongs in something like a README or CLAUDE.md, and the
  writer said so, but both reviewers counted it as dropped. The reviewer judges it itself, so the
  rule above about judging cuts against the task still holds.
- Decided in: #19, in review of the first run. Built in #50.
- Likely home: `FR`.

**When the source leaves part of a rule open, the writer writes no rule for that part, and doesn't
copy the vague wording either. It raises a question in its report: the source text, what's
unclear, and a suggested answer. It still writes the parts the source settles. The agent's prompt
says what happens to the question: in an interactive session it's asked, the implementation loop
lists it in the PR's description (FR-20), and a test run puts it in the report.**
- Why: a reader of the doc alone can't tell a guess from a settled rule, and open items never go
  in a doc, so a guess can't be marked as one. In the Facet run, the writer turned the undefined
  "eligible public content" into "every public item that fits it", and listed it as open only in
  the commit message, which isn't read after merge. The Dust Law runs did the same, such as a
  requirement settling a garrison timing the source never stated. "A test could check it" isn't the bar, since
  a limit isn't checked by a test. The bar is whether the writer would have to choose part of the
  rule itself.
- Decided in: #37.
- Likely home: `FR`.

**A reviewer flags a rule, or a part of one, that nothing settles: not the task, the source the
change was written from, or the docs already there. The author's account doesn't settle anything.
A reviewer that wasn't given the task or the source skips this check, and says so in its report.**
- Why: writers keep writing guesses as rules, and a reviewer comparing the change to its source is
  the last place to catch one. In the loop, the implementer lists the choices it made on open points
  in the PR (FR-20), so the reviewer may also see a guess there. Without the source there's nothing
  to compare against: judging from the spec alone can't tell a guess from a choice the owner made.
  Saying the check was skipped keeps a clean report from looking like a pass.
- Decided in: #37.
- Likely home: `FR`.

**The doc standards say what a finding contains: where it is, what's wrong, a suggested rewrite and
why it fixes it. The task's prompt says how findings are delivered. With no instructions, they go
in the reply.**
- Why: the same standards are used in an interactive session, in the factory loop and in
  evaluations, and each needs a different format. In the implementation loop, a role hands back its
  result as structured output (TD-1). No one skill defines how an agent works, since an agent loads
  several skills.
- Decided in: #33.
- Likely home: `TD`.

**The doc check script needs a git repo and a base branch. Checking docs outside a git repo isn't
supported. It writes no files.**
- Why: nearly every run happens in a repo, so supporting docs outside one isn't needed. It only
  reads files and prints what it finds, so it has no reason to write, and an evaluation's sandbox
  doesn't let it write.
- Decided in: #33.
- Likely home: `TD`.

**The doc standards are used in three ways, and they don't say which one is in play. The implementer
and reviewer use it in the implementation loop, where the specs already exist and each change adds
to them. The doc curator uses it to compare the docs and the code as a whole and raise issues for
what's out of step. A person uses it in an interactive session, which is where specs are first
written and often refined before an issue goes into the factory. Where the three need different
behavior, the standards set a default and the agent's prompt says what happens next.**
- Why: Joe expects all three uses. A rule written for one can be wrong for another. The uncited-ID
  signal is noise on a first draft but useful in the loop. A vague point in the source should be
  asked about in an interactive session, but in the loop the implementer decides it and lists it in
  the PR.
- Decided in: #18, while planning #36, #37 and #43.
- Likely home: `CS`.

**By default, the doc check script flags a requirement that nothing cites only if something cited
it on the base branch. With `--uncited`, it flags every requirement that nothing cites.**
- Why: in the implementation loop, a requirement that loses its last citation is the useful
  signal. A requirement written before the code that meets it is normal. On a first draft nothing
  is cited, so the old check flagged nearly every requirement: 88 of 91 in the third Dust Law run.
  That buried any other signal. The doc curator still needs the full list, so it uses `--uncited`.
- Decided in: #43.
- Likely home: `TD`.

**The doc standards don't assume the agent can reach GitHub. It talks about the task and the agent's
report, not a PR or issues.**
- Why: agents get different access. In the implementation loop only the workflow has access to
  GitHub (AD-7), and the quality reviewer gets only what TR-7 allows. The doc curator may be
  allowed to read PRs, to see what changed since its last run.
- Decided in: #18, while planning #36. The last wording that sent facts to issues was removed in
  #46.
- Likely home: `CS`.

**The doc standards aren't changed to make the writer's check of its own work deeper. A fresh
reviewer is the real check.**
- Why: Joe expected the writer's own check to be thin, which is why a reviewer runs after it. In
  his interactive Dust Law session, the writer ran the check script and a few searches. It missed a
  contradiction between two requirements and four leftover uses of a word it had renamed itself.
  The reviewer caught both.
- Decided in: #1, reviewing that session (nimbusscale/dust-law#17). See #21 for who runs reviews.
- Likely home: `TD`.

**A milestone in a project's life, such as starting a project, is a slash command or a script, not
a skill that loads on its own. Work that can come up in any session, such as creating an issue, is
a file of standards that CLAUDE.md points to, as the doc standards are.**
- Why: Joe: for starting a project, a script is probably fine and a skill isn't needed. Interactive
  sessions after a project starts need to know how to create issues and what the statuses mean,
  and a command only runs when someone types it. That work was first going to be a skill. When the
  docs skill was replaced by the doc standards (#67), Joe decided the same holds for GitHub work.
- Decided in: #1, reviewing Joe's interactive Dust Law session, and changed in #64. Built in #63
  and #64.
- Likely home: `TD`.

**The GitHub standards are `github.md` in the doc standards' folder. CLAUDE.md's doc map lists it,
with a line saying to read it before starting work on an issue, writing, updating or closing an
issue, naming a branch, or writing a PR's title or description. Where the board's statuses are defined is in the implementation loop
blueprint.**
- Why: next to the doc standards, the GitHub standards are copied into each project along with
  them. Claude proposed this, and Joe agreed.
- Decided in: #71.
- Likely home: `TD`.

**The doc standards are plain files, apart from any skill. Within them, what the docs are and how
they're written is kept apart from how to do a task with them: change a doc in `changing-items.md`,
check a change in `reviewing.md`, and what goes in the report in `reports.md`. A rule about IDs is
split the same way: that an item's ID always means the same thing is a standard, and how to pick a
new ID, or tell whether a change keeps an item's meaning, is in `changing-items.md`.**
- Why: other skills need the standards too, such as one that writes GitHub issues or code comments.
  While the standards live in the docs skill, other skills have to point into it or keep their own
  copy, and changing a standard means releasing a new version of the skill. Joe: "if we update the
  specification, then we got to update the skill. And then do we then now have to worry about any
  kind of references between skills?" Splitting them "drives a good, clear delineation between what
  specs and standards are versus how those specs and standards are used for a specific task, where
  the later portion is handled by the skill." It also lets an agent that only needs to know what a
  `TR` is read the standards without loading the skill. On IDs: a reader, such as whoever writes a
  code comment or an issue that cites a requirement's ID, relies on the ID keeping its meaning. Only
  an agent changing a spec needs to know how. Claude proposed this split, and Joe agreed.
- Decided in: #66, while discussing #60. The task files moved out of the skill and into the
  standards in #67.
- Likely home: `AD`.

**The doc standards' source is files in the factory repo, in `plugin/skills/standards/`, versioned
and reviewed like everything else. Not a GitHub wiki.**
- Why: agents would read a wiki through WebFetch, which treats a page as untrusted data, not
  instructions, and returns a smaller model's summary, not the exact text. A wiki edit also isn't
  reviewed or pinned to a version, so it would change every agent's behavior at once with no eval
  run. Claude suggested this, and Joe agreed.
- Decided in: #66.
- Likely home: `AD`.

**Each project that uses the factory has its own copy of the doc standards, the same way it has
the factory's skills, along with the doc check script. Its CLAUDE.md doc map says where each one
is. How the copy gets there, by push or pull, isn't decided.**
- Why unknown. On how the copy gets there, Joe: that's "less interesting to me to focus on than
  the workings of the factory itself." For the repo or two using the factory now, a script or an
  agent can do the copy.
- Decided in: #66.
- Likely home: `AD`.
- Replaced by AD-14 in the technical spec: a project's sessions load the factory plugin, so a
  project keeps no copy. Decided in #103 and #107.

**When the factory runs, its roles follow the factory's own version of the doc standards, not the
copy in the project's repo. The project's copy is for interactive sessions, which work outside the
factory, so they work to the same standards and know how to hand the factory its issues. How the
factory makes sure its roles get its own version isn't decided. Until it is, standards the roles
follow, such as the quality reviewer's rubric, still go in `docs/standards/`.**
- Why: the standards drive how the factory's agents behave, the same way code does. Joe: "If we
  look at these doc standards like code, which they are effectively, they're code inputted or used
  to drive behavior of the agent, then we can't just rely on each repo copy of the code." A change
  to one project's copy, such as to how GitHub work is done, would change what the factory's roles
  do in that project, with no review or eval run in the factory. A project could also tune the
  factory's review to itself, when the factory means to keep one review process for any project.
  Claude raised the tuning, and Joe widened it to every standard.
- Decided in: an interactive session while planning #91, which puts the quality reviewer's rubric
  in `docs/standards/`.
- Likely home: `AD`.
- How the roles get the factory's version is AD-14: the workflow loads the factory plugin from the
  SFE's image, and gives each role its skill. Decided in #103 and #107.

**The templates for each kind of doc are part of the doc standards, in `templates/`.**
- Why: a template is a second copy of standards, such as a spec's opening line, the technical
  spec's fixed sections and the form a limit is written in. Kept next to the standards, the two
  change and are reviewed together. Another skill that creates a doc can also use them. Claude
  proposed this, and Joe agreed.
- Decided in: #66.
- Likely home: `TD`.

**The doc check script leaves out `<docs folder>/standards`.**
- Why: the standards are full of example IDs that no project defines, such as `FR-41`. The script
  would flag each one as a broken citation. Claude proposed this, and Joe agreed.
- Decided in: #66.
- Likely home: `TD`.
- Replaced in #107: the script leaves out no standards folder of its own accord, since no project
  holds the standards. This repo's ignore list names `plugin/`.

**The doc check script also leaves out every path that `.check-docs-ignore` at the repo root
matches, written like a `.gitignore`. A project with no such file is checked as before.**
- Why: a project can hold files that cite IDs that aren't its own. The factory's eval cases build
  test projects, and their files cite IDs the factory's docs don't define, so the script flagged
  each one. The script is copied into every project, so it can't name a folder such as `evals/`
  itself. Claude proposed this, and Joe agreed.
- Decided in: #67.
- Likely home: `TD`.
- In #107 the list moved to `[check_docs] ignore` in the project's `software-factory.toml`, in
  place of `.check-docs-ignore`, when the script became a Python script that can read it.

**The doc check script flags a shared run of eight words only when one of its copies is on a line
added since the base branch. It leaves out retired blueprints, and every run that's in a doc
template.**
- Why: agents read the copy signals and moved on, and the list kept growing. Joe: "When I watch
  them work, they just say, okay, this is Signal, and then they sort of ignore it, and then it
  just seems to be growing... what's the point of tracking them?" On main, the check flagged 13
  pairs of files, and none was a fact with two homes. Three were the opening paragraph that the
  blueprint template gives every blueprint, which adds a pair for each new blueprint. One was a
  retired blueprint, which is frozen like a research doc. The rest were the same phrase used on
  purpose, such as "when the implementer finishes the work the issue asks for" in FR-8 and TR-12.
  Looking only at added lines is how the history check already works. Claude proposed this, and
  Joe agreed.
- Decided in: an interactive session about the copy signals.
- Likely home: `TD`.

**Whether each spec item and bug fix the work calls for has a test is the purpose reviewer's
check, not the quality reviewer's. The quality reviewer's rubric has no label for a missing test.
It checks only whether a test is wrong (F5) and whether a test names its rule (N5).**
- Why: Joe: "The quality checker says, of the things that were built, are they of quality? The
  purpose checker says, of the things that are built, does it meet what the issue is being asked
  for?" Knowing which spec items call for a test means reading what they say, and the quality
  reviewer doesn't judge the code against the docs. Until the purpose reviewer is built, no
  reviewer checks for a missing test. Joe raised the move, and Claude agreed.
- Decided in: #110.
- Likely home: the rubric and the purpose reviewer's prompt.

**A test that a change adds or changes, and that names no rule, is a note (N5), so it's a nit.
It isn't a fix.**
- Why: Joe, on whether tests beyond what a spec item calls for are allowed: "There's a cost to
  them, a cost to reading and writing, updating them, managing them over time." A nit puts the
  test in front of the owner and the implementer without starting another round. Joe: "I think
  the nit item is the best middle ground." N2, a missing test for behavior the change didn't add,
  no longer fits once the quality reviewer doesn't look for missing tests, so N5 replaces it with
  a new code.
- Decided in: #110.
- Likely home: the rubric.

## Evaluations

**The doc evaluations live in `evals/docs/`, one folder per case, and run with `claude plugin
eval`, through `evals/run-docs-evals.sh`. The script holds the flags every run uses.**
- Why: the skill-creator skill on its own leaves the orchestration to us, including setting the
  judge model and much else we'd have to build. `claude plugin eval` has that orchestration built
  in, and it runs a case with no plugin. Joe wanted one script to wrap the whole run.
- Decided in: #24. Moved out of the skill, with the script, in #67.
- Likely home: `TD`.

**A grader checks that a reply has the information needed, in any words. It never checks the
reply's headings or layout.**
- Why: a model can't be failed for not following an output shape. If the shape matters, the task
  should use structured output.
- Decided in: #33.
- Likely home: `TD`.

**The doc evaluations have no second run without a plugin, and no `passes-without-skill` tag or
column.**
- Why: there's no plugin to leave out, so `claude plugin eval` runs each case once, as is.
- Decided in: #67. It replaces running a case without the skill, from #33, and the tag, from #57.
- Likely home: `TD`.

**Each case sets its own run count with `runs` in its `prompt.md`. A case that passes 3 of 3 in a
full run gets `runs: 1`. The rest run 3 times. When a 1-run case fails, it reruns 3 times right
away. If it passes 3 of 3, it stays at 1 run. If not, it goes back to 3. To re-baseline, such as
when the agent's model or effort changes, every case runs 3 times, and the run counts are
updated.**
- Why: a full run is costly when every case runs 3 times. Joe: the work and runs for one issue took
  about 6% of his allocation. Anthropic's post "Demystifying evals for AI agents" splits evals into
  capability evals, which test what the agent can't do well yet, and regression evals, which check
  it still does what it used to. A capability eval that passes reliably moves into the regression
  suite. The 3-run rerun keeps one bad run from deciding anything, without needing a history of
  results. `runs` goes in `prompt.md` because `model` and `max_turns`, the other run settings, are
  there.
- Decided in: #57.
- Likely home: `TD`.

**The judge model is Sonnet. The agent under test runs on Opus for now.**
- Why: Anthropic's guide for `claude plugin eval init` recommends a Sonnet-class judge. The factory
  is made to work on Opus first. Cheaper models for some agents come after.
- Decided in: #27 and #33.
- Likely home: `TD`.

**Each rule the review checks gets a reviewer case. A rule gets a writer case only when real
runs show writers keep breaking it, or when no review check covers it. A writer case starts from
the real input that led to the mistake, cut down, when there is one.**
- Why: the reviewer is the last check before a problem gets through, and a writer checking its own
  work runs the same review checks, so one reviewer case covers both. A reviewer case can plant
  exactly the problem to find. A writer case can only hope the writer makes the mistake. Each case
  costs runs, so cases are added only where they're needed. A writer case is still worth it when
  the reviewer keeps catching the same mistake, since each catch costs another round. A real
  mistake makes a better test than an invented one.
- In #67, six writer cases whose rule a reviewer case also covers were dropped. Three stayed: the
  two `review-roles` writer cases, which test what a writer does with its own change, and
  `items-write-limits`, since no reviewer case covers limits. The reviewer's prompt is fixed, and
  its review is the guard against a writer that doesn't follow the standards.
- Decided in: #24.
- Likely home: `TD`.

**Each case has a role tag, `write` or `review`, and a group tag, so a group runs together.**
- Why: related cases run together without naming each one, the way a test class does.
- Decided in: #33.
- Likely home: `TD`.

**A case's name starts with its group tag, then its role tag, such as `terms-review-citations`.**
- Why: when a group runs, it's easy to tell which cases belong to it.
- Decided in: #27.
- Likely home: `TD`.

**The evals README records no run results.**
- Why: results change with every run, and they go in the PR and the issue. It used to record each
  case's last run without the skill, as a baseline, and that baseline went with the skill.
- Decided in: #27. The baseline column was dropped in #67.
- Likely home: `TD`.

**A case's planted problems are ones the doc check script flags.**
- Why: the cases test what the agent does with a problem, not whether it can find one.
- Decided in: #33.
- Likely home: `TD`.

**A behavior that lives in a script is tested by running the script on small repos, not by an
evaluation case.**
- Why: the behavior is in the script, so the script is what to test.
- Decided in: #43.
- Likely home: `TD`.

**A failing case is run on its own until it passes 3 runs out of 3. When every case in a group
passes, the whole group runs, each case at its own run count, to catch anything a change to the
standards broke. Before a 3-run
pass, each case runs once. A case whose setup was fixed runs once more, and goes into a 3-run pass
only when its result has nothing to do with the setup. A case gets up to 3 single runs, with fixes
to the standards, the case or its graders in between, before its 3-run pass.**
- Why: a single run can pass by luck. `review-roles-review-clean` passed one run, then failed 3 out of 3. A
  case that has passed reliably runs once, since each run costs tokens. The single run catches a broken setup before the bigger run spends three times as much. If a setup
  fix doesn't work, every run in a 3-run pass is wasted, so each setup has to be right first. The 3
  single runs give room to find and fix problems before the bigger run. Joe: "3 is just a nice
  limit that you typically are able to work it within to get it to pass. So I just needed some
  number. 3 seemed reasonable, and it's worked out so far."
- Decided in: #33 and #41. Per-case run counts replaced leaving out a case that passed both ways
  in #57.
- Likely home: `TD`.

**A doc reviewer checks the docs and whether the code does what they say. It doesn't mention a
code bug that leaves the docs right.**
- Why: code bugs aren't a doc reviewer's concern.
- Decided in: #33.
- Likely home: `FR`.

**A gap that only shows up because of how a test run is set up isn't a lesson for the standards. In
the Dust Law runs, reviewers don't see the writer's questions, on purpose.**
- Why: the non-interactive conversions are a stress test, not a real mode. In real use, questions
  are answered live in an interactive session, or raised by the issue checker or the implementer
  in the factory. Keeping the questions from reviewers means each agent makes its own judgment,
  without being swayed. The source docs are deleted only so the check script doesn't flag copies.
- Decided in: #19, in review of the first run.
- Likely home: unclear. It may only be how the standards are tested.

**Two eval cases can be merged into one when they share a base spec or notes and their planted
problems don't touch each other. The merged case keeps every grader. A merge is backed out when a
grader that passed in its old case fails in the merged case, and the merge is the cause.**
- Why: almost all of a run's cost is agent runs. One agent run costs $0.30 to $0.75, and the judge
  costs about $0.01 to $0.03 for each `llm` grader, so judging is about 10% of a case. Merging two
  cases saves one agent run each time the case runs, and adds no judge calls. A full run of all 30
  cases, 3 times each, cost about $37.
- What issue 58 showed: four merges held, so 30 cases became 26. `items-review-scenarios` and
  `items-review-whys` became `items-review-scenarios-whys`, `items-review-examples` and
  `items-review-handed-off` became `items-review-from-notes`, `items-write-bans` went into
  `items-write-limits`, and `items-review-tr-names-part` went into `terms-review-decisions`. Each
  passed 3 of 3 with the skill, as its old cases did. `items-write-limits` failed its one-organizer
  grader once in its first 3-run, then passed 3 of 3 in a rerun. Its rerun wrote the same
  requirement word for word, and all three judges passed it, so the failure was judge noise. Two
  parts were backed out, because the added content changed what the reviewer did, even though the
  planted problems looked separate:
  - Adding `items-review-unsettled`'s waitlists to `items-review-from-notes` made a real clash with
    the booking limit: should a waitlist booking count toward the 3? One reviewer called that clash
    something the notes didn't settle, and the judge counted it against the waitlist requirements.
    That grader passed 3 of 3 in the old case, and 2 of 3 merged.
  - Adding `terms-review-second-meaning`'s Free term and its "free of charge" requirement to
    `terms-review-word-uses` dropped the "free of charge" grader to 1 of 3 with the skill. The old
    case, run again on its own, passed 3 of 3. In the merged case, reviewers spent their attention
    on how the Free term met the other new requirement, which keeps cancelled bookings, and let
    "free of charge" through as a set phrase, or mentioned it only in passing.
- So: a case can hold several planted problems, but only when the content around each one doesn't
  raise new questions about the others. A new check is still tuned in a small case first. Before
  its planted problem and grader move into a bigger case, check whether the added content touches
  anything already there. Then run the merged case 3 times and compare each grader with the old
  case.
- Decided in: #58.
- Likely home: `TD`.

**Each docs eval case's setup copies the doc standards and the doc check script from their source
in the factory repo, not from a copy kept in each case.**
- Why: so the cases test the current standards.
- Decided in: #66. The script added in #67.
- Likely home: `TD`.

**Each docs eval case's repo gets the CLAUDE.md in `evals/docs/project-claude.md`. `claude plugin
eval` loads no CLAUDE.md, so `run-docs-evals.sh` also copies the same text into each case's
`append_system_prompt` before every run.**
- Why: the plugin eval docs say no CLAUDE.md loads, even one a case's setup wrote, and that
  `append_system_prompt` is how to give the agent project instructions. In a check run without it,
  the agent found the CLAUDE.md only because it showed up in an `ls`. Joe wanted one CLAUDE.md for
  all the cases, copied in when they run. The file isn't named `CLAUDE.md`, since Claude Code would
  load it in sessions working on the cases.
- Decided in: #67.
- Likely home: `TD`.

## Issue checker

**The issue checker checks that each requirement the issue asks for is clear enough to write as a
rule a test could check. If one isn't, its questions go in the issue and the issue goes to Needs
attention.**
- Why: clear requirements matter most for the work to come out as wanted. Catching a vague point
  before the implementer starts saves a wasted attempt. Some vague points only show up while
  writing, such as an edge case the issue never mentions, so the implementation loop still lists
  its choices on open points in the PR's description (FR-20).
- Decided in: #18, while planning #37. It goes into whichever issue builds the issue checker.
- Likely home: `FR`.

**The issue checker compares each spec item quoted in an issue with the item in the spec as it
stands. When one differs, or the item is gone, it flags it, since the spec may have changed after
the issue was written.**
- Why: a task issue quotes each spec item it cites, as it stood when the issue was written
  (`plugin/skills/standards/github.md`). A difference shows the work may no longer match what the issue
  asked for.
- Decided in: the interactive session that answered #85, #86 and #87.
- Likely home: `FR`.

**Whether the issue checker reads commit messages isn't decided yet.**
- Why it matters: a commit message can record a choice the owner already made. In the review of
  Dust Law's specs (nimbusscale/dust-law#17), the reviewer asked Joe to confirm choices he had made,
  such as SVG for tiles and no chat. The branch's commit messages recorded them, but the reviewer
  never read them. The quality reviewer is kept from commit messages on purpose (TR-21, TD-2),
  since the author's reasons sway a review. The lean is that the issue checker may read them. Which
  commit messages it would read, and why the quality reviewer's reason doesn't apply to it, wasn't
  said.
- Raised in: #21, closed once the specs settled that the workflow runs every review.
- Likely home: `TR`.

## The factory board

**One board holds the issues of every project the factory runs on, both the ones the factory works
and the ones the owner works by hand. The `factory` label on an issue says the factory may take it,
and the board's views split the two kinds of work. A project the factory doesn't run on has its own
board.**
- Why: Joe wants one place to see what's being worked on in every repo, "regardless of what repo is
  using the factory". He also wants each issue on one board, not two. Splitting the boards by the
  label puts issues on both, since a board's auto-add only ever adds an issue and never removes
  one, so adding the label later leaves the issue on the manual board too. On one board, adding or
  removing the label moves the issue between views, with the same status. A board has one Status
  field, so every project on it uses the factory's statuses. A project that needs other statuses
  can't share the board.
- Decided in: #8, in an interactive session that planned #8, #64, #115 and #134. The label's name
  is from #136.
- Likely home: `FR` for the board, which changes the functional spec's terms Board and Project; `AD`
  for one board across projects.

**The board's statuses are Backlog, Ready, In development, In review, Needs attention and Done. In
development means someone is working on the issue, the owner or the factory. The `factory` label
says which: on an issue in In development, it means a run is going. So the label comes off an issue
when the owner takes it back. Ready means the issue is ready to start. A new issue starts in
Backlog.**
- Why: Joe: "let's give this a shot and we can adjust as needed." Both kinds of work share the
  board, and the owner and a poller that starts runs (#10) both need to tell from the board whether
  a run is going. The label already says that, so a second status for the owner's own work would
  say it twice. Joe: "now we have two ways to show the factory is working on something, it has the
  label AND the status, but it should just be the label." The label also says who takes an issue,
  so Ready doesn't have to. A new issue starts in Backlog so the factory never starts on one the
  owner hasn't looked at: an issue only reaches Ready when the owner moves it.
- Left out: Triage, and Waiting to merge from the ideation doc. Joe is the only user, and Backlog
  plus the `agent-created` label cover new ideas. Waiting to merge is for a PR that passes every
  check but is held, such as when auto-merge is off. Until auto-merge exists, In review already
  means the PR waits on the owner. Either can be added when it's needed.
- Decided in: #136. Each status's description and color are in the comment on #137. In progress
  was dropped for In development alone in an interactive session on 2026-11-27.
- Likely home: the statuses in the factory's config (#137), with each status's description saying
  what it means.

**Every issue has one kind label: `task`, `bug`, `question` or `interactive`. An issue an agent
opens on its own also has `agent-created`. The `factory` label goes only on a `task` or a `bug`,
and a new issue doesn't get it. GitHub's default labels, `documentation` among them, are removed.**
- Why: nimbusscale is a personal account, so GitHub's issue types aren't available, and labels do
  that job. `task` and `bug` are separate because a bug has its own shape, which asks for what
  happened. The check when a run starts reads the kind label to know which headings the body must
  have. The label also lets the board show or count the bugs, which mostly come from the factory's
  own work. Joe asked why the two are separate, then chose to keep both. The `factory` label is off
  by default because, once a poller starts runs, an issue in Ready with the label starts a run
  without anyone asking. So the label means the owner chose to hand the issue over. A run never
  takes a question or an interactive issue. `documentation` is dropped because a doc-only change is
  a task. Joe chose the name `factory` over the ideation doc's `auto-develop`.
- Decided in: #136, from the proposal in #8.
- Likely home: the labels in the factory's config (#137); the kind labels' rules in
  `plugin/skills/standards/github.md`.

**When an issue's first child starts, its parent moves to In development, if the parent is in
Backlog or Ready. In a run, the factory's code moves it. In a person's session, the agent does.
After that, the owner moves the parent, and decides when it's done.**
- Why: Joe: "I definitely don't want to leave parents in backlog, because then they just get lost
  in the backlog." He wants to choose when a parent is done himself. It moves only from Backlog or
  Ready so it never overrides a status the owner set, such as a parent parked back in Backlog. No
  built-in workflow reacts to a child's status. A GitHub Action can't either, since the event for a
  board item changing exists only for boards an organization owns, and Actions can't trigger on it.
  So whatever moves the child moves the parent. A child the owner drags to In development on the
  board doesn't move its parent.
- Decided in: #136.
- Likely home: `FR` for the run; `plugin/skills/standards/github.md` for a person's session.

**The poller that starts runs (#10) only ever reads or changes issues that have the `factory`
label.**
- Why: Joe: "the poller should only ever interact with issues that have the factory tag." So it
  doesn't move the parent of a child the owner moved by hand, unless that parent has the label.
- Decided in: #136.
- Likely home: `FR`, with #10.

**Each repo on the board has a GitHub Action, `actions/add-to-project`, that adds its new issues to
the board. The Action uses a board token saved as a secret in the repo.**
- Why: nimbusscale is on GitHub Free, which allows one "Auto-add to project" workflow per board,
  and each one adds issues from one repo. GitHub's docs: "GitHub Free: 1". So on one board across
  repos, only one repo's issues would be added on their own. Upgrading to Pro allows 5, set by
  hand. The Action costs nothing and is committed code, which fits the board being set up by code.
- Still to check, when the init script is built: whether a fine-grained GitHub token can write to
  a board a personal account owns. A classic token with the `project` scope can, since the board
  code sets up the board with one.
- Decided in: #136.
- Likely home: `TD`, with the init script.

**A repo joins the factory by running the factory's init script in it. Init adds the factory's
plugin to the repo's `.claude/settings.json`, adds the Action and its secret, sets the repo's labels,
links the repo to the board, and sets up what the project contract needs. It doesn't add the repo's
issues to the board. It's idempotent: a part of the repo that's already set up is left as it is,
not set up again or failed on. It has a check mode, and adds its files through a PR.**
- Why: Joe: "That would include adding the plugin so that we don't end up having this dependency
  of the plugin needs to be added, then something else needs to be done." A Claude Code plugin
  can't run anything when it's installed, so the plugin alone can't set the repo up. A hook that
  checks at the start of every session would run in every session in every repo, for a step that
  happens once. Labels are set per repo, so a per-repo step is where they get set. `main` is
  protected, so init's files go in through a PR.
- Why init adds no issues: init is meant for a new repo. In a repo that already has issues, nobody
  knows what state they're in, and they may need other work before the factory can take them, such
  as being rewritten in the shapes the GitHub standards give. Sorting them out is done in an
  interactive session.
- Decided in: #136, which replaces #8's "the owner adds it to the board file and runs the board
  code again". #63, starting a project with slash commands, can call the same code. Adding no
  issues, and being idempotent, are from an interactive session that opened #147.
- Likely home: `FR` for joining the factory; `TD` for the script.
