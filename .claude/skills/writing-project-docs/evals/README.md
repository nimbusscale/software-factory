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

## Cases

Each case has two tags. One says whose work the agent checks: `write` for its own, `review` for
someone else's. The other names the group of cases it belongs to.

### `review-roles`

Whether the agent fixes its own change, and only reports on someone else's. The planted problems
are ones the doc check script flags, so they're easy to find. These cases test what the agent does
with a problem, not whether it can spot one.

| Case | Tags | Task | Passes when |
|---|---|---|---|
| `self-review-fixes-its-problem` | `write` | A new requirement has no ID. FR-3 cites F-SEC-5, which doesn't exist, on main too. | It gives the requirement an ID, leaves FR-3 alone, and doesn't mention F-SEC-5. |
| `self-review-clean` | `write` | A change with no problems. | It edits nothing. |
| `review-clean` | `review` | A change with no problems. | It edits nothing and reports no problems. |
| `review-new-doc` | `review` | A change that adds the whole spec, with a requirement that has no ID. | It edits nothing, lists the missing ID as a problem in this change, and lists no older problems. |
| `review-new-and-older` | `review` | A new requirement with no ID, and the older F-SEC-5 citation. | It edits nothing and puts each problem in the right list, each with all four parts. |
| `review-older-only` | `review` | A change with no problems, and the older F-SEC-5 citation. | It edits nothing, reports no problems in this change, and lists the citation as older. |
| `review-missed-doc` | `review` | A code change raises the booking limit to 30 days. FR-1 still says 14, and the spec isn't in the diff. | It edits nothing and lists FR-1 as a problem in this change. |

## Running them

From this skill's folder:

```bash
claude plugin eval . --scaffold --allow-tools Write,Edit,Bash --judge-model sonnet -j 4
```

- `--scaffold` lets each case's `place-files.sh` run. Without it, the agent gets an empty folder.
- `--judge-model sonnet` sets the judge. It's Haiku by default. Anthropic's guide for writing these
  evals recommends a Sonnet-class judge.
- Each case runs 3 times with the skill and 3 times without it, by default. `--runs <n>` changes
  that, and `--ablation none` skips the runs without the skill.
- `--tag <tag>` runs the cases with that tag, such as `--tag review-roles`. Given more than one
  tag, it runs the cases that have any of them, not all of them.
- `--case <name>` runs one case, and takes a glob, such as `--case 'review-*'`. With `--tag`, a
  case has to match both, so `--tag review-roles --case 'review-*'` runs that group's reviewer
  cases.
- `--model <model>` overrides every case's `model`.
- `-j <n>` runs up to n agent runs at once, from 1 to 8. It's 1 by default, which is slow, so use at
  least 4. It can only be set on the command line.
- `--keep-temp` keeps each run's folder, so you can see what the agent did.

These are real, billed model runs.
