# Technical spec

The technical spec: what the system must achieve that a user wouldn't see (`TR`, in GEARS), the
architecture (`AD`) and design (`TD`) decisions, each with its reason, and the code standards
(`CS`), that new code could follow or break from anywhere. Decisions carried out in one place in
the code are comments there instead.

## T-SEC-1. Terms

- **Doc standards.** The rules a project's docs are written and checked by.
- **Result schema.** The shape of a role's result.
- **Review copy.** The copy of the run's work that the quality reviewer works in.
- **Review diff.** The part of a run's work that the quality reviewer reviews in a round (TR-2,
  TR-3).
- **Role.** An agent that the workflow starts to do one task in a run.
- **Run branch.** The git branch that holds a run's work.
- **Session.** One agent's conversation in the Claude Agent SDK, with the context it has built up.
- **Workflow.** The code that carries out the implementation loop.
- **Working copy.** The checkout of the project's repo that a run works in.

## T-SEC-2. Architecture decisions

**AD-1.** The workflow is a Claude Agent SDK app.

*Why:* rounds and checked results are too much logic for shell commands around `claude -p`, the
way a shell pipeline grows into a real program.

**AD-4.** A run is a series of steps written in the workflow's code. Each step is either the
workflow's own code or a role. A role does its one task on its own and hands back its result, and
the workflow's code picks the next step from that result.

*Why:* an agent may skip a step, do one out of order or stop early, and code can't. Keeping
judgment inside a role's task leaves the models doing the work they're good at, and keeps the rest
of the run predictable.

**AD-3.** The workflow starts every agent in a run, and each one is a role.

*Why:* an agent can skip a review it's told to start, and the workflow's code can't. An implementer
that briefs its own quality reviewer also tends to explain what it did and why, so the review isn't
fresh.

**AD-13.** The workflow is written in Python.

*Why:* the workflow has no client to share code with, and building it in Python shows the owner
how such a workflow looks in that language.

**AD-11.** The workflow is a plain process that any machine can host, such as the owner's computer
or a cloud VM.

*Why:* a local process is quicker to change and try again than a workflow in GitHub Actions.

**AD-5.** Only the workflow has access to GitHub.

*Why:* the workflow then decides what each role sees. Keeping text from a role, such as the
author's account from the quality reviewer, is a choice of what the workflow passes in, not a rule
the role has to follow.

**AD-6.** Every role uses Opus.

*Why:* the implementation loop is made to work before it's made cheaper.

**AD-12.** A role learns the project's rules from the project's docs, which its prompt or the
project's CLAUDE.md points it to.

*Why:* one agent works in one repo, so a skill of the project's own adds complexity and little
else. Pointing the agent at the docs does the same job.

## T-SEC-3. Code standards

How all code is written, with examples where they help. A standard gets a Why only when its reason
isn't clear from it.

## T-SEC-4. A run's rounds and roles

**TR-1.** The workflow shall act on a role's result only after checking it against that role's
result schema.

**TR-13.** When a role hands back no result, or a result that doesn't fit its result schema, the
workflow shall end the run.

**TD-7.** Each role hands back its result as the Agent SDK's structured output, with the role's
result schema as its schema. This meets TR-1.

*Why:* structured output is the Agent SDK's own way to get a result in a set shape, so the workflow
builds nothing of its own to get one.

**TR-2.** While a run is in its first round, the review diff shall be the work the implementer did
before that round.

**TR-3.** While a run is in a round after its first, the review diff shall be the changes in the
implementer's answer to the previous round's findings.

*Why:* the first round reviews all the work, so what it doesn't flag needs no more review. A later
round only has to check the changes made in answer to the previous round's findings.

**TR-16.** When a round's review diff is empty, the workflow shall end the round without starting
the quality reviewer or the implementer.

**TR-14.** The quality reviewer shall start each round in a new session.

**TD-11.** The quality reviewer runs Claude Code's stock code review on the round's review diff.
This meets FR-23.

*Why:* the factory uses stock parts where it can, and one review process that works for any
project, not one tuned to each project.

**TR-4.** The quality reviewer shall have access only to the body of the run's issue, the docs and
code as they stand when the round starts, the round's review diff, and the findings from the run's
earlier rounds.

*Why:* the author's reasons sway a review, such as in commit messages, the PR's description or the
implementer's account of its work. A reviewer that reads them may accept a choice because it's
explained, or look only where the author points. A fresh reviewer that couldn't see them has found
bugs the author missed.

**TD-13.** The review copy is a git repo with one commit, which holds the docs and code as they
stood before the round's review diff, and the review diff on top as changes not yet committed.
This meets TR-4.

*Why:* the quality reviewer can run the tests in it, and the implementer's commit messages aren't
in it.

**TR-12.** The findings from earlier rounds that the quality reviewer gets shall mark each declined
finding as declined, with no reason.

*Why:* without the mark, the quality reviewer raises a declined finding again in every round.

**TR-5.** The implementer shall be the only role that changes the working copy.

**TR-15.** The workflow shall deny every role the shell commands `gh`, `git push` and `git commit`.

**TR-11.** The implementer shall have access only to the body of the run's issue, the working copy,
the findings the workflow gives it, and the web through web search and web fetch.

*Why:* an agent in the implementation loop is short-lived and may work on any machine, so anything
it needs has to be written where every agent can read it, not in Claude Code's memory.

**TR-8.** When the implementer finishes the work the issue asks for, or its changes in answer to a
round's findings, the implementer shall check its own change.

**TR-9.** When the implementer's own check finds a problem its change caused, the implementer shall
fix it before it hands back its result, unless the doc standards say the problem isn't the
implementer's to fix.

**TD-3.** The implementer keeps one session for the whole run, and resumes it in each round. This
meets FR-24.

*Why:* handling a finding needs the implementer's own reasons, such as why it made a choice the
finding questions. Without them, a fix can undo a decision.

## T-SEC-5. GitHub and the PR

**TD-4.** The implementer's last result holds the text that FR-17, FR-19, FR-22 and FR-26 call
for, which the workflow puts in the PR's description.

*Why:* only the implementer knows what it changed.

**TD-12.** The workflow keeps each declined finding and its reason from every one of the
implementer's results, and lists them in the PR's description. This meets FR-18.

*Why:* a finding declined in an early round isn't in the implementer's last result, and the
workflow keeps the declined findings anyway, for the quality reviewer's list (TR-12).

**TD-6.** The workflow writes the line of the PR's description that FR-16 calls for.

*Why:* the workflow already has the issue number.

**TD-8.** The workflow commits the implementer's changes to the run branch in the working copy.
This meets FR-15.

*Why:* a commit needs no judgment, so it's a step for the workflow's code (AD-4).

**TD-10.** The workflow makes the commits TD-8 calls for each time the implementer hands back its
result. This meets TR-2 and TR-3.

*Why:* each review diff is then the difference between two commits.

**TD-9.** The message of each commit TD-8 makes is the one the implementer's result holds. This
meets FR-15.

*Why:* the doc standards put a change's history in its commit message, and only the implementer
knows that history.
