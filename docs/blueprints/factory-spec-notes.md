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
desktop browser, not on phones or tablets." Something not built yet isn't a limit. It's an issue.**
- Why: "shall run in a desktop browser" doesn't rule out running elsewhere. Saying what it does
  only, then what that rules out, is clearer. An ID lets a doc or test cite one limit. The spec says
  what the app should do now, not a roadmap.
- Decided in: #5.
- Likely home: `FR`.

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

**A skill's examples come from a different domain than its evaluations.**
- Why: with an organizer example in the skill, every writer copied its wording into the spec, so a
  pass showed only that it could copy. With a borrower example, the writers' wording varied and
  they still passed.
- Decided in: #27.
- Likely home: `TD`.

**A word defined in Terms means only that, everywhere in the docs. Another meaning gets a
different word. The review greps for each term and its other forms to check every use.**
- Why: in the second Dust Law run, Terms defined "Turn" as one player's go, and a requirement
  then used "turn" to mean rotating a tile. A reader who checks Terms gets the wrong meaning. The
  skill said each thing gets one name but not that each name keeps one meaning, so nothing
  stopped the writer. The reviewer caught it only by chance.
- Decided in: #25.
- Likely home: `TD`.

**A name says what kind of thing it is, even when it's the only thing of its kind. When two names
share a word, the shared word is never used alone. When a new name shares a word with an existing
one, every bare use of the word is changed to the full name in the same change.**
- Why: in road-trip-agent, "brief" was fine while the trip brief was the only one. When the worker
  brief was added, every bare "brief" became unclear, even in sections about both. In Dust Law,
  "shape" and "catalog" read much better as "tile shape" and "tile catalog", and would break the
  same way if a second catalog were added.
- Decided in: #16.
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
a lot. A case that passes without the skill stays as a check against regressions.**
- Why: an agent can't guess the project's standards, such as its IDs and prose, without the skill,
  so running without it mostly shows that. What it does show is whether a case depends on the
  skill. A case that passes without the skill still catches a later skill change that breaks it.
- Decided in: #33.
- Likely home: `TD`.

**The judge model is Sonnet. The agent under test runs on Opus for now.**
- Why: Anthropic's guide for `claude plugin eval init` recommends a Sonnet-class judge. The factory
  is made to work on Opus first. Cheaper models for some agents come after.
- Decided in: #27 and #33.
- Likely home: `TD`.

**Each case has a role tag, `write` or `review`, and a group tag, so a group runs together.**
- Why: related cases run together without naming each one, the way a test class does.
- Decided in: #33.
- Likely home: `TD`.

**A case's planted problems are ones the doc check script flags.**
- Why: the cases test what the agent does with a problem, not whether it can find one.
- Decided in: #33.
- Likely home: `TD`.

**A failing case is run on its own until it passes 3 runs out of 3. When every case in a group
passes, the whole group runs 3 times each, to catch anything a skill change broke. A case that has
passed both with and without the skill is left out, even after the skill changes. Before a 3-run
pass, each case runs once. A case whose setup was fixed runs once more, and goes into a 3-run pass
only when its result has nothing to do with the setup.**
- Why: a single run can pass by luck. `review-clean` passed one run, then failed 3 out of 3. A
  case that has passed both ways gives no reason to run it again, and each run costs tokens. The
  single run catches a broken setup before the bigger run spends three times as much. If a setup
  fix doesn't work, every run in a 3-run pass is wasted, so each setup has to be right first.
- Decided in: #33.
- Likely home: `TD`.

**A doc reviewer checks the docs and whether the code does what they say. It doesn't mention a
code bug that leaves the docs right.**
- Why: code bugs aren't a doc reviewer's concern.
- Decided in: #33.
- Likely home: `FR`.
