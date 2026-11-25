# Functional spec

The functional spec: what the app should do, in the user's terms. Requirements are in GEARS, with
`FR` IDs. It never links to other docs. Other docs, prompts and code point to its IDs.

## F-SEC-1. Terms

- **Board.** A project's GitHub project board.
- **Declined finding.** A finding that the implementer chose not to fix.
- **Doc standards.** The rules a project's docs are written and checked by.
- **Dropped candidate.** A possible problem that the quality reviewer looked into and didn't report
  as a finding, such as one whose claim turned out to be false.
- **Factory.** The app this spec describes, which does a project's work from its issues and docs.
- **Finding.** A problem that the quality reviewer reports in a round.
- **Finding to check.** A finding that the quality reviewer can't mark until someone checks a fact
  from outside the project's repo, such as how an outside service answers a request.
- **Implementation loop.** The part of the factory that makes the changes an issue asks for and
  reviews them.
- **Implementer.** The agent that makes a run's changes and handles the findings.
- **Important finding.** A finding about a problem, not a minor one, that the run's work adds,
  makes worse or exposes again.
- **Issue.** A GitHub issue in a project's repo.
- **Nit.** A finding about a minor problem that the run's work adds, such as code that could be
  cleaner, or a crash that only an unlikely input causes.
- **Owner.** The person the factory does a project's work for.
- **PR.** A GitHub pull request in a project's repo.
- **Pre-existing finding.** A finding about a problem that was there before the run's work, and
  that the work doesn't make worse or expose again.
- **Project.** A piece of software the factory builds, with its own GitHub repo and board.
- **Quality reviewer.** The agent that reviews a run's work.
- **Round.** One review of a run's work by the quality reviewer, and any answer the implementer
  gives to its findings.
- **Run.** One use of the implementation loop on one issue, from its start to its end.
- **Turn cap.** The most turns an agent may take.

## F-SEC-2. Starting a run

**FR-1.** When the implementation loop's command is called with a project's repo and an issue
number, the implementation loop shall start a run on that issue.

**FR-2.** When a run starts, the implementer shall do the work the issue asks for.

## F-SEC-3. How a run goes

**FR-3.** The quality reviewer shall be a different agent from the implementer.

*Why:* an author's own check of its work is thin, so a separate reviewer is the real check. That
check is what lets the owner trust work no person watched.

**FR-4.** The implementation loop shall give a run the number of rounds its command sets, else the
number the project sets, else 3.

**FR-5.** When the command or the project sets fewer than 1 round, the implementation loop shall
refuse to start the run, and say why.

**FR-26.** When a setting the project sets isn't valid, such as a number of rounds that isn't a
whole number, the implementation loop shall refuse to start the run, and say why.

**FR-32.** The implementation loop shall give a run's implementer and quality reviewer the doc
standards only from the factory's own repo, not from the project's repo.

*Why:* the doc standards work as code for the implementer and the quality reviewer, so a change to
them changes how the factory works. A change in a project's repo then can't.

**FR-33.** The implementation loop shall give a run the doc standards on the branch of the
factory's own repo that its command names, else on `main`.

**FR-34.** When the branch that FR-33 picks doesn't exist, or doesn't hold the doc standards, the
implementation loop shall refuse to start the run, and say why.

**FR-35.** The implementation loop shall use the doc standards only as the factory's own repo holds
them, and never change them.

**FR-6.** The implementation loop shall give the implementer and the quality reviewer each the turn
cap the project sets for it, else the factory's default for it, each time it starts or resumes
that agent.

**FR-7.** When the implementer or the quality reviewer reaches its turn cap, the implementation
loop shall end the run.

**FR-8.** When the implementer finishes the work the issue asks for, the implementation loop shall
start the run's first round.

**FR-27.** The quality reviewer shall mark each finding as an important finding, a pre-existing
finding, a nit or a finding to check.

