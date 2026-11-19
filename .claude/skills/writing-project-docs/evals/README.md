# Evaluations for writing-project-docs

Each folder here is one test case, in the layout `claude plugin eval` reads. A case gives a fresh
agent one small task, in a throwaway repo that the case's scaffold script builds. Then graders
check what the agent produced.

## A case folder

- `prompt.md`: run settings, then the task exactly as a user would type it. `plugins: ["../.."]`
  points the runner at this skill's folder. `model` sets the agent's model. `tags` puts the case in
  groups you can run together. `runs` sets how many times the case runs. A case without it runs 3
  times. See "How many runs" below.
- `case.yaml`: the case's name, a plain description of a good result, and the scaffold script. The
  description is for people. The runner never shows it to the judge.
- `place-files.sh`: builds the repo the agent works in, as a git repo, from `files/`. `base/` is
  what's on main. `change/` is copied over it on a branch, and is committed for a reviewer or left
  uncommitted for an agent checking its own change. It also copies the doc standards into the test
  repo's `docs/standards/`, in its first commit. They come from `docs/standards/` in this repo's
  folder as it is when the case runs, uncommitted changes included, whatever branch is checked
  out. So a case tests the standards you're working on. It stops with an error if it can't find
  them.
- `files/`: the input files.
- `graders/`: one check per file. Each is a statement about the result that's true or false.
  - `type: llm` means a judge model decides, from the file or message named in `focus`. Each one is
    a separate judge call, asked 3 times, and the majority wins.
  - `type: regex` matches a pattern against a file or the agent's last message. It's free.
  - `type: tool_used` with `max: 0` passes only if the agent never called that tool. It's free.
- `STATUS.md`: only in a case that still fails some runs. It says how the last run went and
  describes the known failure. When a case fails, read it first to see whether the failure is new.

## Cases

Each case has a group tag and a role tag. The group tag names the group of cases it belongs to.
The role tag says whose work the agent checks: `write` for its own, `review` for someone else's. A case's name starts with both, in
that order, such as `terms-review-citations`. Some cases have a third tag, below.

The "Without the skill" column says how the case did in its last run without the skill. A case
that passes without the skill doesn't depend on it. Every one of those runs was made before the
standards moved out of the skill and into each case's repo. An agent without the skill can now
find the standards in the repo, so some cases may do better without the skill than the column
says. The next re-baseline updates the column. A case whose column says 3 of 3 also has the
`passes-without-skill` tag. See "With or without the skill" below.

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

The rules for the Terms section and names: that a term states no rule, when a term cites
something, that a word defined in Terms means only that, everywhere, and that each thing has one
name. The check script can't flag these, so these cases also test whether the agent finds the
problem.

