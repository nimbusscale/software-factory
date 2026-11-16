# Functional spec

A functional spec says what the app should do, in the user's terms: every behavior and limit a
user would notice. This file says what else it holds and keeps out, and how it changes. The
questions in "Which doc a fact goes in", in SKILL.md, decide which facts go in it.

Read by anyone changing what the app should do, and anyone writing evaluations. Kept current, and
changed in the same PR as the code or prompt change.

- **Also holds** the terms a user would recognize, defined once each.
- **Holds a limit only where it guides the build.** A limit is a requirement that says what the
  app does and where that stops. It always holds. Write it as an absolute: what the app does, with
  "only", then what that rules out. A limit gets a Why under the same rule as any other
  requirement.

  > **FR-7.** The shop shall take orders only from US addresses, not from other countries.
  >
  > *Why:* the payment provider only works in the US.

  The spec says what the app does, for the agents that build it. It isn't a list of the endless
  things the app doesn't do. So a limit goes in only when it passes both of these checks:

  1. **The source says what the app does, as well as where it stops.** A ban such as "no
     advertising" names only what's ruled out. It tells a builder nothing to build, so it stays
     out of the spec. "No matchmaking. Players join a game they've been invited to" passes, since
     its second sentence says what the app does. If you'd have to choose that part yourself, the
     source hasn't settled it, so don't write your guess as a rule.
  2. **Where it stops lets the builder design something simpler.** "Only one person signs in"
     means no accounts or roles to build. "Only the current version of each item" means no
     version history to store. "Email only for jobs the app runs itself" means no address books
     and no handling of spam. FR-7 means one country's addresses and taxes. If knowing where it
     stops simplifies no design, it isn't a limit. Write what's left as an ordinary requirement if
     it says something the app does, and otherwise leave it out. "Show analytics only as
     information, not with goals" simplifies nothing about how analytics are built, so it stays
     out. "Apply an import's changes only after the owner accepts them" becomes "When the owner
     accepts an import's changes, the app shall apply them."

  A limit is checked mostly by whether designs keep to it, not by a test. Don't rewrite one only
  because no test can prove it holds.

  "Only" alone doesn't make a limit. "Only the host can start a game" and "a booking can be made
  only up to 14 days ahead" simplify no design. They're ordinary requirements.
- **Puts each limit with what it bounds.** A limit goes in the section for the feature whose design
  it shapes, with that feature's other requirements. There's no separate section for limits. A
  limit on the whole app, such as FR-7, goes in the section closest to the app as a whole, such as
  one on who the app serves.
- **Describes the app as it is.** A limit the source states holds as written, whether the source
  calls it a limit, a non-goal or a trade-off, and whether it says "for now" or "never". A plan for
  later stays out. "Web only for the first version, with a phone app later" gives a limit, that
  the app runs only in a web browser. The phone app stays out.
- **Keeps out** the prompt's or the code's level of detail. A requirement says what the user gets,
  not how a prompt words it. It also keeps out what's in the current release, which is a roadmap.
- **Never links out.** Prompts, code and other docs point to its IDs.
