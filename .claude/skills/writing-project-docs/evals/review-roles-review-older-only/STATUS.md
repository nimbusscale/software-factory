# Status

Last run: 2026-11-15, on commit `50784c6`, 3 runs with the skill. It passed 2 of 3.

## Known failure

`03-no-problems-in-this-change` fails in some runs. The reviewer finds a problem in FR-5 that the
case didn't plant: FR-5 doesn't say whether the email must name which booking was cancelled. The
code sends the same text for every booking, so a member who missed two bookings gets two
identical emails. The reviewer lists that as a problem in this change, so the judges fail it.

This is a fair point about whether FR-5 can be tested, not a setup problem or a misread rule.
Making FR-5 say what the email contains would likely remove it.
