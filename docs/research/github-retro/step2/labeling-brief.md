# Labeling brief for step 2

You are sorting the text of GitHub issues and pull requests from a finished project,
road-trip-agent, into kinds. This is research for a retrospective on how issues and PRs were
written. You only read and label. Don't change anything outside `step2/labels/`, and don't call
GitHub: everything you need is in two JSON files.

## Background

road-trip-agent was a one-person learning project built mostly by Claude Code agents. Work was
tracked in GitHub issues from 2026-10-19. Each issue used a template with these sections: Why,
Design, Open questions, Do, Done when, Ends in, Settled in. When an open question was settled, the
rule was to strike it out (`~~...~~`) and write the answer and when it was settled. A PR
description was supposed to hold only the task, copied word for word from the issue's Do and Done
when, plus each Done when result. The implementer's decisions went in a separate PR comment, the
"decisions comment", which also listed things set aside.

## Your input

All paths are relative to `/home/jjk3/PycharmProjects/personal/software-factory/docs/research/github-retro/`.

- `step2/issue-blocks.json`: keyed by issue number. Each issue has `blocks`: the final issue body
  split into paragraphs and top-level list items. Each block has an `id`, its `section`, `words`,
  `text`, `first_seen` (when it first appeared in the body), `after_first_pr` (true if it was added
  after the first PR for the issue opened), and `struck`.
- `step2/pr-blocks.json`: keyed by issue number. `issue_comments` are the issue's comments, each
  with an `id`. `prs` are the issue's PRs, each with `description` blocks (ids `P<n>-d<i>`) and
  `decisions` blocks (ids `P<n>-c<i>`), plus a summary of other comments.

## Kinds

Give every block, comment and PR block exactly one kind:

- `task`: what to build or do, or how to tell it's done. Do items, Done when items, and design
  pointers that say which doc section to follow.
- `reason`: why the work matters, or why a choice was made.
- `open-question`: a question still open.
- `settled-question`: a struck-out question with its answer, or a question whose answer is written
  under it.
- `decision`: a settled choice stated on its own, outside a question. Example: "Decided by Joe on
  2026-11-10, in chat: ...". Each item in a decisions comment is usually this.
- `status`: progress or state. Examples: "Part 1 merged in #103", "As of 2026-11-08, the file has
  neither test", "Starts once #47 is merged".
- `result`: data or findings from running something, such as a run's numbers or a comparison.
- `log`: a step-by-step record of what was done or tried, such as a list of runs.
- `history`: what something used to be, or how the text got here. Example: "They were the
  servers' instructions until #117 removed them."
- `copy`: text restated from somewhere else: a design doc, the issue, or another PR. A PR
  description block that repeats the issue's Do or Done when is `copy`. A Done when block with its
  result added is `result`.
- `set-aside`: something left for later, and where it went.
- `boilerplate`: template text that says nothing specific to the work, such as "Ends in: A PR."
- `other`: anything else. Say what in `note`.

When a block mixes kinds, pick the one most of its words are, and name the second in `note`.

## Two more labels

- For each **issue block**, `needed`: would a fresh agent need this block to do the work well, if
  it started from this issue with only the repo? Answer `yes`, `no`, or `unsure`. A settled
  question's answer can be needed even when the question isn't. History and status are usually
  `no`.
- For each **decisions comment block** that is a decision, `doc`: `yes` if it says which design doc
  or section it was written into, else `no`.

## Output

For each issue you're given, write `step2/labels/<issue number>.json`:

```json
{
  "issue": 209,
  "labels": {
    "I209-0": {"kind": "reason", "needed": "yes", "note": ""},
    "IC209-0": {"kind": "set-aside", "note": ""},
    "P290-d0": {"kind": "copy", "note": ""},
    "P290-c3": {"kind": "decision", "doc": "no", "note": ""}
  },
  "notes": "Four to eight plain sentences."
}
```

Every id in the input for that issue must appear in `labels`. Check this before you finish.

`notes` says, in plain words: what the issue was for, how its text grew and when, which kinds take
most of its words, and anything surprising. Then answer any of these the issue bears on, with the
block ids as evidence:

- Were the answers under struck-out questions part of the task, or history?
- Did the PR description add anything the issue didn't already say?
- What did the decisions comment hold, and how much of it was written into a doc?
- Where did results and status go: the body, comments, or the PR?

Finish with a two-line reply: the files you wrote, and any id you couldn't label.
