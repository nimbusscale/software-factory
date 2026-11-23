# Functional spec

The functional spec: what the app should do, in the user's terms. Requirements are in GEARS, with
`FR` IDs. It never links to other docs. Other docs, prompts and code point to its IDs.

## F-SEC-1. Terms

- **Board.** A project's GitHub project board.
- **Declined finding.** A finding that a run chose not to fix.
- **Factory.** The app this spec describes, which does a project's work from its issues and docs.
- **Finding.** A problem that a review reports in a run's work.
- **Implementation loop.** The part of the factory that does the work an issue asks for.
- **In development.** The issue status of an issue that a run is working on.
- **In review.** The issue status of an issue whose PR is open and waiting on the owner.
- **Issue.** A GitHub issue in a project's repo.
- **Issue status.** An issue's column on the board.
- **Needs attention.** The issue status of an issue that waits on the owner before work on it can
  go on.
- **Open question.** A part of a rule that the issue and the docs leave open, so the work would
  have to choose it.
- **Owner.** The person the factory does a project's work for.
- **PR.** A GitHub pull request in a project's repo.
- **Project.** A piece of software the factory builds, with its own GitHub repo and board.
- **Round.** One review of a run's work, then the changes made in answer to its findings.
- **Run.** One use of the implementation loop on one issue, from its start to its end.
- **Task issue.** An issue written for a run to work on.

## F-SEC-2. Starting a run

**FR-1.** When the implementation loop's command is called with a project's repo and an issue
number, the implementation loop shall start a run on that issue.

**FR-2.** The implementation loop shall start a run only when its command is called, not on its
own, such as when an issue moves on the board.

**FR-3.** The body of a task issue shall have the sections this table shows.

| Section | What it holds |
|---|---|
| Why | What the work is for, in a few sentences. |
| Design | Pointers to the spec items and sections the work follows, by their IDs. |
| Do | What to change, specific to this issue. |
| Acceptance criteria | The functional requirements the work must meet, by their IDs. |

**FR-4.** When a run starts, the implementation loop shall take the issue as it's written, with no
check that it has the sections FR-3 lists.

**FR-5.** When a run starts, the implementation loop shall do the work the issue asks for, meeting
each functional requirement its Acceptance criteria name.

## F-SEC-3. How a run goes

**FR-6.** The implementation loop shall give a run the number of rounds its command sets, else the
number the project sets, else 3.

**FR-7.** The implementation loop shall go through every one of a run's rounds, even when a review
finds nothing.

*Why:* Claude Code's stock code review almost always returns findings, since it aims for at least
five. A stop when a review finds nothing would rarely happen, and a fixed number of rounds is the
simplest rule.

**FR-8.** When a run finds an open question, the implementation loop shall end the run without
opening a PR.

*Why:* a guess written as a rule looks settled to every later reader, and nothing in a doc can
mark it as a guess.

## F-SEC-4. Issue statuses and comments

**FR-9.** When a run starts, the implementation loop shall move the issue to In development.

**FR-10.** When a run opens its PR, the implementation loop shall move the issue to In review.

**FR-11.** When a run ends without opening a PR, the implementation loop shall move the issue to
Needs attention.

**FR-12.** When a run ends without opening a PR, the implementation loop shall post a comment on
the issue that gives the reason.

**FR-13.** When a run ends on an open question, the implementation loop shall give each question in
the comment FR-12 posts, with the text it's about, what's unclear and a suggested answer.

**FR-14.** The implementation loop shall change an issue only by moving its issue status and
posting comments on it, not by editing its body or its labels.

## F-SEC-5. The PR

**FR-15.** When a run's last round ends, the implementation loop shall open a PR for the run's
work.

*Scenario:* Given a run with 3 rounds, when the changes in answer to the third review are made,
then the PR opens with no review of those changes.

**FR-16.** The description of a run's PR shall hold `Closes #<number>`, with the number of the
run's issue.

**FR-17.** The description of a run's PR shall say in a few plain sentences what the run changed.

**FR-18.** The description of a run's PR shall list each declined finding, with the reason it was
declined.

**FR-19.** The description of a run's PR shall name each disagreement between a doc and the code
that the run left in place, by the doc item's ID and the code.

**FR-20.** The implementation loop shall take each run only as far as an open PR, not to a merge.
