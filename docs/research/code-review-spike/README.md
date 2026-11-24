# Stock code review spike: findings

2026-11-24. A record of a spike on running Claude Code's stock code review from the Agent SDK, as
of this date. It isn't kept up to date.

## The question

Can a role started from the Agent SDK run Claude Code's stock code review (`/code-review`) on the
changes not yet committed, and still hand back its findings as structured output? The
implementation loop's blueprint asked for this before the review copy was built, when the quality
reviewer was meant to run the stock review.

## Takeaways

1. **Asked in words, it works.** A role told to run the stock code review with no target called the
   `code-review` skill, which reviewed `git diff HEAD`. It found both planted bugs and handed back
   valid structured output, in 3 runs out of 3.
2. **A prompt of only `/code-review` doesn't.** The same review ran and found the same bugs, but
   the role never handed back structured output. The result said `success`, with
   `structured_output` null.
3. **The stock prompt changes from one Claude Code version to the next.** The `high` prompt in
   2.1.331 differs a lot from road-trip-agent's 2.1.301 copy (see "Compared with 2.1.301" below).
   This is why the quality reviewer's prompt became the factory's own, started from the stock one
   (AD-10), and the role no longer runs the stock skill.
4. **The floor of 5 findings fills a review with nits and older problems.** A change with two real
   bugs got 5 or 6 findings in every run.

## Setup

- `claude-agent-sdk` 0.2.188 for Python, Claude Code CLI 2.1.331, `claude-opus-5-5`.
- The repo reviewed was shaped like a review copy: one commit named "base", then a change not yet
  committed, with no git remote. `make-template.sh` in this folder builds it. The change plants two
  bugs. `page()` starts one page late, though its docstring says pages count from 1. The new
  `last_page()` then always returns an empty list. The existing `test_first_page` fails with it.
- The role had `setting_sources=["project"]` (the repo had no CLAUDE.md or settings), no edit
  tools, and `gh`, `git push` and `git commit` denied. It ran with `bypassPermissions` and a turn
  cap of 100.
- Its findings schema had an ID, file, line, problem and a case where it goes wrong, with no
  severity field.
- `spike.py` in this folder is the script. Each run reviewed a fresh copy of the repo.

The script here was rebuilt from the session after its scratch copy was cleared, and hasn't been
run in this form.

## The runs

| Run | Prompt | Structured output | Findings | Both bugs found | Cost |
|---|---|---|---|---|---|
| init | "Reply with the single word: ok" | Not asked for | None | n/a | $0.13 |
| slash | `/code-review` | Null, with `success` | 5, in the result text only | Yes | $0.12 |
| told 1 | Told in words | Valid | 6 | Yes | $0.25 |
| told 2 | Told in words | Valid | 5 | Yes | $0.16 |
| told 3 | Told in words | Valid | 5 | Yes | $0.16 |

Each review run took about a minute.

## What the runs showed

- **The skill is there for a role.** The session's start message listed `code-review` in both its
  skills and its slash commands. Its tools included `Skill` and `ReportFindings`.
- **How the told runs went.** The role called its Skill tool with `{"skill": "code-review"}`. The
  skill ran as a fork, a general-purpose subagent on Opus. The fork's prompt is in
  `stock-prompt-high-2.1.331.md`, and all four review runs got it word for word. The fork handed
  the role a JSON array of findings, each with `file`, `line`, `summary`, `failure_scenario` and
  `severity`. The role copied them into its schema and called `StructuredOutput`. Since the schema
  had no severity field, the severity was lost, except in one run that folded "Severity: ..."
  into the problem text.
- **It ran at `high` with nothing asking for a level.** The fork's prompt opens with
  "high effort". The skill's description says that with no level given, it reuses the last one
  typed, and a fresh SDK session has none.
- **How the slash run went.** Claude Code expanded the command before the role's first turn, so the
  skill's instructions were the whole task. The fork ran the same review. The role then wrote the
  findings as text and ended. The result reported 0 turns, `subtype: "success"`, `is_error: false`
  and `structured_output: null`. This is the same result as the SDK quirk the loop's blueprint
  records, where a role ends with no structured output.
- **The diff command.** The fork's first command was `git diff origin/HEAD...HEAD`, as its prompt
  says to run "exactly as written". It failed, since the repo had no remote. The fork went on to
  `git diff HEAD`, which its prompt also asks for when there are changes not yet committed.
- **The floor.** Past the two planted bugs, each run filled out its 5 or 6 findings with older
  problems and nits. The older problems were that `page()` and `page_count()` don't check their
  inputs, so 0 or a negative number gives wrong pages or a `ZeroDivisionError`. The nit was that
  `last_page()` has no test.
- **`ReportFindings` was never called,** as the prompt asks.

## Compared with 2.1.301

road-trip-agent copied the `high` prompt from 2.1.301, in its
`research/code-review/code-review-prompt-high.md`. The 2.1.331 prompt differs in these ways:

- **4 angles, down from 8.** The reuse, simplification, efficiency and altitude angles are gone.
  The three bug angles and the CLAUDE.md conventions angle are left.
- **Each finding has a severity:** `important`, `nit` or `pre_existing`, each defined.
- **Each summary ends with "Fix:"** and the change to make.
- **A different diff step.** 2.1.301 ran `git diff @{upstream}...HEAD`. 2.1.331 runs
  `git diff origin/HEAD...HEAD`, and says never to use `@{upstream}`, grouped commands or shell
  variables, since they need permission.
- **The user-level CLAUDE.md** is taken only from the fork's context, never searched for or read.
- **The same in both:** the floor of at least 5 findings, the cap of 10, no check of each finding
  against the code, and "Do not call the ReportFindings tool".

## What the spike didn't test

- A real change. This one was tiny, with obvious bugs.
- A project's docs or CLAUDE.md, since the repo had none.
- Running tests, since the repo had no dependencies installed.
- More than three runs of the prompt that worked, or any model but Opus.
