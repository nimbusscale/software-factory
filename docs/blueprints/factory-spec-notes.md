# Factory spec notes

A blueprint, written to build from before the factory's functional and technical specs exist. It
collects decisions made while building the factory, each with its reason, so the reasons aren't
lost before the specs are written. When the specs are written, each entry is sorted into them with
the `writing-project-docs` skill, and this file is retired.

Each entry gives the rule, why, where it was decided, and a guess at its home: `FR`, `TR` or a
decision (`AD`, `TD`). The guess is only a starting point. "Why unknown" means no reason was given.

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

**When a doc and the code disagree, the doc wins, unless CLAUDE.md says otherwise. If the agent
can't fix the code within its task, it leaves both and reports the disagreement in the PR
description or its final report, naming the item ID and the code.**
- Why: the docs say what the system should do. An agent with no default does whatever it thinks
  best. A headless agent can't ask the user, and opening issues is outside writing docs, so the
  report goes in output the agent already produces.
- Decided in: #18, while splitting the skill.
- Likely home: `FR`.

**Every doc opens with one line saying what kind of doc it is. In the specs, the line also gives
the rules a writer needs, such as GEARS and no links out.**
- Why: an agent or a person may change a doc without the skill loaded. The line is how they learn
  what the doc is and how it's written.
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

**A skill doesn't tell the agent to take outside actions, such as opening or commenting on an issue
or a PR. It says what goes in the doc.**
- Why: the same skill runs for a writer, a reviewer and an implementer, and in interactive sessions
  where the owner talks through how to handle things. The factory may not let a given agent take
  those actions. The skill still mentions PRs in places. Joe will deal with those separately.
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

**A skill's examples come from a different domain than its evaluations.**
- Why: with an organizer example in the skill, every writer copied its wording into the spec, so a
  pass showed only that it could copy. With a borrower example, the writers' wording varied and
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
least one test, and counts as met when its tests pass. An issue's acceptance criteria name the
requirements the issue must meet, which tells the workflow which tests must pass. They don't define
the tests. A test an issue needs may not exist yet, and then it's written as part of the work.**
- Why: each requirement should be testable, or easy to see how to test, from its own text. If it
  isn't, the requirement needs refining. Tracing tests to scenarios made scenarios carry rules and
  hide vague requirements. An earlier idea, in the docs retro findings, was that scenarios become
  evaluation cases. This replaces it.
- Decided in: #12, in discussion with the owner.
- Open: how a missing test gets written, and by whom, when an issue needs it.
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

**The skill doesn't say technical requirements are rare.**
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
- Likely home: unclear. It may only be how the skill is tested.

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

## Skills

**SKILL.md holds what every task needs, and rules shared by more than one kind of doc. A rule used
by one kind of doc goes in that doc's reference file. Every reference file is linked directly from
SKILL.md, with no file linking on to another.**
- Why: Anthropic and agentskills.io recommend a SKILL.md under 500 lines and 5,000 tokens. Files it
  links to cost nothing until read. An agent may only partly read a file it reaches through another
  file.
- Decided in: #18.
- Likely home: `TD`, in code standards.

**A skill gives the standard a doc must meet and trusts the model on method. The docs skill has no
step-by-step method for turning existing docs into specs. It only checks that nothing in the source
was dropped, whatever the source is.**
- Why: Anthropic's guidance says to assume Claude is capable. The Dust Law conversion went fine
  without a method. Facts come from many sources, such as source docs, issues or a long spoken
  explanation, and the same standard and check fit them all. Guidance gets added only if the Dust
  Law and Facet runs show it's needed.
- Decided in: #20.
- Likely home: `TD`, in code standards.

**The docs skill doesn't say what happens to source docs after they're turned into specs. The
task's prompt says it, such as "delete the foundation docs".**
- Why: it won't always be the same. Some projects may keep their source docs.
- Decided in: #18, after the second Dust Law run.
- Likely home: `TD`, in code standards.

**A skill keeps a reason only when, without it, an agent would likely act differently. Other
reasons go in the specs.**
- Why: a skill's body is read every time it's used, so a sentence that doesn't change what the
  agent does is clutter.
- Decided in: #18, about the ID section.
- Likely home: `TD`, in code standards.

**Skill names use the gerund form, such as `writing-project-docs`, and don't name the factory.**
- Why: Anthropic recommends the gerund form. The model sees the name next to the description, and
  the name is the command a person types. A project using the skill doesn't need to know where it
  came from.
- Decided in: #18.
- Likely home: `TD`, in code standards.

