# Status

Last run: 2026-11-17, on commit `ebf5b5f`, 3 runs with the skill and 3 without. It passed 2 of 3
with the skill and 0 of 3 without.

| Grader | With the skill | Without |
|---|---|---|
| `01-no-edit` | 3 of 3 | 3 of 3 |
| `02-no-write` | 3 of 3 | 3 of 3 |
| `03-fr18-guess-is-a-problem` | 3 of 3 | 0 of 3 |
| `04-site-accessibility-guess-is-a-problem` | 2 of 3 | 0 of 3 |
| `05-fr31-hour-is-fine` | 3 of 3 | 3 of 3 |

## Known failure

`04-site-accessibility-guess-is-a-problem` fails in some runs. The reviewer uses the check
"Nothing was added that the source didn't settle", and lists other guesses, FR-18's among them,
each with a question and a suggested answer. It reads the design doc's accessibility line, but
only says colour contrast is missing. It doesn't say FR-43 and FR-44 stretch the admin's keyboard
and screen-reader rules to the site.

This guess is less clear than FR-18's. "Accessible" has a common meaning, and keyboard use and
screen-reader labels are its usual core, so a reviewer can fairly read "public pages aim to be
accessible" as covering FR-43 and FR-44. In a run with the example below added to the skill, a reviewer said
just that.

An example added to the check, "a rule the source gives for one part of the app applied to more
parts", didn't help. With it, the grader passed 1 of 3, so it isn't in the skill.
