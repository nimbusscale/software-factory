# Status

Last run: 2026-11-17, on commit `aa5f5a6`, 1 run with the skill. It failed, with a score of 0.67.
Every earlier run passed, 7 of 7, the last on 2026-11-17 before commit `0a12ffe`.

## Known failure

`01-no-rule-for-eligible` failed. The writer raised the right question in its report, asking what
makes content eligible, so `03-report-asks-about-eligible` passed. But it also wrote FR-7 as
"every public content item that is eligible for that view section". That copies the notes' vague
word into a rule, which "Not settled by the source?" in SKILL.md says not to do.

Neither change since the last pass touched that paragraph. Those changes are `0a12ffe`, which put
both specs and their item rules in one reference file, and `aa5f5a6`, which cut the skill down to
the specs and blueprints. One run can't tell chance from a real change. Run it 3 times in the full
run after the day's batch of skill changes. If it still fails, look at what those two commits
moved or cut around the unsettled-source rules.
