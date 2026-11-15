# Evaluations for writing-project-docs

Each folder here is one test case, in the layout `claude plugin eval` reads. A case gives a fresh
agent one small task, in a throwaway repo that the case's scaffold script builds. Then graders
check what the agent produced.

## A case folder

- `prompt.md`: run settings, then the task exactly as a user would type it. `plugins: ["../.."]`
  points the runner at this skill's folder.
- `case.yaml`: the case's name, a plain description of a good result, and the scaffold script.
- `place-files.sh`: builds the repo the agent works in, as a git repo, from `files/`.
- `files/`: the input files.
- `graders/`: one check per file. Each is a statement about the result that's true or false.
  `type: llm` means a judge model decides. `focus` says what the judge reads: here, the spec the
  agent wrote or edited.

## Cases

| Case | Task | Tests |
|---|---|---|
| `review-term-citations` | Review a change that adds five terms, and fix it. | Terms cite only when the meaning depends on a rule. |
| `write-term-citations` | Write a functional spec from planning notes. | The same rule, from the writer's side. |

## Running them

From this skill's folder:

```bash
claude plugin eval . --scaffold --allow-tools Write,Edit,Bash
```

- `--scaffold` lets each case's `place-files.sh` run. Without it, the agent gets an empty folder.
- Each case runs 3 times with the skill and 3 times without it, by default. `--runs <n>` changes
  that, and `--ablation none` skips the runs without the skill.
- `--case <name>` runs one case. `--judge-model <model>` changes the judge, which is Haiku by
  default.
- `--keep-temp` keeps each run's folder, so you can see what the agent did.

These are real, billed model runs.
