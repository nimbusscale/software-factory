# Project docs

The standards for a project's functional spec, technical spec and blueprints: which doc a fact
goes in, and how to write any doc. How to write the items in a spec is in `specs.md`, and what a
blueprint holds is in `blueprints.md`, both in this folder. `templates/` holds a template for each
kind of doc.

The functional spec, the technical spec and blueprints are the input an agent turns into code.
Most of their readers are agents. They list a doc's headings, read one section, and act on it. So
every item has to be findable by its heading, make sense on its own, and say exactly what it
means. Every fact has one home, and other places point to it by ID. A second copy drifts, and an
agent can't tell which copy is right.

## Which doc a fact goes in

Ask these questions in order, and stop at the first yes.

1. **Is it about the past or the work in progress?** When something was decided, by whom, what
   was tried in a session, status. It goes in the commit message, never a doc.
2. **Is it about something other than what the app does and how it's built?** For example, how
   to do one task, a record of something tried and measured, or who the project is for. It
   doesn't go in a spec or a blueprint. Its home is somewhere else, such as a skill, a research
   doc or a README.
3. **Is it a plan for how to build something,** such as the order to build the parts in? It's a
   blueprint.
4. **Is it a quirk of an outside service,** such as an API that returns an empty list where you'd
   expect an error? It's a comment on the code that handles it, not a doc.
5. **Does a type, a lint rule or a setting already enforce it, and is breaking it a quick fix?**
   A file naming rule is one: when the check fails, you rename the file. The check is its
   documentation, so it isn't written in a doc. If its reason isn't obvious, a comment at the check
   gives it.
6. **Would a user notice if it changed?** It's a functional requirement (`FR`), in the user's
   terms. A user uses the app through its own screens, as it's meant to be used. What stops someone
   who tampers with the app, such as by changing what their browser sends, isn't something a user
   sees. It's a technical requirement. See "One item for each fact" in `specs.md` for how the two
   cite each other.
7. **Is it something the system must achieve that a user wouldn't see?** It's a technical
   requirement (`TR`), such as "backups meet a set recovery point". It may name a part an
   architecture decision created. For example, an architecture decision picks an outside service
   to sign users in, and a `TR` says the user IDs the app stores are its own, never change and are
   never reused, whatever IDs that service gives. Test it by asking whether it leaves the how open.
   If several ways of building it could each meet it, it's a requirement. If it picks one of those
   ways, it's a decision.
8. **Otherwise it's a decision about how the system is built:** an architecture decision, a design
   decision or a code standard. "Kinds of item" in `specs.md` says which. Then:
   - **Is there no other option?** A decision picks one way out of several. If the only reason
     anyone can give for it is that the rules or the domain work that way, nobody chose it, so
     it isn't a decision. Two kinds come up most. One says what a type holds, when the rules
     leave it nothing else to hold, such as a playing card that has a suit and a rank. The other
     follows from how a term or a rule defines something, such as that e4 and f5 lie on one
     diagonal, when a chess board's squares are named by a column letter and a row number.
     Its home is the code: the type, or the function that works it out. Until that code
     exists, it goes in a blueprint.
   - **Not made yet?** It goes in no doc until it's made. A decision that needs a spike to settle
     is one. **Rejected?** It goes nowhere. Name it in a code comment only if an agent would
     likely change the code back to it.
   - **Is there one place in the code that every case of it goes through, now and in the future?**
     Then it's a comment in that place. If new code could follow or break it without touching that
     place, it goes in the technical spec. "Every database write runs in a transaction" is a
     comment on the one function every write goes through. "Services never call each other" goes
     in the spec, since a new service could call another without touching any shared place.
   - **If a check also enforces it,** the check's comment cites the decision's ID. "Services never
     call each other" stays in the spec even when lint enforces it, since breaking it can mean
     redesigning a change, not a quick fix.

**Is its home a code comment?** These questions decide when a fact goes in a comment instead of a
spec. The project's guidance for code comments says how to write the comment. It may also find a
better home in the code, such as a clearer name or a type. Either way, the fact stays out of the
specs.

**Is the code not written yet?** When a fact's home is in code that doesn't exist yet, such as a
code comment, a check, a setting or a data file the code reads, the fact goes in a blueprint until
the code is written. The blueprint's retirement steps then move it to its home. Requirements, and
decisions the technical spec holds, go in the specs even before any code exists.

