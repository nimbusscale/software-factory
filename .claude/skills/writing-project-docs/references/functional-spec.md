# Functional spec

What a functional spec holds and keeps out, and how it changes. The questions in "Which doc a fact
goes in", in SKILL.md, decide which facts go in it.

Read by anyone changing what the app should do, and anyone writing evaluations. Kept current, and
changed in the same PR as the code or prompt change.

- **Also holds** the limits that always hold, each with its reason, such as "US only, because the
  payment provider only works there". It defines the terms a user would recognize, once each.
- **Keeps out** the prompt's or the code's level of detail. A requirement says what the user gets,
  not how a prompt words it. It also keeps out what's in the current release, which is a roadmap.
- **Never links out.** Prompts, code and other docs point to its IDs.