**Skill descriptions are written in the third person, such as "Writes and reviews…".**
- Why: Anthropic's guidance says to always write descriptions in the third person.
- Decided in: #18.
- Likely home: `TD`, in code standards.

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
- Likely home: `TD`, in code standards.

**A skill with steps in order, or a list of checks, gives a checklist the agent copies into its
task list. A file an agent may read on its own, such as the review file, has its own checklist.**
- Why: a skipped step becomes visible, and an evaluation can see from the transcript which steps
  were done. The steps most likely to be skipped are searching first, following the change, and
  checking it. Within checking, the reading checks are skipped most easily, since a script can't
  do them. A reviewer reads only the review file, so it can't use another file's checklist.
- Decided in: #18 and #22.
- Likely home: `TD`, in code standards.

**An agent checking its own change fixes what it finds. A reviewer checking someone else's change
edits nothing and reports what it finds.**
- Why: in the factory, the implementer reviews its own work so it can fix problems before the work
  goes to a reviewer. The reviewer's findings go back to the implementer, who makes the fixes. So a
  reviewer never changes code or docs.
- Decided in: #33.
- Likely home: `FR`.

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
  only by the general rules in SKILL.md, and can flag an item that follows its doc's rules as a
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

**When the source leaves part of a rule open, the writer writes no rule for that part, and doesn't
copy the vague wording either. It raises a question in its report: the source text, what's
unclear, and a suggested answer. It still writes the parts the source settles. The agent's prompt
says what happens to the question: in an interactive session it's asked, an implementer stops and
the issue goes to Needs attention, and a test run puts it in the report.**
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
  the last place to catch one. The reviewer only sees a change where the writer wrote a rule, since
  an implementer that raises a question stops before review. Without the source there's nothing to
  compare against: judging from the spec alone can't tell a guess from a choice the owner made.
  Saying the check was skipped keeps a clean report from looking like a pass.
- Decided in: #37.
- Likely home: `FR`.

**A skill says what a finding contains: where it is, what's wrong, a suggested rewrite and why it
fixes it. The task's prompt says how findings are delivered. With no instructions, they go in the
reply.**
- Why: the same skill runs in an interactive session, in the factory loop and in evaluations, and
  each needs a different format. The loop will likely need JSON or a tool call. No one skill
  defines how an agent works, since an agent loads several skills.
- Decided in: #33.
- Likely home: `TD`.

**The doc check script needs a git repo and a base branch. Checking docs outside a git repo isn't
supported. It writes no files.**
- Why: nearly every run happens in a repo, so supporting docs outside one isn't needed. It only
  reads files and prints what it finds, so it has no reason to write, and an evaluation's sandbox
  doesn't let it write.
- Decided in: #33.
- Likely home: `TD`.

**The docs skill is used in three ways, and it doesn't say which one it's in. The implementer and
reviewer use it in the implementation loop, where the specs already exist and each change adds to
them. The doc curator uses it to compare the docs and the code as a whole and raise issues for
what's out of step. A person uses it in an interactive session, which is where specs are first
written and often refined before an issue goes into the factory. Where the three need different
behavior, the skill sets a default and the agent's prompt says what happens next.**
- Why: Joe expects all three uses. A rule written for one can be wrong for another. The uncited-ID
  signal is noise on a first draft but useful in the loop. A vague point in the source should be
  asked about in an interactive session, but should stop an implementer that has no one to ask.
- Decided in: #18, while planning #36, #37 and #43.
- Likely home: `TD`, in code standards.

**By default, the doc check script flags a requirement that nothing cites only if something cited
it on the base branch. With `--uncited`, it flags every requirement that nothing cites.**
- Why: in the implementation loop, a requirement that loses its last citation is the useful
  signal. A requirement written before the code that meets it is normal. On a first draft nothing
  is cited, so the old check flagged nearly every requirement: 88 of 91 in the third Dust Law run.
  That buried any other signal. The doc curator still needs the full list, so it uses `--uncited`.
- Decided in: #43.
- Likely home: `TD`.

**The docs skill doesn't assume the agent can reach GitHub. It talks about the task and the agent's
report, not a PR or issues.**
- Why: Joe's working assumption is that the workflow brokers what each agent sees, and agents get
  different access. A reviewer in the loop gets only what the workflow gives it. The doc curator
  may be allowed to read PRs, to see what changed since its last run.
- Decided in: #18, while planning #36.
- Likely home: `TD`, in code standards.

## Evaluations

