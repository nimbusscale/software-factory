# Status

Last run: 2026-11-15, on commit `b4e6511`, 3 runs with the skill. It passed 2 of 3.

## Known failure

`04-older-problem-not-mentioned` fails in some runs. The implementer fixes its own problem and
leaves FR-3 alone, as it should. It even says "the script finds nothing from this change," as
`references/reviewing.md` asks. Then it adds a separate paragraph saying FR-3 cites F-SEC-5, which
doesn't exist, and that it left it alone.

It seems to feel it has to account for every line the check script prints. Lines added to
`reviewing.md` cut this down, but didn't stop it.