**Not settled by the source?** When part of a rule would have to be chosen by whoever writes it,
because the source leaves it open, that part goes in no doc until someone settles it. The source's
vague wording doesn't go in either. The parts the source does settle are still written. For
example, notes say the shop emails a customer when their order ships, "and again if it's running
late", and never say when an order counts as late. The rule for the shipping email is written.
When an order is late is a question for whoever owns the notes. A guess written as a rule looks
settled to every later reader, and nothing in the doc can mark it as a guess.

Words such as "may" and "could" often leave a part open. When they say what the system might do,
or what the people building it might choose, they name options, not a decision. Choosing among them
is a decision not made yet, so the "may" stays out of the doc, and so does the same option in other
words, such as "can". The same goes for a "such as" that names a choice still to make, as in "a
database such as PostgreSQL". Everything the source says that holds whichever option is chosen
still goes in, even when it's in the same sentence as the option. For example, notes say a phone
app shows a customer their past orders, keeps no other customer data, and "may keep a copy of the
orders on the phone so it works offline". The rules for showing past orders and keeping no other
data go in, since they hold either way. Whether the app keeps a copy is a decision not made yet.
A reworded sentence that holds either way has to still hold either way. "Keeps no other customer
data" holds whether or not the app keeps a copy of the orders. "Keeps only the orders on the phone"
doesn't, since it says the app keeps them there. A sentence that sounds settled can still depend on
the option. If it only makes sense when one option is chosen, it's part of the same open decision,
and stays out too. If the same notes say the order list "syncs to the phone", that only makes sense
if the app keeps a copy, so it stays out with the copy. Two uses of these words do settle
something. A "may" that says what a person is allowed to do is a rule: "a member may cancel a
booking before it starts" means the app lets them. A "such as" that gives an example of a rule is
an example, not an option.

## When a doc and the code disagree

The doc wins, unless CLAUDE.md says otherwise: the doc says what the system should do. The code is
changed to match, in the same change as any change to the doc.

## How to write any doc

Every doc opens with one line saying what kind of doc it is, so a reader knows which standards
apply. Then, for every sentence, in any doc:

- **Would a first-time reader do anything differently if it were gone?** If not, cut it.
- **Write the present only.** No dates, issue numbers, session names, "was X, now Y", or "the new
  check". Turn an incident into a general scenario, with no detail that only one session had. The
  evidence stays. The history goes.
- **Make each section stand on its own.** The reader may not have read the section before it.
- **Point, don't restate.** Cite another item's ID instead of repeating what it says.

### Names

- **One name for each thing.** Before naming a part of the app, a step or a state, search the docs
  for what they already call it, and use that exact name. A new name gets one home: a term in the
  Terms section, or the item that introduces it. A part an architecture decision creates, such as
  a worker, always gets a term, since other items name it without citing the decision. When names
  come as a set, such as the steps of a process, list every name in that home. Never give a rule
  for making names, such as "each step is named for what happens in it".
- **One meaning for each term.** A word defined in Terms means only that, everywhere in the docs.
  When another meaning is needed, use a different word. For example, if "order" is defined as a
  customer's purchase, write "sort", not "order", for how a list is arranged. This is about
  meaning, not spelling. A set phrase that no reader could take for the term is fine, such as "in
  order to".
- **A name says what kind of thing it is,** even when it's the only thing of its kind: "order
  status", not "status". A short name breaks when a second thing of that kind is added.
- **Never use a shared word alone, unless it's a term.** When two names share a word, such as
  "user account" and "admin account", always write the full name. "Account" alone could mean
  either. To use the bare word for every kind, as in "each account", define it as a term that says
  which kinds it covers: "Account. A user account or an admin account." The term lists the kinds.
  It doesn't say what the word means in general. Otherwise write the full names, or reword so the
  word isn't needed.
- **Cite where a word's meaning lives.** A word defined in a Terms section needs no citation. Any
  other word whose meaning lives in another item gets that item's ID or section ID the first time
  an item uses it. The test: could a reader of this item alone find what the word means?

### Citing IDs

To point to a group of items, cite the section ID. It means whatever the section holds now. To
point to specific items, list each ID. Never cite a range, such as "FR-12 to FR-18". A new item
placed among them gets the next free number, so a range can't say whether it's included.