**A skill's evaluations live in an `evals/` folder inside the skill, one folder per case, and run
with `claude plugin eval`.**
- Why: the skill-creator skill on its own leaves the orchestration to us, including setting the
  judge model and much else we'd have to build. `claude plugin eval` has that orchestration built
  in.
- Decided in: #24.
- Likely home: `TD`.

**A grader checks that a reply has the information needed, in any words. It never checks the
reply's headings or layout.**
- Why: a model can't be failed for not following an output shape. If the shape matters, the task
  should use structured output.
- Decided in: #33.
- Likely home: `TD`.

**Evaluations run with the skill only. A case also runs without the skill when it's new or changes
a lot.**
- Why: an agent can't guess the project's standards, such as its IDs and prose, without the skill,
  so running without it mostly shows that. What it does show is whether a case depends on the
  skill.
- Decided in: #33.
- Likely home: `TD`.

**A case that passes without the skill moves to a second folder, `evals-no-skill/`, next to
`evals/`. A plain run runs only `evals/`. The second folder runs when an agent's model or effort
changes, after which every case is sorted again, and in a full run after a batch of skill
changes.**
- Why: a case that passes without the skill shows no value from the skill, and runs add up. Joe:
  the work and runs for one issue took about 6% of his allocation. But the case still records a
  behavior we cared about. If the writer moves from Opus to Sonnet, or from high effort to medium,
  it may start to fail, and the folder is a checklist for that change. A folder, not a tag,
  because the runner has no way to leave a tagged case out by default.
- Open: Joe may change how full runs are done, because of their cost.
- Decided in: #38.
- Likely home: `TD`.

**The judge model is Sonnet. The agent under test runs on Opus for now.**
- Why: Anthropic's guide for `claude plugin eval init` recommends a Sonnet-class judge. The factory
  is made to work on Opus first. Cheaper models for some agents come after.
- Decided in: #27 and #33.
- Likely home: `TD`.

**Each rule a skill's review checks gets a reviewer case. A rule gets a writer case only when real
runs show writers keep breaking it, or when no review check covers it. A writer case starts from
the real input that led to the mistake, cut down, when there is one.**
- Why: the reviewer is the last check before a problem gets through, and a writer checking its own
  work runs the same review checks, so one reviewer case covers both. A reviewer case can plant
  exactly the problem to find. A writer case can only hope the writer makes the mistake. Each case
  costs runs, so cases are added only where they're needed. A writer case is still worth it when
  the reviewer keeps catching the same mistake, since each catch costs another round. A real
  mistake makes a better test than an invented one.
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

**The evals README records how each case did in its last run without the skill, and the commit it
ran on. It records no other results.**
- Why: that's the baseline. It says which cases depend on the skill, so later runs can leave out
  the ones that don't. Other results change with every run, and they go in the PR and the issue.
- Decided in: #27.
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
passes, the whole group runs 3 times each, to catch anything a skill change broke. A case that has
passed both with and without the skill is left out, even after the skill changes. Before a 3-run
pass, each case runs once. A case whose setup was fixed runs once more, and goes into a 3-run pass
only when its result has nothing to do with the setup. A case gets up to 3 single runs, with fixes
to the skill, the case or its graders in between, before its 3-run pass.**
- Why: a single run can pass by luck. `review-roles-review-clean` passed one run, then failed 3 out of 3. A
  case that has passed both ways gives no reason to run it again, and each run costs tokens. The
  single run catches a broken setup before the bigger run spends three times as much. If a setup
  fix doesn't work, every run in a 3-run pass is wasted, so each setup has to be right first. The 3
  single runs give room to find and fix problems before the bigger run. Joe: "3 is just a nice
  limit that you typically are able to work it within to get it to pass. So I just needed some
  number. 3 seemed reasonable, and it's worked out so far."
- Decided in: #33 and #41.
- Likely home: `TD`.

**A doc reviewer checks the docs and whether the code does what they say. It doesn't mention a
code bug that leaves the docs right.**
- Why: code bugs aren't a doc reviewer's concern.
- Decided in: #33.
- Likely home: `FR`.

## Issue checker

**The issue checker checks that each requirement the issue asks for is clear enough to write as a
rule a test could check. If one isn't, its questions go in the issue and the issue goes to Needs
attention. An implementer that finds a vague point while writing a spec stops the same way.**
- Why: clear requirements matter most for the work to come out as wanted. Catching a vague point
  before the implementer starts saves a wasted attempt. Some vague points only show up while
  writing, such as an edge case the issue never mentions, so the implementer still needs to stop.
- Decided in: #18, while planning #37. It goes into whichever issue builds the issue checker.
- Likely home: `FR`.
