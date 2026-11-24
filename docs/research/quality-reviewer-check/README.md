# Quality reviewer check: three prompts on four changes with known bugs

2026-11-24. A record of what was tried and measured on this date. It isn't kept up to date.

## What was tried

Three prompts for the quality reviewer each reviewed the same four road-trip-agent changes, whose
real bugs are known:

- **The stock code review's prompt** at `high`, from Claude Code 2.1.331.
- **A prompt started from the stock one,** in two wordings. The first is the stock prompt with no
  floor or cap on findings, no conventions angle, and a review target from its caller. The current
  wording also asks for every candidate with a failure scenario, and says a bug a user of the code
  can hit is never a nit. Both are in `stock-based/`.
- **A prompt started from road-trip-agent's `review-pr` skill,** with a rubric for any project. It
  keeps the skill's angles A to C and its step that checks each candidate against the code, then
  labels it. It leaves out the task and the design docs, and lists every candidate it drops. The
  prompt and the rubric, as they were run, are in `rubric-based/`.

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
- The clones had no dependencies installed, so a reviewer could run plain `node -e` but couldn't
  import the repo's TypeScript.
- The stock-based runs parsed findings from the result text. The rubric-based runs used a result
  schema, which required the `dropped` list.
- For the rubric-based runs, each clone held the rubric at `docs/standards/review-rubric.md`, as an
  untracked file outside the review target.

`stock-based/run.py` read its prompts from a worktree that no longer exists, and
`stock-based/findings_md.py` reads runs from `runs-v1/` and `runs/`. Those are
`runs-first-wording/` and `runs-current-wording/` here. `stock-based/report.md` is the working
report from that check, with every finding and its mark. `rubric-based/runs/` holds each run's
whole result, including the tool calls.

## What was measured

Whether each run found each known bug, and how it marked it:

| PR | Stock | Stock-based, first wording | Stock-based, current wording | Rubric-based |
|---|---|---|---|---|
| #30 | Missed | Found, important | Missed | Missed |
| #32 | Found, important | Found, nit | Missed | Seen, then dropped as a false claim |
| #33 | Found, pre-existing | Seen, then called safe | Found, nit | Seen, then dropped as a false claim |
| #35 | Missed | Missed | Missed | Missed |

Findings and cost of the rubric-based runs:

| PR | Findings | Important | Nit | To check | Dropped | Cost | Time |
|---|---|---|---|---|---|---|---|
| #30 | 5 | 3 (2 F6, 1 F4) | 1 (NF1) | 1 (V1) | 4 | $0.71 | 120s |
| #32 | 2 | 2 (2 F6) | 0 | 0 | 4 | $0.72 | 107s |
| #33 | 2 | 0 | 2 (2 N3) | 0 | 3 | $1.11 | 150s |
| #35 | 4 | 1 (F6) | 3 (2 NF1, 1 N3) | 0 | 3 | $0.81 | 132s |

The stock and stock-based runs cost $0.42 to $0.89 each.

## What was found

1. **No prompt found more than two of the four known bugs.** #35's was missed by every run.
2. **The stock-based prompts marked real bugs as nits.** The first wording marked #32's bug a nit,
   and the current wording marked #33's a nit. About 5 of the current wording's 16 nits were bugs a
   user could hit, though its own definition of a nit ruled those out.
3. **The rubric-based prompt saw two known bugs and dropped both as false claims.** For #32, it
   reasoned that each waiting stop's set time is at or before the end of the drive, so the order
   holds. The bug is a waiting stop whose time is before the drive's start, so that reasoning
   doesn't rule it out. For #33, it found that the only caller of `save()` checks the lock first.
   That holds for the code, and the bug in the answer key is that the design contradicts itself.
   Both calls show only because the result lists every dropped candidate.
4. **The rubric-based prompt gave each finding a reason for its label that fits the rubric.** Its
   nits were wrong text (N3) or bugs that need an unlikely input (NF1). One NF1 is open to doubt:
   in #35, places whose opening periods meet at midnight may be common in Google's data.
5. **Most of its important findings were missing tests.** Five of its six were F6, behavior the
   change adds that no test checks.
6. **It ran little code.** Two of its four runs ran no `node` or `python` check, and none could
   import the repo's TypeScript, since the clones had no dependencies. #32's dropped bug is the kind
   of claim that running the code would settle.
7. **Most of its dropped candidates were false claims (D1).** 13 of its 14 were dropped as D1, and
   one as a note on code that can't run.

## What the check didn't test

- More than one run of each prompt on each change.
- A review copy with its dependencies installed, so the reviewer can run the code it checks.
- A project with no agents of its own, or one whose docs set a threat model.
- The earlier findings that a later round gets.
