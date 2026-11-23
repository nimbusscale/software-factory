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
- **Round.** One review of a run's work by the quality reviewer, then the implementer's answer to
  its findings.
- **Run.** One use of the implementation loop on one issue, from its start to its end.
- **Turn cap.** The most turns an agent may take.

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

**FR-29.** When the command or the project sets fewer than 1 round, the implementation loop shall
refuse to start the run, and say why.

**FR-27.** The implementation loop shall give the implementer and the quality reviewer each the turn
cap the project sets for it, else the factory's default for it, each time it starts or resumes
that agent.

**FR-28.** When the implementer or the quality reviewer reaches its turn cap, the implementation
loop shall end the run.

**FR-23.** When the implementer finishes the work the issue asks for, the implementation loop shall
start the run's first round.

**FR-24.** When the implementer gets a round's findings, the implementer shall fix each finding or
decline it with a reason.

*Why:* the implementer owns the work, and a review is feedback to it. A finding can be wrong, or
can question a choice the implementer made on purpose, and then the implementer declines it.

**FR-7.** While the run has rounds left, when a round ends, the implementation loop shall start the
next round.

## F-SEC-4. The board and the issue's comments

**FR-9.** When a run starts, the implementation loop shall show on the board that the issue is
being worked on.

**FR-10.** When a run opens its PR, the implementation loop shall show on the board that the
issue's PR is ready for the owner.

**FR-11.** When a run ends without opening a PR, the implementation loop shall show on the board
that the issue needs the owner before work on it can go on.

*Accepted gap:* when the implementation loop itself stops partway, such as when its machine shuts
down, the board still shows the issue as being worked on. This is accepted because the owner
starts each run by hand, so they see when one stops.

**FR-12.** When a run ends without opening a PR, the implementation loop shall post a comment on
the issue that gives the reason.

## F-SEC-5. The PR

**FR-15.** When a run's last round ends, the implementation loop shall open a PR for the run's
work.

*Scenario:* Given a run with 2 rounds, when the run starts, then the implementer does the work,
the quality reviewer reviews it, the implementer answers the findings, the quality reviewer
reviews those changes, the implementer answers again, and the PR opens with no review of that
last answer.

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
