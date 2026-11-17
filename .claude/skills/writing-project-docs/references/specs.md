# Specs

How to write and change the functional spec and the technical spec: how to write each kind of
item, the Terms section and IDs, then what each spec holds and keeps out. Read all of it when
writing in either spec, creating one, or checking a change to one. The questions in "Which doc a
fact goes in", in SKILL.md, decide which spec a fact goes in, or whether it goes in a spec at all.

## Spec items

### Kinds of item

| Kind | Prefix | Doc |
|---|---|---|
| Functional requirement | `FR` | Functional spec |
| Technical requirement | `TR` | Technical spec |
| Architecture decision | `AD` | Technical spec |
| Design decision | `TD` | Technical spec |

A requirement says what the system must achieve. A decision says how the system meets its
requirements, and why this way:

| Requirement | A decision that meets it |
|---|---|
| When data enters the program, the data shall be checked against a defined schema, with no extra keys. | Outside data is parsed with a schema library where it enters the program. |
| The services shall each be usable on their own. | Services never call each other. Code two services need goes in a shared module each is given. |

How to write a decision, and whether it's an `AD` or a `TD`, is in "Writing a decision", under
"Technical spec" below.

### Requirements: GEARS

Every requirement uses this pattern. Every part but the last is optional:

> [Where \<fixed precondition\>] [While \<state at run time\>] [When \<trigger\>] The \<subject\>
> shall \<behavior\>.

- Where, While and When each appear at most once, in that order.
- The requirement starts with Where, While, When, or The.
- One behavior per requirement, so exactly one "shall". Two behaviors are two requirements.
- One trigger per requirement. A paragraph with several triggers becomes several requirements,
  unless the triggers are one fact. See "One item for each fact".
- The subject is a part of the system, or the code or data the rule is about. A plural subject
  keeps the "The" form: "The services shall each be usable on their own."
- State the condition a requirement depends on in its Where or While, even when it's always true
  today. A requirement written when a value was always empty breaks the day that value gets a
  default, unless "while it's empty" is in the requirement.
- When a requirement limits who may do something, say what's allowed, not what's refused, and cite
  the set it applies to. A list of what's refused misses whatever no one thought of. Check that
  every member of the set belongs, and that no other requirement makes an exception to it.

> **FR-12.** While the user hasn't set a time zone, the app shall show times in the time zone of
> the user's browser.

> **FR-30.** Where the account is a team account, the app shall ask an admin to approve each new
> member.

> **FR-41.** When a user deletes their account, the app shall keep their order history for seven
> years.
>
> *Why:* tax law requires order records for seven years.


### Lines under an item

Every paragraph under a requirement starts with one of the labels below. A plain paragraph never
goes there. If it holds a rule, the rule goes in the requirement's own text, or in a requirement of
its own. If it only shows a rule at work, such as a worked example from a source doc, cut it,
unless it passes the bar for a Scenario.

The one other thing that can go under a requirement is a table its own text points to, such as
"as this table shows". The table is part of the requirement.

- **Why:**
  - On a requirement, it works like a code comment: the reason behind the rule. Add one only when
    both of these hold:
    - the reason isn't clear from the rule itself, and
    - knowing it would change how someone applies or changes the rule.

    FR-41 needs one, since without it an agent might shorten the period to save storage. FR-12
    doesn't, since its reason is clear from the rule. "When an order ships, the app shall email the
    customer a tracking link", with the Why "customers want to know where their order is", fails
    the second test. Knowing it changes nothing.
  - A Why can keep a rule that looks unneeded from being deleted, such as a rule that never fires
    under the other rules:

    > **FR-52.** While an order's total is zero, the app shall skip the payment step.
    >
    > *Why:* the payment provider rejects a charge of zero, so a free item or a full discount would
    > otherwise block the order.
  - A Why never states a fact about the rest of the system today, such as "no check uses this yet".
    That kind of fact goes stale when other items change. A condition goes in the Where or While.
