# Technical spec

What a technical spec holds and keeps out, and how it changes. The questions in "Which doc a fact
goes in", in SKILL.md, decide which facts go in it.

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