| Case | Task | Passes when | Without the skill |
|---|---|---|---|
| `terms-review-citations` | A change adds five terms. Organizer cites a requirement its meaning doesn't depend on. Waitlist cites the requirement that adds members to it. No-show cites the rule that says when it happens. Check-in cites the section with every check-in rule. | It edits nothing, lists the Organizer and Waitlist citations as problems in this change, and doesn't call the other two problems. | 0 of 3 |
| `terms-write-citations` | Write a functional spec from planning notes. | No-show cites its rule. Organizer, waitlist and booking cite no requirement. A section citation names a section that holds the term's rules. | 0 of 3 |
| `terms-review-second-meaning` | The spec defines Free as a room no booking holds. A change adds FR-9, which says bookings are "free of charge". | It edits nothing, lists FR-9's "free" as a problem in this change, and suggests a rewrite without the word. | 3 of 3 |
| `terms-write-second-meaning` | Write a functional spec from planning notes that use "free" both for a slot nobody has booked and for costing nothing. | Every use of "free" in the spec has one meaning, and the spec still says bookings cost nothing. | 3 of 3 |
| `terms-review-one-name` | The spec defines Meeting room, Phone room and Organizer. A change adds FR-4, which limits the hours of a booking of a "room", and FR-5, which emails the booking's "host". | It edits nothing, and lists both as problems in this change: "room" should be the full name or names, or go, and "host" should be "organizer". | 0 of 3 |
| `terms-review-word-uses` | The spec defines Room as a meeting room or a phone room, Hold as a room and time slot kept for a member, and Round as the office manager's evening check. A change adds FR-6, which shows the hours "each room" was booked, "rounded up", and FR-7, which says the app shall "hold" a cancelled booking for 30 days. | It edits nothing, lists FR-7's "hold" as a problem in this change, and doesn't object to "rounded up" or to the bare "room". | 3 of 3 |
| `terms-review-decisions` | The technical spec's AD-2 splits the app into a web server and a worker, AD-3 says the web server runs no task, and TD-1 says how many tries a task gets. A change adds three terms. Worker is "the part of the app that runs tasks (AD-2)". Web server "never runs a task". Failed task is a task that still fails after its last try, citing TD-1. The change also adds TR-2, which says the worker runs every task that came due while it was stopped, and TD-2, which meets it. | It edits nothing, lists the Worker citation and Web server's "never runs a task" as problems in this change, and doesn't object to Worker's "runs tasks", to Failed task's citation, or to TR-2 naming the worker. | 1 of 3 |
| `terms-write-decisions` | Write a technical spec from architecture notes that split the app into a web server and a worker, and call a job that still fails after its last try a dead job. | The web server and the worker are terms that name their main job, cite no architecture decision, and don't say which part runs jobs. Dead job cites the item that says how many tries a job gets. | 0 of 3 |
| `terms-review-rules` | A change adds three terms. Organizer is "the one member" a booking is for, and FR-9 allows only one organizer. Waitlist lasts "until that time slot starts", and FR-10 empties it then. Room has "at least four chairs", and no requirement says what a room holds. | It edits nothing, lists Organizer and Waitlist as problems in this change, and doesn't object to Room's definition. | 0 of 1 |

The runs without the skill were on commit `eda6175`, except for `terms-review-one-name`'s, which
were on commit `f8306f9`, `terms-review-word-uses`'s, which were on commit `85aba06`, and
`terms-review-rules`'s, which was one run, on the commit that added the case.
`terms-write-decisions`' were on the commit that added the case. `terms-review-decisions`' were on
the commit that merged `items-review-tr-names-part` into it (issue 58).

`terms-review-decisions` also has the `items` tag. It holds the check from the old
`items-review-tr-names-part`, that a technical requirement may name a part an architecture decision
created.

### `items`

The rules for writing an item: one item for each fact, when a requirement gets a scenario or a
Why, what may go under a requirement, and how a limit is written. The check script can't flag
most of these either.

Most of these are reviewer cases. The reviewer is the last check before a problem gets through,
and a writer checking its own work runs the same review checks, so one reviewer case covers both.
`items-write-limits`, `items-write-unsettled`, `items-write-options` and `items-write-no-option`
are writer cases.

