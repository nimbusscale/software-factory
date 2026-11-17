# Status

Last run: 2026-11-17, 4 single runs with the skill. None passed. Each scored 0.67, failing one
grader. It hasn't been run without the skill yet.

| Run | 01 no decision | 02 AD | 03 asks | What changed before it |
|---|---|---|---|---|
| 1 | Fail | Pass | Pass | Nothing |
| 2 | Pass | Fail | Pass | Grader 01 rewritten to name the items that are fine |
| 3 | Fail | Pass | Pass | SKILL.md: write what holds whichever option is chosen |
| 4 | Pass | Fail | Pass | Nothing |

## Known failures

- **Grader 01 fails, though the spec looks right.** In runs 1 and 3, no item says the client uses
  the engine. Given each spec and the grader directly, Sonnet passed both, naming the client
  rule as the closest item. The runner doesn't save the judge's reasons, and `--verbose` doesn't
  log them, so why its judge failed them is unknown.
- **The client rule isn't always an AD.** In run 2 the writer left it out, treating the whole
  passage as open. In run 4 it wrote it as a TD citing FR-2: "The client applies game rules only
  to show the player their options, such as the spaces FR-2 highlights."
- **The writer drops "of its own"** in runs 3 and 4. "The client uses game rules only to show a
  player their options", next to an AD that puts every game rule in the engine, can read as the
  client using the engine.
