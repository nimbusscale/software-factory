# GitHub work

The standards for working with a project's GitHub issues, its board and its PRs: what each kind of
issue holds, what a parent issue is, how an issue's title is written, how issues are linked, which
labels an issue has, what the board's statuses mean, who moves an issue's status, how an issue is
updated and closed, how a branch is named, and how a PR's title and description are written.

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

## A parent issue

An issue with sub-issues is a parent. A parent is always an interactive issue, with the
`interactive` label and an interactive issue's two sections. Its Goal says what the whole piece of
work delivers, and can hold the plan and what's left out of it. Its Acceptance criteria say when
the whole piece is done. No label marks a parent, since GitHub shows its sub-issues.

An issue becomes a sub-issue when the owner asks for it. In a session, the agent can also suggest
one, such as a task that hands a part of the session's work to the factory. It raises the idea
with the owner, and makes the sub-issue once the owner agrees. When the issue that would be the
parent isn't interactive, its kind label changes to `interactive`.

A sub-issue can be any kind of issue. Its body doesn't name its parent, such as with "Part of
#123", since GitHub shows the parent.

*Why:* breaking work down, and handing parts of it to the factory, are done in a session with the
owner.

## An issue's title

An issue's title is a plain sentence that says what the work changes, such as "Keep each run's
transcripts in a run folder". A question issue's title is the question, ending in "?", such as
"Can a task issue's acceptance criteria list technical requirements?" The title doesn't name the
issue's kind, such as with "Question:", since its label does.

## Where an issue or a comment came from

An issue or a comment doesn't open with a line saying where it came from, such as "From an
interactive session on <date>".

*Why:* an issue an agent opened on its own judgment has the `agent-created` label. Every other
issue came from a person's session.

## Blocked-by links

Mark an issue on GitHub as blocked by another, of any kind, only when the other has to be done
before this one can start. An order that's only preferred isn't a block. A comment can say why an
issue waits, but the link has to be there too.

*Why:* a wait written only in a comment doesn't show on the issue's page or on the board.

## Labels

Every issue has exactly one kind label: `task`, `bug`, `question` or `interactive`. An issue an
agent opens on its own judgment also has `agent-created`.

The `factory` label says the factory may take the issue. Only a `task` or a `bug` can have it, and
a new issue doesn't get it. The owner adds it.

*Why:* once the factory starts runs on its own, an issue in Ready with the `factory` label starts a
run without anyone asking. So the label goes on only when the owner chooses to hand the issue over.

When the owner takes an issue that has the `factory` label back to work on it, such as after a run
stops in Needs attention, the label comes off. In a person's session, the agent removes it when it
starts work on the issue.

*Why:* the board has one status, In development, for an issue someone is working on. The label is
what says the factory is working on it. A labeled issue the owner is working on would look like a
run is going.

## The board's statuses

The statuses the factory uses are on the board, and each status's description says what
it means. Read them there, and don't list them anywhere else.

## Moving an issue's status in a person's session

In a person's session, the agent moves the issue it works on to In development when it starts work
on it, and to In review when it opens the issue's PR. It does this without being asked. When the PR
merges and closes the issue, the board moves it to Done on its own.

When it moves an issue to In development, it also moves the issue's parent to In development, if
the parent is in Backlog or Ready. After that, only the owner moves the parent.

*Why:* the board is where the owner sees what's being worked on. Nothing else moves the issue to In
review when its PR opens, or its parent to In development. A parent left in Backlog gets lost there.
It moves only from Backlog or Ready, so it never overrides a status the owner set.

## Updating an issue

An issue with the `factory` label counts as started once it's in Ready, since a run can take it at
any time. From then on, change it only by moving its status on the board and by posting comments.
Never edit its title or body. Anything that comes up while the work goes on, such as why a run
stopped, goes in a comment.

If such an issue has to change, stop the work on it and start over. Move the issue back to
Backlog, stop any run on it, edit it, and move it back to Ready.

*Why:* a run reads the issue when it starts, and nothing can tell it about a change after that.

Any other issue can be edited at any time. In a person's session, the agent edits it when the
owner asks.

## Closing an issue without a PR

Most issues close when a PR with `Closes` for them merges. When an issue is closed any other way,
pick the close reason that fits, and post one comment that says why:

- **Completed:** the work got done without a PR that closes the issue, such as in a PR that does
  only part of it. The comment links what did the work, such as "Done in #123."
- **Not planned:** the issue won't be done as written. It was replaced, folded into another issue
  or dropped, or it repeats another issue. The comment says why in one sentence, and links the
  issue that holds the work now, if there is one, such as "Replaced by #123, which checks the
  prompt against real bugs instead."

Don't use GitHub's "duplicate" reason, since `gh issue close` can't set it.

*Why:* without the comment, nothing says where the work went.

## A branch's name

In a person's session, the branch for an issue's work is named `issue-<number>-<slug>`, such as
`issue-123-run-transcripts`. A branch for work with no issue is named with the slug alone. A run
names its own branches.

*Why:* the name shows which issue a branch or a worktree is for, in a list of them.

## A PR's title and description

These rules are for a PR an agent writes in a person's session. A PR the factory's code opens,
such as a run's PR, follows the requirements for it.

A PR's title is its issue's title. When the PR does only part of the issue, its title says what
the PR does.

The description's first line is `Closes #<number>`, on its own, with one such line for each issue
the PR closes. When the PR merges, GitHub closes each of those issues, and the board moves them to
Done. A PR that does only part of an issue puts `Part of #<number>` there instead, which closes
nothing. A PR with no issue has no such line. A PR can close a question issue, when the PR writes
the question's answer down.

After that line comes the summary. It says, in a few plain sentences, what the change does. Write
it for someone skimming the project's PRs, or reading a summary of the work that was merged. Don't
copy the issue's Do or its acceptance criteria into the description. The PR links to its issue, and
a copy drifts from it.

After the summary, the description has these two sections, in this order, each under a `##`
heading of that name. Each one is there only when it has something in it:

- **Decisions on open points:** each call the work made that the issue left open. A disagreement
  between a doc and the code that the owner chose to leave in place is one of them.
- **Different from the issue:** each place the work departs from the issue, including each change
  the issue didn't ask for.

Nothing else goes in the description, such as what the tests cover or which spec items changed,
since the diff shows those. Declined review findings go in a comment, as "A factory review of a PR
made outside a run" says.

*Why:* the owner remembers the session a PR came from. An agent that later has to work out what
happened and why has only the PR, and these two sections hold what the diff can't show.

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