| Case | Task | Passes when | Without the skill |
|---|---|---|---|
| `items-review-one-fact` | A change adds FR-5, which repeats FR-1's 14-day limit as "two weeks", and FR-4, a cap of 3 upcoming bookings. All three limit making a booking. | It edits nothing, lists FR-5 as a problem in this change, and doesn't call FR-4 a copy of another requirement. | 3 of 3 |
| `items-review-scenarios-whys` | A change adds three requirements with Whys, and check-ins with a scenario under each requirement. FR-4's Why, the office's hours, passes both tests. FR-5's changes nothing, and FR-6's is clear from the rule. FR-7's scenario shows that an organizer can't check in 20 minutes into a booking, since FR-8 cancelled it at 15. FR-8's only restates FR-8. | It edits nothing, lists the Whys on FR-5 and FR-6 and FR-8's scenario as problems in this change, and doesn't call FR-4's Why or FR-7's scenario a problem. | 0 of 3 |
| `items-review-from-notes` | The task, given in the prompt, is to add the rules in planning notes to the spec. The notes open with a paragraph saying the first version is for an office of 20 to try for a month, and the change leaves it out. It cuts both of the notes' examples. The check-in example only shows FR-5 at work. The booking-limit example held a rule, that same-day bookings don't count toward the 3, and no requirement has it. A plain line under FR-6 holds a rule. | It edits nothing, and lists the lost same-day rule and FR-6's plain line as problems in this change. It doesn't call the cut check-in example or the left-out paragraph a problem. | 3 of 3 |
| `items-review-cuts` | The task, given in the prompt, is to take projectors out of the spec. The change deletes the projector term and requirements. It also drops FR-4's exception for bookings on the same day, and the commit message says the exception was only there for projector bookings. | It edits nothing, lists the lost same-day exception as a problem in this change, and doesn't call the projector cuts a problem. | 3 of 3 |
| `items-review-triggers` | A change adds two requirements, each with two triggers. FR-13 offers another room to a member asking for a room an admin has closed, or a room kept for the board, which lists the rooms FR-11 and FR-12 keep from a member. FR-14 emails a confirmation when an organizer cancels a booking or a member joins a waitlist. | It edits nothing, says FR-13 should cite FR-11 and FR-12 in place of its list, doesn't ask to split FR-13, and says to split FR-14. | 1 of 3 |
| `items-write-limits` | Write a functional spec from planning notes that list eight things the app won't do, and say it's web only for the first version, with a phone app later. One of the eight has a reason that passes both tests for a Why. Three name only what's ruled out, or don't simplify the design: no ads, no chat, and no targets or nudges on the office manager's room figures. | Equipment, other offices, web only and one organizer are limits, written with "only ... not", with no separate Limits section. Only the 6 pm rule has a Why. Ads, chat and targets aren't in the spec, and the room figures are. The spec doesn't mention the phone app coming later. | 0 of 3 |
| `items-review-facet-guesses` | From a real run: the source is Facet's design doc, and the change adds the spec a writer wrote from it, with its commit message. FR-18's "every public item that fits it" guesses at "eligible public content", which the doc never defines, and the commit message lists it as an open question. | It edits nothing, lists FR-18's guess as a problem in this change whatever the commit message says, and doesn't call FR-31's one hour a guess. | 0 of 3 |
| `items-review-unsettled` | The task is to add waitlists to the spec from planning notes, which say waitlists close "shortly before the slot starts". The change adds FR-7, which empties a slot's waitlists 30 minutes before it starts. FR-4, FR-5 and FR-6 say only what the notes settle. | It edits nothing, lists FR-7's 30 minutes as a problem in this change, and doesn't say FR-4, FR-5 or FR-6 go beyond the notes. | 3 of 3 |
| `items-write-unsettled` | Write a functional spec from planning notes that say a view's section "can follow all eligible public content or show selected items", and never say what makes content eligible. | No rule says which items a following section shows, and none uses "eligible". The spec keeps the rule for selected items. The report asks what "eligible" means and suggests an answer. | 0 of 3 |
| `items-write-options` | Write a technical spec from architecture notes that say the engine is shared code and the client "may use" it to show legal moves, and that the client holds no rules logic of its own beyond what it needs to show options. | No item says whether the client uses the engine, and none copies the "may". The report asks whether the client should use it and suggests an answer. | 0 of 3 |
| `items-review-no-option` | A change adds two design decisions with no Why. TD-1 identifies spaces by axial coordinates, a real choice. TD-2 says a tile's side n faces side (n + 3) mod 6 of the tile next to it, which follows from how the Tile side term numbers the sides. | It edits nothing, lists TD-2 as a problem in this change because it isn't a decision, suggests moving it out of the spec's decisions rather than adding a Why, and doesn't say TD-1 isn't a decision. | 3 of 3 |
| `items-write-no-option` | Write a technical spec from architecture notes that give the same facing rule with no reason, and split the code into an engine, a server and a client, also with no reason. | No item or term says which tile sides face each other. The report puts that fact in a blueprint or names its home in the code, and doesn't ask for its reason. The split into engine, server and client is a decision, and the report asks for its reason. | 0 of 3 |

