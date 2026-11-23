# Technical spec

The technical spec: what the system must achieve that a user wouldn't see (`TR`, in GEARS), the
architecture (`AD`) and design (`TD`) decisions, each with its reason, and the code standards
(`CS`), that new code could follow or break from anywhere. Decisions carried out in one place in
the code are comments there instead.

## T-SEC-1. Terms

- **Doc standards.** The rules a project's docs are written and checked by.
- **Implementer.** The role that does a run's work and handles the findings.
- **Quality reviewer.** The role that reviews the quality of a run's work.
- **Result schema.** The shape of a role's result.
- **Review diff.** The part of a run's work that the quality reviewer reviews in a round (TR-2,
  TR-3).
- **Role.** The implementer or the quality reviewer.
- **Run branch.** The git branch that holds a run's work.
- **Session.** One agent's conversation in the Claude Agent SDK, with the context it has built up.
- **Workflow.** The code that carries out the implementation loop.
- **Working copy.** The clone of the project's repo that a run works in.

## T-SEC-2. Architecture decisions

**AD-1.** The workflow is a Claude Agent SDK app.

*Why:* rounds and checked results are too much logic for shell commands around `claude -p`, the
way a shell pipeline grows into a real program.

**AD-11.** The workflow is a plain process that any machine can host, such as the owner's computer
or a cloud VM, and it doesn't depend on GitHub Actions to operate.

*Why:* a local process is quicker to change and try again than a workflow in GitHub Actions.

**AD-10.** A run's work is done by the implementer and reviewed by a separate quality reviewer, in
rounds.

*Why:* an author's own check of its work is thin, so a separate reviewer is the real check.

**AD-3.** The workflow starts every role itself, as its own Agent SDK call, never as another
agent's subagent.

*Why:* an agent can skip a review it's told to start, and the workflow's code can't. An implementer
that briefs its own quality reviewer also tends to explain what it did and why, so the review isn't
fresh.

**AD-4.** The workflow chooses each next step of a run from the roles' results, among paths written
in its code.

*Why:* a model can skip a step or stop early, so the steps and the round count belong in code.

**AD-5.** Only the workflow has access to GitHub.

*Why:* the workflow then decides what each role sees. Keeping text from a role, such as the
author's account from the quality reviewer, is a choice of what the workflow passes in, not a rule
the role has to follow.

**AD-6.** Every role uses Opus.

*Why:* the implementation loop is made to work before it's made cheaper.

**AD-12.** A role gets its guidance from the project's docs, which its prompt or the project's
CLAUDE.md points it to.

*Why:* one agent works in one repo, so a skill adds complexity and little else. Pointing the agent
at the docs does the same job.

## T-SEC-3. Code standards

How all code is written, with examples where they help. A standard gets a Why only when its reason
isn't clear from it.

## T-SEC-4. A run's rounds and roles

**TR-1.** The workflow shall act on a role's result only after checking it against that role's
result schema.

**TD-7.** Each role hands back its result as the Agent SDK's structured output, with the role's
result schema as its schema. This meets TR-1.

*Why:* the SDK makes the agent's answer fit the schema, asking it to try again when it doesn't, so
the factory needs no tool or hook of its own for this.

**TR-2.** While a run is in its first round, the review diff shall be everything the run has
changed.

**TR-3.** While a run is in a round after its first, the review diff shall be only what changed
since the previous round's review.

*Why:* it keeps a fix from pulling more of the code base into review.

**TR-4.** The quality reviewer shall start each round fresh, with access only to the body of the
run's issue, the docs and code in the working copy, the round's review diff, and the findings from the run's
earlier rounds.

*Why:* the author's reasons sway a review, such as in commit messages, the PR's description or the
implementer's account of its work. A reviewer that reads them may accept a choice because it's
explained, or look only where the author points. A fresh reviewer that couldn't see them has found
bugs the author missed.

**TR-5.** The implementer shall be the only role that changes the working copy.

**TR-8.** When the implementer finishes the work the issue asks for, or its changes in answer to a
round's findings, the implementer shall check its own change, including the doc standards' checks
on each doc it changed.

**TR-9.** When the implementer's own check finds a problem, the implementer shall fix it before it
hands back its result.

**TR-7.** When the implementer gets a round's findings, the implementer shall either fix each
finding or decline it with a reason.

*Why:* not every finding holds up. In one project's reviews, about 10% of findings were wrong, and
23% were design choices.

**TD-3.** The implementer keeps one session for the whole run, and resumes it in each round. This
meets TR-7.

*Why:* handling a finding needs the implementer's own reasons, such as why it made a choice the
finding questions. Without them, a fix can undo a decision.

## T-SEC-5. GitHub and the PR

**TD-4.** The implementer's result holds the text that FR-17, FR-18 and FR-19 call for, which the
workflow puts in the PR's description.

**TD-6.** The workflow writes the line of the PR's description that FR-16 calls for.

**TD-5.** The implementer commits its work to the run branch in the working copy. This meets FR-15.