- **Scenario:** Given, when, then. Add one only when both of these hold:
  - the result comes from several requirements working together, and
  - a reader of one of those requirements and the Terms would likely get it wrong.

  The reader knows only what the docs say, not how similar products work. A scenario must be able
  to happen under the other requirements. It never holds a rule of its own: a rule found only in a
  scenario is a missing requirement. A vague or untestable requirement is fixed by rewriting it,
  never by adding a scenario. A limit is the exception to "untestable": see "Holds a limit only
  where it guides the build", under "Functional spec" below. A requirement can still need both.

  > **FR-60.** When an order's total is over $50, the app shall ship it for free.
  >
  > *Scenario:* Given a $55 order and a $10 discount code, when the customer checks out, then
  > shipping is charged, since the total is now $45.
- **Accepted gap:** a gap the item knowingly leaves, and the reason it's accepted. Without the
  reason, a reviewer can't judge whether the gap still fits.


### One item for each fact

Two items are the same fact if changing one would force a change to the other. Merge them into one
item. If each would change for a different reason, they're two facts, and both stay, even when
they limit the same action. Test with a change that has a reason of its own, one someone could
really ask for. Nearly any two items could change apart for no reason, and that doesn't make them
two facts.

> **FR-70.** The app shall accept changes to an account's shipping address only from the account's
> owner.
>
> **FR-71.** When a shipping address is saved, the app shall accept it only if it's in a country the
> shop ships to.

Both limit changing a shipping address, but they're two facts. If an account could have several
users, FR-70 would change and FR-71 wouldn't. If the shop shipped to more countries, FR-71 would
change and FR-70 wouldn't.

The same test applies to the triggers of one requirement, such as "When A or B". Triggers that are
two facts become two requirements. "When a customer places an order or changes their email
address, the app shall email them a confirmation" is two facts: the order email could gain a
delivery date without the other one changing.

Triggers that are one fact stay one requirement. When they list the members of a set another
requirement defines, cite that requirement in place of the list. Otherwise the list has to be
updated by hand each time the set changes.

> **FR-72.** Where a product is discontinued or not yet launched, the shop shall show it only to
> staff.
>
> **FR-73.** When a customer asks for a product that FR-72 keeps from them, the shop shall answer
> "not found".

Written as "When a customer asks for a discontinued product or a product not yet launched", FR-73
would repeat FR-72's list. A third kind of hidden product would then have to be added in both.

The same test applies across the two specs. A rule a user sees often has a technical half that
stops someone who tampers with the app from getting around it. The technical half cites each
requirement it protects, instead of repeating it:

> **FR-80.** The app shall show each customer only their own orders.
>
> **TR-4.** The server shall send each customer's browser only the orders that FR-80 lets that
> customer see.

If TR-4 repeated FR-80's rule, letting a customer see a partner's orders would mean changing both.
Citing FR-80 makes them two facts. FR-80 changes when who may see an order changes. TR-4 changes
only if the app trusts each browser to hide what it's sent. The citation also shows whoever changes
FR-80 that TR-4 depends on it. Cite a section in place of the requirements only when the section
holds every one the technical half protects.

### The Terms section

A term is a word and its definition, written once, in the spec's Terms section. The definition says
what the thing is. It never states a rule a requirement holds, such as a count, a limit, or when
something finishes. A rule stated in two places can change in one and not the other.

To test each part of a definition, ask: if a requirement changed, would this part have to change
too? If so, it states that requirement's rule. Cut it. If the word's meaning depends on the rule,
cite the requirement in its place, as below.

- **A rule:** "Admin. The one person who runs a shop's account," when FR-5 lets each shop have
  only one admin. If FR-5 allowed two admins, "the one" would be wrong. Write "Admin. The person
  who runs a shop's account."
- **A definition:** "Bundle. Two or more products sold together as one item." No requirement says
  how many products a bundle holds. "Two or more" is part of what a bundle is, so no requirement
  changing could make it wrong.

