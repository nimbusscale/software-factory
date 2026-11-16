# Evaluations for writing-project-docs

Each folder here is one test case, in the layout `claude plugin eval` reads. A case gives a fresh
agent one small task, in a throwaway repo that the case's scaffold script builds. Then graders
check what the agent produced.

## A case folder

- `prompt.md`: run settings, then the task exactly as a user would type it. `plugins: ["../.."]`
  points the runner at this skill's folder. `model` sets the agent's model. `tags` puts the case in
  groups you can run together.
- `case.yaml`: the case's name, a plain description of a good result, and the scaffold script. The
  description is for people. The runner never shows it to the judge.
- `place-files.sh`: builds the repo the agent works in, as a git repo, from `files/`. `base/` is
  what's on main. `change/` is copied over it on a branch, and is committed for a reviewer or left
  uncommitted for an agent checking its own change.
- `files/`: the input files.
- `graders/`: one check per file. Each is a statement about the result that's true or false.
  - `type: llm` means a judge model decides, from the file or message named in `focus`. Each one is
    a separate judge call, asked 3 times, and the majority wins.
  - `type: regex` matches a pattern against a file or the agent's last message. It's free.
  - `type: tool_used` with `max: 0` passes only if the agent never called that tool. It's free.
- `STATUS.md`: only in a case that still fails some runs. It says how the last run went and
  describes the known failure. When a case fails, read it first to see whether the failure is new.

## Cases

Each case has two tags. One names the group of cases it belongs to. The other says whose work the
agent checks: `write` for its own, `review` for someone else's. A case's name starts with both, in
that order, such as `terms-review-citations`.

The "Without the skill" column says how the case did in its last run without the skill. A case
that passes without the skill doesn't depend on it. See "With or without the skill" below.

### `review-roles`

Whether the agent fixes its own change, and only reports on someone else's. The planted problems
are ones the doc check script flags, so they're easy to find. These cases test what the agent does
with a problem, not whether it can spot one.

| Case | Task | Passes when | Without the skill |
|---|---|---|---|
| `review-roles-write-fixes-its-problem` | A new requirement has no ID. FR-3 cites F-SEC-5, which doesn't exist, on main too. | It gives the requirement an ID, leaves FR-3 alone, and doesn't mention F-SEC-5. | 0 of 3 |
| `review-roles-write-clean` | A change with no problems. | It edits nothing. | 3 of 3 |
| `review-roles-review-clean` | A change with no problems. | It edits nothing and reports no problems. | 0 of 3 |
| `review-roles-review-new-doc` | A change that adds the whole spec, with a requirement that has no ID. | It edits nothing, lists the missing ID as a problem in this change, and lists no older problems. | 1 of 3 |
| `review-roles-review-new-and-older` | A new requirement with no ID, and the older F-SEC-5 citation. | It edits nothing and puts each problem in the right list, each with all four parts. | 0 of 3 |
| `review-roles-review-older-only` | A change with no problems, and the older F-SEC-5 citation. | It edits nothing, reports no problems in this change, and lists the citation as older. | 0 of 3 |
| `review-roles-review-missed-doc` | A code change raises the booking limit to 30 days. FR-1 still says 14, and the spec isn't in the diff. | It edits nothing and lists FR-1 as a problem in this change. | 3 of 3 |

The runs without the skill were on commit `6eee2a4`. Some of these cases changed after it.

### `terms`

The rules for the Terms section and names: when a term cites something, that a word defined in
Terms means only that, everywhere, and that each thing has one name. The check script can't flag
these, so these cases also test whether the agent finds the problem.

| Case | Task | Passes when | Without the skill |
|---|---|---|---|
| `terms-review-citations` | A change adds five terms. Organizer cites a requirement its meaning doesn't depend on. Waitlist cites the requirement that adds members to it. No-show cites the rule that says when it happens. Check-in cites the section with every check-in rule. | It edits nothing, lists the Organizer and Waitlist citations as problems in this change, and doesn't call the other two problems. | 0 of 3 |
| `terms-write-citations` | Write a functional spec from planning notes. | No-show cites its rule. Organizer, waitlist and booking cite no requirement. A section citation names a section that holds the term's rules. | 0 of 3 |
| `terms-review-second-meaning` | The spec defines Free as a room no booking holds. A change adds FR-9, which says bookings are "free of charge". | It edits nothing, lists FR-9's "free" as a problem in this change, and suggests a rewrite without the word. | 3 of 3 |
| `terms-write-second-meaning` | Write a functional spec from planning notes that use "free" both for a slot nobody has booked and for costing nothing. | Every use of "free" in the spec has one meaning, and the spec still says bookings cost nothing. | 3 of 3 |
| `terms-review-one-name` | The spec defines Meeting room, Phone room and Organizer. A change adds FR-4, which limits the hours of a booking of a "room", and FR-5, which emails the booking's "host". | It edits nothing, and lists both as problems in this change: "room" should be the full name or names, or go, and "host" should be "organizer". | 0 of 3 |

