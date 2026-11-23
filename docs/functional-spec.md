# Functional spec

The functional spec: what the app should do, in the user's terms. Requirements are in GEARS, with
`FR` IDs. It never links to other docs. Other docs, prompts and code point to its IDs.

## F-SEC-1. Terms

- **Board.** A project's GitHub project board.
- **Declined finding.** A finding that the implementer chose not to fix.
- **Factory.** The app this spec describes, which does a project's work from its issues and docs.
- **Finding.** A problem that the quality reviewer reports in a run's work.
- **Implementation loop.** The part of the factory that makes the changes an issue asks for and
  reviews them.
- **Implementer.** The agent that makes a run's changes and handles the findings.
- **Issue.** A GitHub issue in a project's repo.
- **Owner.** The person the factory does a project's work for.
- **PR.** A GitHub pull request in a project's repo.
- **Project.** A piece of software the factory builds, with its own GitHub repo and board.
- **Quality reviewer.** The agent that reviews a run's work.
- **Round.** One review of a run's work, then the implementer's answer to its findings.
- **Run.** One use of the implementation loop on one issue, from its start to its end.

## F-SEC-2. Starting a run

**FR-1.** When the implementation loop's command is called with a project's repo and an issue
number, the implementation loop shall start a run on that issue.

**FR-5.** When a run starts, the implementer shall do the work the issue asks for.

## F-SEC-3. How a run goes

**FR-25.** The quality reviewer shall be a different agent from the implementer.

*Why:* an author's own check of its work is thin, so a separate reviewer is the real check. That
check is what lets the owner trust work no person watched.

**FR-6.** The implementation loop shall give a run the number of rounds its command sets, else the
number the project sets, else 3.

**FR-23.** When a round starts, the quality reviewer shall review the run's work.

**FR-24.** When the implementer gets a round's findings, the implementer shall fix each finding or
decline it with a reason.

*Why:* the implementer owns the work, and a review is feedback to it. A finding can be wrong, or
can question a choice the implementer made on purpose, and then the implementer declines it.

**FR-7.** The implementation loop shall go through every one of the run's rounds, even when the
quality reviewer finds nothing.

*Why:* Claude Code's stock code review almost always returns findings, since it aims for at least
five. A stop when a review finds nothing would rarely happen, and a fixed number of rounds is the
simplest rule.

## F-SEC-4. Statuses and comments

**FR-9.** When a run starts, the implementation loop shall move the issue to In development
on the board.

**FR-10.** When a run opens its PR, the implementation loop shall move the issue to In review on
the board.

**FR-11.** When a run ends without opening a PR, the implementation loop shall move the issue to
Needs attention on the board.

*Why:* Needs attention is the status of an issue that waits on the owner before work on it can go
on.

*Accepted gap:* when the implementation loop itself stops partway, such as when its machine shuts
down, nothing moves the issue, and it stays In development. This is accepted because the owner
starts each run by hand, so they see when one stops.

**FR-12.** When a run ends without opening a PR, the implementation loop shall post a comment on
the issue that gives the reason.

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

**FR-26.** The description of a run's PR shall list each choice the implementer made on a point the
issue and the docs left open, with the text it's about, what was unclear and what it chose.

*Why:* the implementer has no one to ask during a run, so the owner checks each such choice at the
PR.

**FR-22.** The description of a run's PR shall list each decision the implementer wrote into a spec
with no reason, as a question for the owner that quotes the decision and suggests a reason where
the implementer has one.