The runs without the skill were on commit `f8306f9`, except for those below.
`items-review-triggers`', `items-review-cuts`', `items-review-unsettled`', `items-write-unsettled`'
and `items-review-facet-guesses`' were on the commit that added the case. `items-write-options`' were
on the commit that dropped its grader for the client rule. `items-review-no-option`' and
`items-write-no-option`' were on the commit that added the case, before the writer case's control
changed from axial coordinates to the three-part split. `items-review-from-notes`',
`items-review-scenarios-whys`' and `items-write-limits`' were on the commit that made them by
merging other cases (issue 58).

## Running them

From this skill's folder:

```bash
claude plugin eval . --scaffold --allow-tools Write,Edit,Bash --judge-model sonnet -j 8 --ablation none
```

- `--scaffold` lets each case's `place-files.sh` run. Without it, the agent gets an empty folder.
- `--judge-model sonnet` sets the judge. It's Haiku by default. Anthropic's guide for writing these
  evals recommends a Sonnet-class judge.
- `--ablation none` skips the runs without the skill. See below for when to leave it off.
- Each case runs as many times as its `runs` says, or 3 times if it has none. `--runs <n>` runs
  every case n times, whatever its `runs` says.
- `--tag <tag>` runs the cases with that tag, such as `--tag review-roles`. Given more than one
  tag, it runs the cases that have any of them, not all of them. A group's tag also picks up the
  group's `passes-without-skill` cases.
- `--case <name>` runs one case, and takes a glob, such as `--case 'terms-review-*'` for the
  `terms` group's reviewer cases. With `--tag`, a case has to match both. Give `--case` only once.
  Given twice, it runs only the last one.
- `--model <model>` overrides every case's `model`.
- `-j <n>` runs up to n agent runs at once, from 1 to 8. It's 1 by default, which is slow, so use
  8. It can only be set on the command line.
- `--keep-temp` keeps each run's folder, so you can see what the agent did.

These are real, billed model runs.

### With or without the skill

Run with the skill only, using `--ablation none`. Without that flag, each case also runs without
the skill, which doubles the cost.

Leave the flag off only when a case is new or has changed a lot, or when re-baselining (see "How
many runs"). The runs without the skill show whether the case depends on the skill at all. An agent
can't guess this project's standards, such as its IDs, its prose and the two lists a reviewer
reports, without the skill. So for most cases, runs without it only confirm that, and running them
every time adds nothing.

A case that passes 3 of 3 without the skill gets the `passes-without-skill` tag. It doesn't show
that the skill helps, but it still matters. It catches a model or effort change that breaks
something the agent used to do on its own. Some of these cases also catch the skill making the
agent worse, such as fixing things that aren't broken. `--tag passes-without-skill` runs just
these cases.

### How many runs

A full run is costly when every case runs 3 times, so each case sets its own run count with `runs`
in `prompt.md`. Anthropic's post
[Demystifying evals for AI agents](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)
splits evals into capability evals, which test what the agent can't do well yet, and regression
evals, which check it still does what it used to. A capability eval that passes reliably moves into
the regression suite. Here, that works like this:

- **After a full run,** a case that passed 3 of 3 gets `runs: 1`. The rest stay at 3, with no
  `runs` line.
- **When a 1-run case fails,** rerun it 3 times right away, with `--case <name> --runs 3`. If it
  passes 3 of 3, it stays at 1 run. If not, remove its `runs` line, so it goes back to 3 runs. This
  keeps one bad run from deciding anything, without needing a history of results.
- **To re-baseline,** such as when the agent's model or effort changes, run every case without
  `--ablation none` and with `--runs 3`. Then update each case's `passes-without-skill` tag, its
  "Without the skill" column and its `runs`. On a model change, also decide whether a reviewer case
  needs a writer case on the new model.

### Which cases to run

While the skill changes, run only the failing cases. A case passes at 3 runs out of 3.

A full run after a batch of skill changes runs every case, each at its own run count: the command
above, with no `--tag` or `--case`.

Before a 3-run pass, do one run of each case. It costs a third as much, and it catches a broken
setup before the bigger run. A case gets up to 3 single runs, with fixes to the skill, the case or
its graders in between, before its 3-run pass.

When a case fails because of its setup, fix the setup and run that case once more. Read the reply.
A case goes into a 3-run pass only once its result, pass or fail, has nothing to do with the
setup.