A count or a time can be either. What decides it is whether a requirement holds it. If a part of
a definition is something the app must do or check, and no requirement holds it, it's a missing
requirement. Write the requirement, then cut the part from the definition.

A term cites something in only two cases. Otherwise it's a plain definition, with no citation.

- **Its meaning depends on a requirement's rule.** It cites that requirement. For example,
  "Overdue. A loan past its due date (FR-12)," where FR-12 says when a loan is due.
- **A section holds the rules for the thing it names.** It may cite that section, such as
  "Refund. Money returned to a customer for an order (F-SEC-6)."

A citation that only says where the thing comes from adds nothing. Leave it out. That includes a
requirement that creates the thing, or one that decides who fills a role. For example,
"Borrower. The member a loan is for" cites nothing, even when requirements decide whose loan it
is. To test a citation, cover it and read the term. If the word's meaning is still clear, the
citation goes. Overdue keeps FR-12, since without it nothing says when a loan is due.

### IDs

- **Item IDs** are a prefix and a plain number, such as `FR-42`, `TR-7`, `AD-2` or `TD-3`. The
  number says nothing about where the item sits, so it never goes stale when the item moves. Don't
  put a topic in an ID, such as `TD-CS-4`. It goes wrong the day the item moves to another
  section.
- **Section IDs** have a different shape, so they can't be mistaken for item IDs: `F-SEC-3` in the
  functional spec and `T-SEC-3` in the technical spec. They go in the heading:
  `## T-SEC-4. Outside services`.
- **A new ID** is one more than the highest number with that prefix in the doc:

  ```bash
  grep -oE '\bFR-[0-9]+' docs/functional-spec.md | grep -oE '[0-9]+$' | sort -n | tail -1
  ```

  An ID that was retired and deleted can come back this way. That's accepted, since a retired ID
  shouldn't be cited anywhere. Use only the doc's current text, not its git history.

## Functional spec

A functional spec says what the app should do, in the user's terms: every behavior and limit a
user would notice. This section says what else it holds and keeps out, and how it changes.

Read by anyone changing what the app should do, and anyone writing evaluations. Kept current, and
changed along with the code or prompt.

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
     source hasn't settled it. Follow "Not settled by the source?" in SKILL.md.
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
  only up to 14 days ahead" simplify no design. They're ordinary requirements. An ordinary
  requirement can still be written with "only", then what it rules out, when that's the clearest
  way to say it. Whether a rule counts as a limit decides only whether it goes in the spec, never
  how it's written or where it sits.
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

## Technical spec

A technical spec says what the system must achieve that a user wouldn't see (`TR`), and how it
meets its requirements: the decisions (`AD`, `TD`) that new code anywhere could follow or break.
This section says what else it holds and keeps out, how it changes, and how to write a decision.

Read by every implementer and reviewer, each reading the sections their task needs. Kept current,
and changed along with the code that changes one of its items. Split it only when different
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
- **A list of tests or checks the app must pass isn't written as a list.** This includes a goal for
  the whole app, such as "two people can play a game to the end." Every requirement has at least
  one test, so an entry the requirements already cover adds nothing. An entry that tests something
  no requirement states is a missing requirement, so write the requirement. A rule for how all
  tests are written, such as "a fix comes with a test that fails without it", is a code standard.
- **Keeps out** process, statuses and merge rules. Those are in the workflow's code and its role
  prompts.

### Writing a decision

A decision is a one-line statement of the choice, in prose, and always has a Why. The Why says why
this option was chosen.

**No reason in the source?** When the source gives no reason for a decision, write the decision
with no Why. Never write a reason the source doesn't give, however likely it seems. Ask for the
reason in your report: quote the decision, and suggest a reason if you have one. The check script
flags the missing Why until the reason is known.

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

Besides the Why, and the lines in "Lines under an item" above, a decision can have:

- **Examples:** a list of cases, for decisions about how code is written, where a list helps more
  than a scenario.
