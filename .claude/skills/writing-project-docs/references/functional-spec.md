# Functional spec

A functional spec says what the app should do, in the user's terms: every behavior and limit a
user would notice. This file says what else it holds and keeps out, and how it changes. The
questions in "Which doc a fact goes in", in SKILL.md, decide which facts go in it.

Read by anyone changing what the app should do, and anyone writing evaluations. Kept current, and
changed in the same PR as the code or prompt change.

- **Also holds** a Limits section, and defines the terms a user would recognize, once each.
- **Each limit is a requirement,** with its own ID, in the Limits section. A limit always holds.
  Write it as an absolute: what the app does, with "only", then what that rules out. A limit gets
  a Why under the same rule as any other requirement.

  > **FR-7.** The app shall take orders only from US addresses, not from other countries.
  >
  > *Why:* the payment provider only works in the US.

  Something the app doesn't do yet, but might later, isn't a limit. It goes in an issue, since the
  spec says what the app should do now, not what's planned.
- **Keeps out** the prompt's or the code's level of detail. A requirement says what the user gets,
  not how a prompt words it. It also keeps out what's in the current release, which is a roadmap.
- **Never links out.** Prompts, code and other docs point to its IDs.