**FR-23.** When a round's review reports an important finding, the implementation loop shall give
the implementer only the round's important findings and nits, not its pre-existing findings.

*Why:* a pre-existing finding is about code the issue didn't ask to change. Each fix of one widens
the change and gives the next round more code to find problems in, so the rounds go on fixing
things the issue never asked for.

**FR-9.** When the implementer gets findings from a round, the implementer shall fix each one or
decline it with a reason.

*Why:* the implementer owns the work, and a review is feedback to it. A finding can be wrong, and
then the implementer declines it. A finding against a decision the implementer made on purpose
isn't wrong for that reason alone, so the implementer keeps the decision only if its reasons
outweigh the finding.

**FR-24.** When a round's review reports no important finding, the implementation loop shall make
that round the run's last.

**FR-10.** While the run has rounds left, when a round ends, the implementation loop shall start the
next round.

## F-SEC-4. The board and the issue's comments

**FR-11.** When a run starts, the implementation loop shall show on the board that the issue is
being worked on.

**FR-28.** While no review in a run has reported a finding to check, when the run opens its PR, the
implementation loop shall show on the board that the issue's PR is ready for the owner.

**FR-29.** While a review in a run has reported a finding to check, when the run opens its PR, the
implementation loop shall show on the board that the issue needs the owner before work on it can
go on.

**FR-13.** When a run ends without opening a PR, the implementation loop shall show on the board
that the issue needs the owner before work on it can go on.

*Accepted gap:* when the implementation loop itself stops partway, such as when its machine shuts
down, the board still shows the issue as being worked on. This is accepted because the owner
starts each run by hand, so they see when one stops.

**FR-14.** When a run ends without opening a PR, the implementation loop shall post a comment on
the issue that gives the reason.

## F-SEC-5. The PR

**FR-15.** When a run's last round ends, the implementation loop shall open a PR for the run's
work.

*Scenario:* Given a run with 2 rounds, where each review reports an important finding, when the
run starts, then the implementer does the work, the quality reviewer reviews it, the implementer
answers the findings, the quality reviewer reviews those changes, the implementer answers again,
and the PR opens with no review of that last answer.

**FR-16.** The description of a run's PR shall hold `Closes #<number>`, with the number of the
run's issue.

**FR-17.** The description of a run's PR shall say in a few plain sentences what the run changed.

**FR-18.** The description of a run's PR shall list each declined finding, with the reason it was
declined.

**FR-19.** The description of a run's PR shall name each disagreement between a doc and the code
that the run left in place, by the doc item's ID and the code.

**FR-20.** The description of a run's PR shall list each decision the implementer made on a point
the issue and the docs left open, with the text it's about, what was unclear and the decision.

*Why:* the implementer has no one to ask during a run, so the owner checks each such decision at
the PR.

**FR-21.** The description of a run's PR shall list each decision from the issue or the docs that
the implementer wrote into a spec with no reason, as a question for the owner that quotes the
decision and suggests a reason where the implementer has one.

**FR-36.** The changes in a run's PR shall hold no file of the doc standards, neither one that
FR-32 gives the run nor one in the project's own copy of them.

**FR-37.** The description of a run's PR shall name the commit of the factory's own repo that the
run's doc standards came from.

*Why:* it labels the run's code with the doc standards it was made by. When a problem shows up in
that code, the owner can find the other runs that used the same doc standards, and check whether
the problem is in their code too.

**FR-25.** When a run opens its PR, the implementation loop shall post a comment on the PR that
lists each nit and pre-existing finding the implementer didn't get.

**FR-30.** When a run opens its PR, the implementation loop shall post a comment on the PR that
lists each finding to check from the run's reviews, with what to check.

**FR-31.** When a run opens its PR, the implementation loop shall post a comment on the PR that
lists each dropped candidate from the run's reviews, with the reason the quality reviewer dropped
it.

*Why:* a candidate dropped by mistake is a real problem that nobody else sees. The list lets the
owner check each call.
