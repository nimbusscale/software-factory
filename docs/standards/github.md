# GitHub work

The standards for working with a project's GitHub issues, its board and its PRs: what a task
issue and a question issue hold, what the board's statuses mean, how an issue is updated, and how
the summary in a PR's description is written.

## A task issue

A task issue is the kind of issue the factory's implementation loop takes. Its body has these four
sections, in this order, each under a `##` heading of that name:

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
- **FR-22.** The quality reviewer shall mark each finding as an important finding, a pre-existing
  finding or a nit.
```

List each item on its own, not a whole section by its section ID, so each one can be quoted.

*Why:* the owner reads issues on GitHub, often on a phone, where an ID alone doesn't say what the
item is. The text also shows what the item said when the issue was written. If the spec changed
before the work starts, the two differ, and the spec wins.

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

## The board's statuses

The statuses the factory uses are on the project's board, and each status's description says what
it means. Read them there, and don't list them anywhere else.

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