The runs without the skill were on commit `eda6175`, except for `terms-review-one-name`'s, which
were on commit `f8306f9`.

### `items`

The rules for writing an item: one item for each fact, when a requirement gets a scenario or a
Why, what may go under a requirement, and how a limit is written. The check script can't flag
most of these either.

Most of these are reviewer cases. The reviewer is the last check before a problem gets through,
and a writer checking its own work runs the same review checks, so one reviewer case covers both.
`items-write-limits` is a writer case.

| Case | Task | Passes when | Without the skill |
|---|---|---|---|
| `items-review-one-fact` | A change adds FR-5, which repeats FR-1's 14-day limit as "two weeks", and FR-4, a cap of 3 upcoming bookings. All three limit making a booking. | It edits nothing, lists FR-5 as a problem in this change, and doesn't call FR-4 a copy of another requirement. | 3 of 3 |
| `items-review-scenarios` | A change adds check-ins, with a scenario under each requirement. FR-4's shows that an organizer can't check in 20 minutes into a booking, since FR-5 cancelled it at 15. FR-5's only restates FR-5. | It edits nothing, lists FR-5's scenario as a problem in this change, and doesn't call FR-4's a problem. | 0 of 3 |
| `items-review-whys` | A change adds three requirements with Whys. FR-4's Why, the office's hours, passes both tests. FR-5's changes nothing, and FR-6's is clear from the rule. | It edits nothing, lists the Whys on FR-5 and FR-6 as problems in this change, and doesn't call FR-4's a problem. | 0 of 3 |
| `items-review-examples` | A change writes three rules from planning notes and cuts both of the notes' examples. The check-in example only shows FR-5 at work. The booking-limit example held a rule, that same-day bookings don't count toward the 3, and no requirement has it. A plain line under FR-6 holds a rule. | It edits nothing, lists the lost same-day rule and FR-6's plain line as problems in this change, and doesn't call the cut check-in example a problem. | not run yet |
| `items-write-limits` | Write a functional spec from planning notes with four limits, one with a reason that passes both tests, and a phone app planned for later. | Each limit is a requirement in the Limits section, written with "only ... not". Only the 6 pm limit has a Why. The spec doesn't mention a phone app. | 0 of 3 |

The runs without the skill were on commit `f8306f9`, except for `items-review-scenarios`'s. Those
were on an earlier version of the case, before both of its scenarios changed.

## Running them

From this skill's folder:

```bash
claude plugin eval . --scaffold --allow-tools Write,Edit,Bash --judge-model sonnet -j 4 --ablation none
```

- `--scaffold` lets each case's `place-files.sh` run. Without it, the agent gets an empty folder.
- `--judge-model sonnet` sets the judge. It's Haiku by default. Anthropic's guide for writing these
  evals recommends a Sonnet-class judge.
- `--ablation none` skips the runs without the skill. See below for when to leave it off.
- Each case runs 3 times by default. `--runs <n>` changes that.
- `--tag <tag>` runs the cases with that tag, such as `--tag review-roles`. Given more than one
  tag, it runs the cases that have any of them, not all of them.
- `--case <name>` runs one case, and takes a glob, such as `--case 'terms-review-*'` for the
  `terms` group's reviewer cases. With `--tag`, a case has to match both. Give `--case` only once.
  Given twice, it runs only the last one.
- `--model <model>` overrides every case's `model`.
- `-j <n>` runs up to n agent runs at once, from 1 to 8. It's 1 by default, which is slow, so use at
  least 4. It can only be set on the command line.
- `--keep-temp` keeps each run's folder, so you can see what the agent did.

These are real, billed model runs.

### With or without the skill

Run with the skill only, using `--ablation none`. Without that flag, each case also runs 3 times
without the skill, which doubles the cost.

Leave the flag off only when a case is new or has changed a lot. The runs without the skill show
whether the case depends on the skill at all. An agent can't guess this project's standards, such
as its IDs, its prose and the two lists a reviewer reports, without the skill. So for most cases,
runs without it only confirm that, and running them every time adds nothing.

A case that passes without the skill still stays. It checks that the skill doesn't make the agent
worse, such as fixing things that aren't broken, and it catches a later change to the skill that
breaks it. The cases whose "Without the skill" column says 3 of 3 are like this.

### Which cases to run

Run only the failing cases. A case passes at 3 runs out of 3. Leave out a case that has passed
both with and without the skill, even after the skill changes, since it doesn't depend on the
skill.

Before a 3-run pass, do one run of each case. It costs a third as much, and it catches a broken
setup before the bigger run.

When a case fails because of its setup, fix the setup and run that case once more. Read the reply.
A case goes into a 3-run pass only once its result, pass or fail, has nothing to do with the
setup.
