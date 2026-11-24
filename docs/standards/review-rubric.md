# Review rubric

The rubric the quality reviewer labels each finding with. The label decides whether the finding is
fixed in the run, and it gives the finding its mark (FR-27). The rubric describes kinds of
findings, not real cases, so a finding can be labeled with it without pointing to one. It works for
any project. Where a label hangs on a fact about one project, such as who reads the app's text or
what its threat model is, the rubric points to the project's own docs.

The quality reviewer checks whether the code is fit for use: whether it works. Other reviewers
check the rest. The purpose reviewer checks whether the work meets each acceptance criterion in its
issue and follows the project's design. The doc reviewer checks whether the docs are right and the
code does what they say. So no label here covers the task, the docs or code comments, and the
quality reviewer doesn't judge the code against the docs. It reads the project's docs only for the
two facts F2 and F4 need: which agents the app runs, and its threat model.

## The labels

**Each finding gets one label: the first one in the table that fits.** A finding that would meet a
fix label but doesn't meet its condition gets the matching NF label. Other findings below the bar
get an N label. D1 drops the finding from the review, so it fits only when it clearly fits.
When you're unsure, treat it as not fitting, and keep going down the table.

| Label | Kind | Rule |
|---|---|---|
| V1 | Check | The label depends on a fact the reviewer can't check from the repo, and that fact decides whether it's a fix |
| D1 | Dropped | The claim about the code is false |
| F1 | Fix | The app does the wrong thing, crashes, or hangs, in normal use |
| F2 | Fix | Text the app's agents read says something false, in normal use |
| F3 | Fix | Data is lost or corrupted, in normal use |
| F4 | Fix | A security hole within the project's threat model |
| F5 | Fix | A test is wrong |
| F6 | Fix | The change adds behavior that no test checks |
| NF1 | Note | The app does the wrong thing, crashes, or hangs, but not in normal use |
| NF2 | Note | Text the app's agents read says something false, but not in normal use |
| NF3 | Note | Data is lost or corrupted, but not in normal use |
| NF4 | Note | A security hole outside the project's threat model |
| N1 | Note | Cleaner code |
| N2 | Note | A missing test, for behavior the change didn't add |
| N3 | Note | Text the app's agents read is unclear, or says something twice, or is an error message with the wrong reason for a failure |
| N4 | Note | Advice about code that isn't written yet |

F5 and F6 have no NF label. Normal use doesn't apply to them.

## Check first

**V1: the label depends on a fact the reviewer can't check from the repo, and that fact decides
whether the finding is a fix.** For example, how an outside service answers a request the code
hasn't sent before. The finding says what to check and how, such as the call to make. It's a
finding to check: the implementer doesn't get it, and the owner checks it once the run's PR is
open. V1 applies only when all of these hold:

- The fact is outside the repo, and nothing in the repo shows it.
- Settling it takes a real call or run that the reviewer can't make. If running code in the review
  copy would settle it, the reviewer runs it.
- The answer decides whether it's a fix. A finding that's a note either way gets its note label.

## Dropped

A dropped finding isn't sent to anyone in the run. It goes in the result's list of dropped
candidates, with the reason, so the owner can check the call.

- **D1: the claim about the code is false.** For example, the finding describes a failure that the
  code's own checks make impossible. The failure has to be impossible with the code as it stands.
  A claim that's true only for an unlikely input, such as a setting no one would choose, isn't
  false, and gets an NF label. Neither is one that only code not yet written would prevent.

Two kinds of finding the reviewer can't settle get their usual label, and the implementer can
decline them. One is about work that a code comment puts off to another issue. The reviewer can't
read other issues, so it can't check that one holds the work. The other is about code that does
what the project's docs ask, since the reviewer doesn't judge the code against the docs. The
implementer declines it by naming the issue or the doc item.

## Normal use

**Normal use is a use of the app that a real user could make, or a failure the code is meant to
handle.** An outside service that doesn't answer in time is a failure the code is meant to handle.
Where the app has its own agents, so is a plausible mistake by one of them: a slip models make in
practice, such as a wrong input name or the same ID twice. A rare case a real user could still
reach is normal use. Normal use doesn't cover an unlikely input, such as one nothing in the app has
a reason to produce, a setting no one would choose, or timing so narrow that two things running at
once have to line up in a particular order.

