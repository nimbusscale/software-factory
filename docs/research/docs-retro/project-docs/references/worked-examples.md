# Worked examples

Real passages from an earlier project, a road trip planner with a coordinator agent and worker
agents. Each one is sorted with the questions in step 3 of the skill. They show the reasoning, so
use them for the pattern, not the details.

## Contents

- A table cell that held five rules
- A long bullet that mixed four kinds of text
- A rule with its reason missing
- A decision mixed with how it's carried out
- A history tail on a rule

## A table cell that held five rules

**Before:** one 175-word cell about comfortable driving hours. It gave the default, when the
planner asks, what a yes means, the daily maximum, and the recommended limit, in one paragraph.

**Sorted:** a user would notice every part, so all of it is functional requirements. One trigger
per requirement made eight of them, such as:

> **FR-12.** While the user hasn't said how long they like to drive, the planner shall not ask until
> the user can see a day's drive.
>
> *Why:* until the user sees a day's drive, they have nothing to judge the number by.
>
> *Scenario:* Given a new trip where the user hasn't mentioned driving, when the planner asks about
> the start and end points, then it doesn't ask about driving hours.

**What it shows:** most of the gain comes from splitting one cell into items that can each be cited
and tested. GEARS also forced the condition to the front. The original said "the agent doesn't ask
for it up front", with no condition at all. Only two of the eight needed a Why.

## A long bullet that mixed four kinds of text

**Before:** a 900-word bullet on today's date. It held rules that span files, rules for one file,
facts about an outside tool's own date line, history, and two other topics.

**Sorted:**

- Which date counts as today is something a user would notice, so it's a functional requirement:
  "Where the trip has a start place, the planner shall treat today as the date in that place's time
  zone."
- "Rules that use today's date take it from the last date line the app added" is a design decision.
  A new prompt rule could use the date from any prompt file, so there's no one place for a comment.
- "Every outside process the app starts runs in the date line's time zone" is a design decision.
  The process was started from two places, and a third could skip it.
- "UTC until the trip has a start place" is a comment. Every use of the trip's time zone goes
  through one function.
- Which messages get the date line is a comment where the line is built. The line's exact wording
  is in the prompt file. The history goes in commit messages. The two other topics go to the
  sections that own them.

**What it shows:** none of the four rules was a technical requirement. One was something the user
sees, and the rest were how the app meets it. About 900 words became about 150, and nothing was
lost.

## A rule with its reason missing

**Before:** "Services never call each other. A lookup that two services need is in a shared module
that each of them is given." No reason was written down anywhere.

**Sorted:**

> **TR-3.** The services shall each be usable on their own.
>
> **TD-14.** Services never call each other. Code two services need goes in a shared module each
> of them is given.
>
> *Why:* a service that calls another can't be used without it, and calls between services can end
> up in a circle.

A lint rule on imports between service files can enforce TD-14. Its comment cites TD-14, and TD-14
stays in the spec, since someone designing a change needs to see it before any code exists.

**What it shows:** writing the Why exposed the missing reason. Two of six decisions in that project
had a full reason written down.

## A decision mixed with how it's carried out

**Before:** "Each agent sees only its own tools. Tools are grouped into servers by job, and each
agent gets a list of exactly the tools it uses. Every agent runs from a definition that lists them,
the coordinator too, so it's sent only those."

**Sorted:** two decisions and a comment.

> **TD-2.** Each agent gets only the tools it uses.
>
> *Why:* a shorter list of tools means fewer choices for the agent. It's less likely to be
> confused, and it can't use a tool it doesn't need.

> **TD-3.** Tools are grouped into servers by job, not by vendor or by agent.
>
> *Why:* the server's name is part of every tool name the model sees. Naming by job keeps that name
> stable when a source changes.

The last sentence is about the one place the coordinator is started, so it's a comment there:

```ts
// Runs as a named agent so it's sent only the tools in its definition (TD-2).
// Without a named agent, the SDK sends the main agent every tool on every server.
```

## A history tail on a rule

**Before:** a rule, "each town on the path gets its own reason", followed by a tail of the kind
that project had often: when it was settled, in which issue, and the story of the session that
showed the rule was needed. In that session, two route sketches passed through the same town and
gave it the same reason.

**Sorted:** the rule stays. The date, issue and session go in the commit message. The evidence
stays as a general scenario, with no detail only that session had:

> *Scenario:* Given two route sketches that pass through the same town, when the planner explains
> each sketch, then each gives that town its own reason.

**What it shows:** a history tail usually mixes the rule, the evidence for it, and history. Deleting
the tail loses the evidence. Rewriting it as a scenario keeps the evidence, and the scenario can
become an evaluation case.
