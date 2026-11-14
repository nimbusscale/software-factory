# Technical spec

A technical spec says what the system must achieve that a user wouldn't see (`TR`), and how it
meets its requirements: the decisions (`AD`, `TD`) that new code anywhere could follow or break.
This file says what else it holds and keeps out, how it changes, and how to write a decision. The questions in "Which doc a
fact goes in", in SKILL.md, decide which facts go in it.

Read by every implementer and reviewer, each reading the sections their task needs. Kept current,
and changed in the same PR as the code that changes one of its items. Split it only when different
tasks read different parts of it.

- **Decisions that every part of one kind must follow** go here, such as "every endpoint returns
  errors in one shape".
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

## Writing a decision

A decision is a one-line statement of the choice, in prose, and always has a Why. The Why says why
this option was chosen.

> **AD-1.** TypeScript for the whole app.
>
> *Why:* the back end and the UI share one definition of the data model. In two languages, every
> field change would be made twice.

- Use `AD` when the decision shapes the whole system, so a change would touch most of it, such as
  the language, the agent framework or the database. Use `TD` otherwise, such as which library
  checks outside data.
- A line that makes two choices is two decisions. "TypeScript, with React for the UI" is two.
- A decision can cite the requirement it meets, but it doesn't have to. There's no full map from
  every decision to a requirement.

Besides the Why, and the lines under any item in SKILL.md, a decision can have:

- **Examples:** a list of cases, for decisions about how code is written, where a list helps more
  than a scenario.