**Code that's written but not called yet is judged as if it were called** the way it's plainly
meant to be called.

## Fix labels

A finding is fixed in the run when its label is a fix label. That's "the bar".

**F1: the app does the wrong thing, crashes, or hangs, in normal use.** "Wrong" means different
from what the code says it does, such as in a function's name, its docstring or the message it
returns, or different from what a user would plainly expect.

**F2: text the app's agents read says something false, in normal use.** The app's agents are the
ones the project's docs say the app runs, such as models that call its tools. The agents that build
or review the code don't count. The text is tool descriptions, input schemas, what tools return,
and error messages. An agent acts on them, so false text leads to wrong actions. The test is
whether an agent that believes the text would do the wrong thing. For example, a tool description
promises something the tool doesn't do. False text is a specific claim an agent could act on as a
real answer, such as a wrong time, day or place. An error message that gives the wrong reason for a
failure is N3, not F2. For example, "access denied" when the input was the problem. The agent knows
the call failed, so it judges what to do next, such as trying again or asking the user.

Some apps run no agents of their own, such as a board game played in the browser. For them, F2, NF2
and N3 never fit. False text that a person reads is wrong behavior, judged under F1 like any
other.

**F3: data is lost or corrupted, in normal use.** Data the app saves is lost, changed when it
shouldn't be, or saved in a form that can't be loaded again. Lost means the information is gone,
such as deleted, overwritten, or dropped on save. Corrupted means what's saved is wrong, such as a
link to a record that no longer exists, so the app can't use it until the stored data is repaired.
A load that fails on stored data that's fine is F1, not F3.

**F4: a security hole within the project's threat model.** The project's docs set the threat
model: who might attack the app, and what they're after. When the docs set none, every security
hole is F4.

**F5: a test is wrong.** It can't catch a break in the very thing it targets. For example, it
checks only that a list isn't empty, so a list with the wrong items passes. Or it fails when the
code is right, such as a test that reads the real clock and breaks on a set date. A test that
checks the real thing but misses a case or a path is a missing test, not a wrong one. So is one
that checks the result but leaves one piece of it out, such as a check that compares every field
of a loaded object except its name. A wrong test gives false confidence, which is worse than
having no test.

**F6: the change adds behavior that no test checks.** For example, the change adds a rule that
refuses a booking longer than 14 days. If the check could be deleted and every test would still
pass, that's F6. A test checks the behavior only if it would fail when the behavior is removed or
wrong. A test that runs the new code but never looks at the result doesn't count. Behavior is
what the code does that a caller or a user could see, such as a result, an error or a saved
record. The change adds it when the code that does it is new, or when the change makes old code
do something new. A missing test for behavior that was there before the change is N2.

## Notes

Notes are below the bar. They aren't fixed in the run.

- **NF1 to NF3: like F1 to F3, but not in normal use.**
- **NF4: a security hole outside the project's threat model.** It's a note, so the owner sees it
  and decides.
- **N1: cleaner code.** That covers duplication, structure, speed, and code that can never run.
- **N2: a missing test, for behavior the change didn't add.** A test that exists but is wrong is
  F5.
- **N3: text the app's agents read is unclear, or says something twice, or is an error message
  with the wrong reason for a failure.**
- **N4: advice about code that isn't written yet.**

## From a label to a mark

Each finding the reviewer keeps gets the mark FR-27 asks for, from its label and from whether the
change caused the problem. The change caused it when the problem is in a line the change adds or
changes, or when the change makes an older problem worse or exposes it again. A problem in an
unchanged line that the change only fails to fix was there before the change.

| Label | The change caused it | It was there before |
|---|---|---|
| A fix label | Important finding | Pre-existing finding |
| A note label | Nit | Dropped |
| V1 | Finding to check | Finding to check |

A note about a problem that was there before is dropped, with "a note about older code" as its
reason.
