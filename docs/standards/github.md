# GitHub work

The standards for working with a project's GitHub issues, its board and its PRs: what a task
issue holds, what the board's statuses mean, how an issue is updated, and how the summary in a PR's
description is written.

## A task issue

A task issue is the kind of issue the factory's implementation loop takes. Its body has these four
sections, in this order, each under a `##` heading of that name:

- **Why:** what the work is for, in a few sentences.
- **Design:** pointers to the spec items and sections the work follows, by their IDs. Pointers
  only, with no copy of what the items say.
- **Do:** what to change, specific to this issue.
- **Acceptance criteria:** the functional requirements the work must meet, by their IDs. A
  requirement counts as met when its tests pass. A test the work needs that doesn't exist yet is
  written as part of the work.

## The board's statuses

The statuses the factory uses, and what each one means, are in `board-statuses.yaml` in this
folder. That file is the one place they're defined. Don't list them anywhere else.

## Updating an issue

Once work on an issue starts, change it only by moving its status on the board and by posting
comments. Never edit its body.

*Why:* the body is the task. Anything that comes up while the work goes on, such as why a run
stopped, goes in a comment, so the task stays as it was asked.

## The summary in a PR's description

The summary in a PR's description says, in a few plain sentences, what the change does. Write it
for someone skimming the project's PRs, or reading a summary of the work that was merged.

Don't copy the issue's Do or its acceptance criteria into the description. The PR links to its
issue, and a copy drifts from it.
