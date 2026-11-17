# Status

Last run: 2026-11-17, 1 run with the skill, after the two fixes below. It passed. Before the fixes,
3 runs passed 2 of 3, and every run before commit `0a12ffe` passed, 7 of 7.

## Fixes made, and what to watch for

**FR-4 now says "only".** In a smoke run after commit `aa5f5a6`, a reviewer said FR-4's scenario
holds a rule FR-4 doesn't state. FR-4 said the app "shall let" the organizer check in while the
time slot runs, but never that it refuses at other times, and the scenario's result is "then they
can't". So FR-4 became: "The app shall let a booking's organizer check in to it only while its
time slot has started and hasn't ended, and the booking hasn't been cancelled."

**Grader 04 allows a move that comes from a different problem.** One run suggested splitting FR-4
into who may check in and when, with the 14:20 scenario moving under the new requirement. Grader 04
failed it for "moving" the scenario, even though the reply said the scenario earns its place.

**Watch for:** the new FR-4 wording draws its own comments. Reviewers say it breaks GEARS, since the
condition comes after "only" instead of in a While, and that "only" can mean "only the organizer"
or "only during this window". Two of four runs since the fix also suggested splitting FR-4 into who
and when. No grader checks these, so the case still passes, but they're noise this case planted by
accident, not a skill problem. If they keep showing up, reword FR-4 with the While first and the
limit at the end:

> **FR-4.** While a booking's time slot has started and hasn't ended, and the booking hasn't been
> cancelled, the app shall let its organizer check in to it, and not at other times.
