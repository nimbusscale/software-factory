# Quality reviewer check: prompts on four changes with known bugs

2026-11-24. A record of what was tried and measured on this date. It isn't kept up to date.

## What was tried

Several prompts for the quality reviewer each reviewed the same four road-trip-agent changes, whose
real bugs are known, once per change:

- **The stock code review's prompt** at `high`, from Claude Code 2.1.331.
- **A prompt started from the stock one,** in two wordings. The first is the stock prompt with no
  floor or cap on findings, no conventions angle, and a review target from its caller. The current
  wording also asks for every candidate with a failure scenario, and says a bug a user of the code
  can hit is never a nit. Both are in `stock-based/`.
- **A prompt started from road-trip-agent's `review-pr` skill,** with a rubric for any project. It
  keeps the skill's angles A to C and its step that checks each candidate against the code, then
  labels it. It checks fit for use only, leaving out the task and the design docs, and lists every
  candidate it drops. It was run as a first draft and then in three iterations, each a change to
  the prompt and the rubric, in `rubric-based/`:

| Run | Folder | What changed |
|---|---|---|
| First draft | `0-first-draft` | The prompt and rubric as first written |
| Iteration 1 | `1-run-code` | D1 needs proof: a check in the code, or a run of it. The prompt says to run the code when a claim depends on values. The clones had their dependencies installed |
| Iteration 2 | `2-drop-rules` | Only D1 and a note about older code drop a candidate. A doc that puts a case outside the app's use isn't proof for D1 |
| Iteration 3 | `3-drop-reasons` | Each dropped candidate names one of those two reasons, in a field the schema limits to them. A doc that asks for the behavior isn't proof for D1 either |

Each folder holds the prompt and rubric as they were run, and each run's whole result, including
the tool calls.

The four changes, and the known bug in each, from road-trip-agent's answer key in its
`research/code-review/code-review-evaluation.md`:

| PR | Known bug | Kind, in the answer key |
|---|---|---|
| #30 | `isAddress()` drops Google's name for a `premise` place, such as a named hotel | Code works, wrong behavior. Needs the design to find |
| #32 | `scheduleOf()` can return entries out of time order | Code bug. Can be found from the code alone |
| #33 | The persistence design says repositories hold the started-trip lock at save, and `save()` stops checking it | Doc contradicts itself |
| #35 | The driving warning and the schedule count a day's driving two different ways | In between |

## Setup

- `claude-agent-sdk` 0.2.188 for Python, Claude Code CLI 2.1.331, `claude-opus-5-5`.
- Each run reviewed a clone of road-trip-agent with history only up to the end of the change, so the
  fix commits weren't there. The review target was the change's commit range, such as
  `2682d24..d1107ab`.
- The role had `setting_sources=["project"]`, `bypassPermissions`, and no edit, agent or web
  tools. `gh`, `ssh`, `curl`, `wget`, and `git push`, `commit`, `fetch` and `pull` were denied.
- The stock runs, the stock-based runs and the rubric-based first draft ran in clones with no
  dependencies, so a reviewer could run plain `node -e` but couldn't import the repo's TypeScript.
  The three iterations ran after `npm ci`, so it could.
- The stock-based runs parsed findings from the result text. The rubric-based runs used a result
  schema, which required the `dropped` list. `rubric-based/run.py` is the script for iteration 3.
  The earlier rubric-based runs used the same script without the `dropped_as` field.
- For the rubric-based runs, each clone held the rubric at `docs/standards/review-rubric.md`, as an
  untracked file outside the review target.

`stock-based/run.py` read its prompts from a worktree that no longer exists, and
`stock-based/findings_md.py` reads runs from `runs-v1/` and `runs/`. Those are
`runs-first-wording/` and `runs-current-wording/` here. `stock-based/report.md` is the working
report from that check, with every finding and its mark.

## What was measured

Whether each run found each known bug, and how it marked it:

| PR | Stock | Stock-based, first | Stock-based, current | Rubric, first draft | Iteration 1 | Iteration 2 | Iteration 3 |
|---|---|---|---|---|---|---|---|
| #30 | Missed | Important | Missed | Missed | Missed | To check | Missed |
| #32 | Important | Nit | Missed | Dropped by mistake | Important | Important | Missed |
| #33 | Pre-existing | Called safe | Nit | Dropped, with the caller's check as proof | Dropped, the same way | Missed | Dropped, the same way |
| #35 | Missed | Missed | Missed | Missed | Missed | Missed | Missed |

The rubric-based runs, over all four changes:

| Run | Important | Of them, F6 | Nit | To check | Dropped | Drops the rubric doesn't allow | Code runs | Cost |
|---|---|---|---|---|---|---|---|---|
| First draft | 6 | 5 | 6 | 1 | 14 | 2 | 2 | $3.34 |
| Iteration 1 | 11 | 8 | 4 | 1 | 12 | 4 | 4 | $3.30 |
| Iteration 2 | 8 | 6 | 6 | 1 | 11 | 3 | 6 | $3.44 |
| Iteration 3 | 7 | 6 | 4 | 0 | 6 | 1 | 5 | $3.85 |

A drop the rubric doesn't allow is a D1 with no proof, a D1 whose proof is a doc, or a note about
code the change added. The first draft's rubric hadn't yet said a D1 needs proof. Code runs count
the `node` and `python` commands the reviewer ran. Each run took 80 to 150 seconds. The stock and
stock-based runs cost $0.42 to $0.89 each.

## What was found

1. **No prompt found more than two of the four known bugs in one set of runs.** #35's was missed by
   every run.
2. **The stock-based prompts marked real bugs as nits.** The first wording marked #32's bug a nit,
   and the current wording marked #33's a nit. About 5 of the current wording's 16 nits were bugs a
   user could hit, though its own definition of a nit ruled those out.
3. **The rubric-based prompt gave each finding a reason for its label that fits the rubric.** Its
   nits were wrong text (N3), code that can't run (N1), or bugs that need an unlikely input (NF1).
   Whether an input is unlikely varied: #35's opening periods that meet at midnight were NF1 in
   two runs and F2 in one, and one run didn't raise them.
4. **The first draft found #32's bug and argued it away.** It reasoned that each waiting stop's set
   time is at or before the end of the drive, so the order holds. The bug is a waiting stop whose
   time is before the drive's start. The call shows only because the result lists every dropped
   candidate. Once a D1 needed proof and the code could run, iterations 1 and 2 found the bug, and
   confirmed it by running the code. Iteration 3 didn't raise it at all. Its change was only to
   how a candidate is dropped, so the miss is likely the spread between single runs.
5. **#33's bug was dropped with real proof.** The only caller of `save()` checks the lock first.
   The bug in the answer key is that the design contradicts itself, which a reviewer of fit for use
   doesn't check.
6. **#30's bug came up once, as a finding to check.** Iteration 2 asked for a real Google call to
   see whether named buildings carry the `premise` type.
7. **The reviewer drops notes it judges too small,** though the rubric makes each one a nit. Each
   iteration's rule cut this down, from 4 drops the rubric doesn't allow to 1. The one left in
   iteration 3 drops "You agreed to 5." as a false claim because the domain model gives the same
   text.
8. **Most important findings were missing tests.** F6 was 25 of the 32 important findings over the
   four runs.
9. **The reviewer ran little code,** one or two commands per change, even with the dependencies
   installed.

## What the check didn't test

- More than one run of each prompt on each change, so a single miss can be chance.
- A project with no agents of its own, or one whose docs set a threat model.
- The earlier findings that a later round gets.
