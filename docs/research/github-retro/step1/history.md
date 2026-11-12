# How the practice changed

Sources: git history of `plan/`, `.github/ISSUE_TEMPLATE/task.md`, DEVELOPMENT.md and CLAUDE.md;
the GitHub pull in `step1/raw/`. Dates are 2026.

The project went through four eras. The measures use them as groups.

## A. The plan in the repo (10-15 to 10-19)

- Work was tracked in `plan/development-plan.md` (numbered phases) and `plan/open-items.md`. Together
  they are about 12,750 words today.
- `plan/` got 76 commits in five days.
- 46 PRs were opened. None had an issue. 41 of the first 49 PRs touched `plan/`.
- About 16 of the 46 PRs only updated the plan, such as "Mark phase 4 done" (16 words) or "Add the
  out-of-order note from phase 12 to phase 13's question". The work and the record of the work were
  separate PRs.
- Parallel batches ("Plan batch 4: phases 15 to 20 overnight") made the plan a shared file that
  several branches needed to change.
- From 10-16, the PR description already had a rule: "keep decisions out of the PR description"
  (commit bf206d0, when the CI review started). Only 6 of the 46 PRs had a decisions comment.

## B. Issues (10-19 to 10-22)

- Commit 93e1824 froze `plan/`, added DEVELOPMENT.md section 9 and the task issue template, and
  pointed CLAUDE.md at issues. 24 issues were opened that day, mostly phases moved from the plan.
- The template had Design, Open questions, Do, Done when, Ends in, and Settled in. No Why yet.
- The PR rule became: the task word for word, then "Done when" results, and a separate decisions
  comment. 19 of 20 PRs in this era had one.

## C. Why and "stand on its own" (10-22 to 10-28)

- Commits 07c8562 and d374ea3 added the Why section and the test: "could a new Claude Code session,
  with only the repo and this issue, build it the way it's meant?"
- This came from the itinerary read case in Joe's learnings doc: an issue said "Joe doesn't want
  to raise the limit" with no reason.
- Every PR in this era had a decisions comment (56 of 56).

## D. Autonomous work (10-28 on)

- Commit be80f72 added DEVELOPMENT.md section 10: working on issues without Joe, with subagents
  in worktrees, and a merge rule.
- Commit 812c02b (same day) sent set-aside items with a decided answer to an issue's Do list, not
  its open questions.
- Eval issues became common in this era (the "Eval Canidate" label), and so did simulated-user
  recordings, whose results went in issue comments.
