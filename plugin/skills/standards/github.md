# GitHub work

The standards for working with a project's GitHub issues, its board and its PRs: what each kind of
issue holds, which labels an issue has, what the board's statuses mean, who moves an issue's
status, how an issue is updated, and how the summary in a PR's description is written.

## A task issue

A task issue is the kind of issue the factory's implementation loop takes. It has the `task` label.
Its body has these four sections, in this order, each under a `##` heading of that name:

- **Why:** what the work is for, in a few sentences.
- **Design:** what the work has to follow, other than the requirements it meets. That's the
  decisions and code standards it follows, the requirements it has to fit that other work meets,
  and pointers to the blueprint sections it follows, by file and heading.
- **Do:** what to change, specific to this issue.
- **Acceptance criteria:** the functional and technical requirements the work must meet. List each
  functional requirement the work meets in full. List a technical requirement when the work meets
  it, such as work that builds one part of the system, which meets no functional requirement on its
  own. A requirement counts as met when its tests pass. A test the work needs that doesn't exist
  yet is written as part of the work.

An item goes in one of the two sections, never both. A requirement the work meets goes in
Acceptance criteria, which already tells whoever does the work to build to it. A requirement the
work only has to fit goes in Design. For example, the work that writes an agent's prompt has to
fit a requirement for how that agent handles its input, when other work hands it the input and
the tests for the requirement run there.

Each spec item in Design or Acceptance criteria is listed by its ID and its text as it stood when
the issue was written, with nothing under it, such as its Why:

```markdown
- **FR-27.** The quality reviewer shall mark each finding as an important finding, a pre-existing
  finding, a nit or a finding to check.
```

List each item on its own, not a whole section by its section ID, so each one can be quoted.

*Why:* the owner reads issues on GitHub, often on a phone, where an ID alone doesn't say what the
item is. The text also shows what the item said when the issue was written. If the spec changed
before the work starts, the two differ, and the spec wins.

## A bug issue

A bug issue is a task issue for something that doesn't work as it should. It has the `bug` label
in place of `task`. Its body has these five sections, in this order, each under a `##` heading of
that name:

- **What happened:** what was seen, with links to what shows it, such as a session, a trace or a
  failed check.
- **Expected:** what should have happened instead.
- **Design**, **Do** and **Acceptance criteria:** as in a task issue. Acceptance criteria includes
  the failing case, written as behavior, such as "Running `make check` on a fresh clone passes."

It has no Why section, since What happened and Expected say why the work is needed.

*Why:* agents and code open many bugs, and a fixed shape prompts them for the evidence.

## A question issue

A question issue holds a question that has to be settled before some work can start. It generates
no code. It has the `question` label, so questions can be told apart from work at a glance. Its body
has these three sections, in this order, each under a `##` heading of that name:

- **Question:** the question, in a sentence or two.
- **Context:** what's known so far, and which issues the answer changes.
- **Options:** the answers weighed so far, or "None yet."

Each issue that waits on the answer is marked on GitHub as blocked by the question issue. When the
question is answered, the answer is written where it belongs, such as in a spec or in these
standards, and the question issue is closed.

*Why:* a question written only in a comment or a conversation is easy to miss. The agent that
picks up the waiting work may never see it, and nothing shows the owner what's waiting on it.

## An interactive issue

An interactive issue is work the owner does in a session with an agent, such as settling a set of
questions or doing research. The factory never takes one. It has the `interactive` label. Its body
has these two sections, in this order, each under a `##` heading of that name:

- **Goal:** what the session is for, in whatever form helps. It can hold links to read, or a list
  of items to go through, or neither.
- **Acceptance criteria:** the conditions that say the work is done, so it's clear when to close
  the issue. They're plain conditions, such as "the decisions are in the spec", not requirements.

*Why:* an interactive issue can be whatever the owner needs it to be, so its shape stays small. The
owner is in the session, so the agent can ask about anything the issue doesn't say.

## Labels

Every issue has exactly one kind label: `task`, `bug`, `question` or `interactive`. An issue an
agent opens on its own judgment also has `agent-created`.

The `factory` label says the factory may take the issue. Only a `task` or a `bug` can have it, and
a new issue doesn't get it. The owner adds it.

*Why:* once the factory starts runs on its own, an issue in Ready with the `factory` label starts a
run without anyone asking. So the label goes on only when the owner chooses to hand the issue over.

## The board's statuses

The statuses the factory uses are on the board, and each status's description says what
it means. Read them there, and don't list them anywhere else.

## Moving an issue's status in a person's session

In a person's session, the agent moves the issue it works on to In progress when it starts work on
it, and to In review when it opens the issue's PR. It does this without being asked. When the PR
merges and closes the issue, the board moves it to Done on its own.

When it moves an issue to In progress, it also moves the issue's parent to In progress, if the
parent is in Backlog or Ready. After that, only the owner moves the parent.

*Why:* the board is where the owner sees what's being worked on. Nothing else moves the issue to In
review when its PR opens, or its parent to In progress. A parent left in Backlog gets lost there.
It moves only from Backlog or Ready, so it never overrides a status the owner set.

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

## A factory review of a PR made outside a run

A PR made outside a run, such as in a person's session, can get the factory's review from the
review command. The agent that made the PR starts it from a checkout of the factory's repo:

```bash
bash tools/run-sfe.sh --review <owner/name> <PR number>
```

It takes several minutes, so run it in the background. When it ends, it prints the findings for
the PR's author to answer, and posts the rest of the review as a comment on the PR.

Fix each finding it prints, or decline it with a reason, as the factory's implementer does. Push
the fixes to the PR's branch. Then post one comment on the PR that lists each finding you
declined, by its ID, such as `R1-F2`, with the reason. Don't put the declined findings in the PR's
description.

*Why:* the comment sits right after the review it answers, so the owner reads each review and its
answer in order. The PR's description stays as its author wrote it.
