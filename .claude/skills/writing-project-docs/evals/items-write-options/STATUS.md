# Status

Last run: 2026-11-18, 3 runs with the skill, after `SKILL.md` said a sentence that only makes
sense when one option is chosen is part of the same question. 2 of 3 passed. It hasn't been run
without the skill yet.

| Run | 01 no decision | 02 decision | 03 asks |
|---|---|---|---|
| 1 | Pass | Pass | Pass |
| 2 | Pass, 2 of 3 votes | Pass | Pass |
| 3 | Fail | Pass | Pass |

No spec wrote "The engine is shared code". Runs 1 and 2 said in their reports that they left it out
because it only holds if the client uses the engine.

## Known failures

- **The writer drops "of its own".** Run 3's spec has "AD-2. All the code that decides whether an
  action is allowed, and what game state it leads to, is in the engine" and "TD-2. The client uses
  the logic that decides whether an action is allowed only to show a player their options." Read
  together, they say the client uses the engine. Grader 01 failed it 3 of 3. Run 2 has the same
  pair in other words, and one of its three judges failed it. The judge's reasons aren't saved, so
  this is a guess, but no other item in either spec touches the client.
- **The writer leaves out the client rule.** In the earlier 3-run on 2026-11-18, one spec had no
  item saying the client holds no rules logic of its own beyond what it needs to show options.
- **The writer copies the "may" in other words.** In the same earlier 3-run, AD-5 said "The engine
  is shared code, which the server and the client can each import." `SKILL.md` now names this.

## Not tested here

Whether the client rule is an `AD` or a `TD`. The skill's rule is that an `AD` shapes the whole
system, such as the parts the code is split into. It doesn't clearly cover a rule about what one
part may do, so either is defensible. That gap could be its own issue.
