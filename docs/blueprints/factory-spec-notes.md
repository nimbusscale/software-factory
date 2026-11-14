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

**A name says what kind of thing it is, even when it's the only thing of its kind. When two names
share a word, the shared word is never used alone. When a new name shares a word with an existing
one, every bare use of the word is changed to the full name in the same change.**
- Why: in road-trip-agent, "brief" was fine while the trip brief was the only one. When the worker
  brief was added, every bare "brief" became unclear, even in sections about both. In Dust Law,
  "shape" and "catalog" read much better as "tile shape" and "tile catalog", and would break the
  same way if a second catalog were added.
- Decided in: #16 (being applied).
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

**A skill with steps in order gives a checklist the agent copies into its task list.**
- Why: a skipped step becomes visible, and an evaluation can see from the transcript which steps
  were done. The steps most likely to be skipped are searching first, following the change, and
  checking it.
- Decided in: #18.
- Likely home: `TD`, in code standards.
