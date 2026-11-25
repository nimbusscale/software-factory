# Technical spec

The technical spec: what the system must achieve that a user wouldn't see (`TR`, in GEARS), the
architecture (`AD`) and design (`TD`) decisions, each with its reason, and the code standards
(`CS`), that new code could follow or break from anywhere. Decisions carried out in one place in
the code are comments there instead.

## T-SEC-1. Terms

- **Doc standards.** The rules a project's docs are written and checked by.
- **Result schema.** The shape of a role's result.
- **Review copy.** The copy of the run's work that the quality reviewer works in.
- **Review diff.** The part of a run's work that the quality reviewer reviews in a round (TR-3,
  TR-4).
- **Role.** An agent that the workflow starts to do one task in a run.
- **Run branch.** The git branch that holds a run's work.
- **Session.** One agent's conversation, with the context it has built up.
- **SFE.** The container a run happens in. It holds the factory, and the run's copies of the
  project's repo.
- **Workflow.** The code that carries out the implementation loop.
- **Working copy.** The checkout of the project's repo that a run works in.

## T-SEC-2. Architecture decisions

**AD-1.** The workflow is a Claude Agent SDK app.

*Why:* rounds and checked results are too much logic for shell commands around `claude -p`, the
way a shell pipeline grows into a real program.

**AD-2.** A run is a series of steps written in the workflow's code. Each step is either the
workflow's own code or a role. A role does its one task on its own and hands back its result, and
the workflow's code picks the next step from that result.

*Why:* an agent may skip a step, do one out of order or stop early, and code can't. Keeping
judgment inside a role's task leaves the models doing the work they're good at, and keeps the rest
of the run predictable.

**AD-3.** The workflow starts every role. A role may start agents for its own task, but never one
that does another role's task.

*Why:* an agent can skip a review it's told to start, and the workflow's code can't. An implementer
that briefs its own quality reviewer also tends to explain what it did and why, so the review isn't
fresh.

**AD-4.** The workflow is written in Python, with strict type checking.

*Why:* the workflow has no client to share code with, and building it in Python shows the owner
how such a workflow looks in that language. Static typing was what drew the owner to TypeScript,
and strict type checking brings it to Python.

**AD-11.** The quality reviewer's prompt is the factory's own, started from road-trip-agent's
reviewer, which labels each finding with a rubric that gives a rule for each label.

*Why:* a reviewer with a rule for each label marks findings more consistently than one that only
picks among the marks. Road-trip-agent's reviewer also checks each candidate against the code
before it labels it, running code where that settles the claim, so it confirms real findings and
rules out claims that can't happen. Owning the prompt, rather than running Claude Code's stock
code review, keeps a new version of Claude Code from changing the review. The prompt and its rubric
work for any project, so the factory keeps one review process, not one tuned to each project.

**AD-6.** The workflow is a plain process that any machine can host, such as the owner's computer
or a cloud VM.

*Why:* a local process is quicker to change and try again than a workflow in GitHub Actions.

**AD-7.** Only the workflow has access to GitHub.

*Why:* the workflow then decides what each role sees. Keeping text from a role, such as the
author's account from the quality reviewer, is a choice of what the workflow passes in, not a rule
the role has to follow.

*Accepted gap:* the roles run as the same user as the workflow, so a role's shell can read the
GitHub token from the workflow's process. This is accepted while the owner starts each run by
hand.

**AD-8.** Every role uses Opus.

*Why:* the implementation loop is made to work before it's made cheaper.

**AD-12.** Each run happens in its own SFE, which is thrown away when the run ends.

*Why:* the factory in the SFE stays the same for the whole run, so nothing in a project's repo can
change how the factory works, even when the project is the factory's own repo. A project's setup
can install whatever the project needs, and none of it outlives the run. The standards and the
code that uses them also come in one version.

**AD-13.** A role's instructions come only from the factory, and a project's docs and files are
content the role reads.

*Why:* the factory controls how work is done, so a run follows a known version of its prompts and
standards. If a project's files could put instructions into a role's prompt, a team using the
factory could tell the role how to work, not just what to build. The project's CLAUDE.md also
keeps one use, for people working in the repo.

## T-SEC-3. Code standards

How all code is written, with examples where they help. A standard gets a Why only when its reason
isn't clear from it.

**CS-2.** When code goes over a size limit that a check sets, it's split into smaller parts, and
the limit stays the same.

*Why:* the limits keep the code modular. Raising one to fit the code takes that pressure away.

*Examples:*

- A function with too many branches becomes two functions with clear names.
- A file over the line limit becomes two modules, each with one job.

**CS-3.** A fix for a bug comes with a test that fails without the fix and passes with it.

**CS-4.** A test calls an outside service, such as Claude or GitHub, only when it's kept apart
from the tests that run on every commit. The others replace each outside service with a fake.

*Why:* a test that calls Claude costs tokens every time it runs, and its result can change from
one run to the next.

**CS-5.** Names in code use the specs' terms, such as `ReviewDiff` or `review_diff` for a review
diff.

*Why:* a reader finds the code that carries out a spec item by searching for the item's terms.

**CS-6.** Each role has a view file in the repo that shows the role's model, effort, prompt,
tools, permission rules, turn cap and result schema, and a test fails when the file doesn't match
the code.

*Why:* a change to what a role is given then shows in the PR's diff as text a reviewer can read.
In the code, such a change is easy to miss.

## T-SEC-4. A run's rounds and roles

**TR-1.** The workflow shall act on a role's result only after checking it against that role's
result schema.

**TR-2.** When a role hands back no result, or a result that doesn't fit its result schema, the
workflow shall end the run.

**TD-1.** Each role hands back its result as the Agent SDK's structured output, with the role's
result schema as its schema. This meets TR-1.

*Why:* structured output is the Agent SDK's own way to get a result in a set shape, so the workflow
builds nothing of its own to get one.

**TR-3.** While a run is in its first round, the review diff shall be the work the implementer did
before that round.

**TR-4.** While a run is in a round after its first, the review diff shall be the changes in the
implementer's answer to the previous round's findings.

*Why:* the first round reviews all the work, so what it doesn't flag needs no more review.

**TR-5.** When the implementer's answer to a round's findings changes nothing, the workflow shall
make that round the run's last.

**TR-6.** The quality reviewer shall start each round in a new session.

**TR-21.** The quality reviewer shall have access only to the body of the run's issue, the docs and
code as they stand when the round starts, the round's review diff, the findings from the run's
earlier rounds, and the factory's doc standards.

*Why:* the author's reasons sway a review, such as in commit messages, the PR's description or the
implementer's account of its work. A reviewer that reads them may accept a choice because it's
explained, or look only where the author points. A fresh reviewer that couldn't see them has found
bugs the author missed.

**TD-2.** The review copy is a git repo with one commit, which holds the docs and code as they
stood before the round's review diff, and the review diff on top as changes not yet committed.
This meets TR-21.

*Why:* the quality reviewer can run the tests in it, and the implementer's commit messages aren't
in it.

**TR-8.** When a run ends, the workflow shall remove the run's working copy.

**TR-16.** When a run starts, the workflow shall put the run's work on a new run branch, not on
one an earlier run made.

*Why:* a run then never has to delete or overwrite an earlier run's branch, which might still be
needed.

**TR-19.** When an issue is closed, the workflow shall delete each run branch of the issue's runs,
both on GitHub and on the machine the workflow runs on.

*Why:* the owner closes an issue on purpose. A status can change by mistake, such as an issue
moved out of its status and back, and a branch deleted on that could still be needed.

**TR-18.** When a git command the workflow runs fails, the workflow shall end the run.

**TR-10.** The findings from earlier rounds that the quality reviewer gets shall mark each declined
finding as declined, with no reason.

*Why:* without the mark, the quality reviewer raises a declined finding again in every round.

**TR-20.** The findings from earlier rounds that the quality reviewer gets shall mark each finding
the implementer didn't get as not given to the implementer.

*Why:* without the mark, the quality reviewer takes a finding nobody was asked to fix, such as a
pre-existing finding, for one whose fix didn't work. It raises the finding again under a new ID,
so the PR's comment lists the same problem twice.

**TD-12.** The workflow gives each finding an ID made of its round and its place in the round's
list, such as `R2-F3` for the third finding of round 2. This meets FR-18.

*Why:* a reviewer that numbers its own findings starts from `F1` again each round, so the same ID
names different findings in the earlier findings the reviewer gets and in the PR's list of
declined findings. The workflow knows the round, so no agent has to keep count.

**TR-22.** The implementer shall have access only to the body of the run's issue, the working copy,
the factory's doc standards, the findings the workflow gives it, and the web through web search and
web fetch.

*Why:* an agent in the implementation loop is short-lived and may work on any machine, so anything
it needs has to be written where every agent can read it, not in Claude Code's memory.

**TR-12.** When the implementer finishes the work the issue asks for, or its changes in answer to a
round's findings, the implementer shall check its own change.

**TR-13.** When the implementer's own check finds a problem its change caused, the implementer shall
fix it before it hands back its result, unless the doc standards say the problem isn't the
implementer's to fix.

**TD-3.** The implementer keeps one session for the whole run, and resumes it in each round. This
meets FR-9.

*Why:* handling a finding needs the implementer's own reasons, such as why it made a choice the
finding questions. Without them, a fix can undo a decision.

## T-SEC-5. GitHub and the PR

**TD-4.** The implementer's last result holds the text that FR-17, FR-19, FR-21 and FR-20 call
for, which the workflow puts in the PR's description. So each of the implementer's results holds
that text for its whole change so far, not just for its latest round.

*Why:* only the implementer knows what it changed. A later round can undo an earlier decision or
settle a disagreement, and only the implementer knows when it has.

**TD-5.** The workflow keeps each declined finding and its reason from every one of the
implementer's results, and lists them in the PR's description. This meets FR-18.

*Why:* a finding declined in an early round isn't in the implementer's last result.

**TD-6.** The workflow writes the line of the PR's description that FR-16 calls for.

*Why:* the workflow already has the issue number.

**TD-7.** The workflow commits the implementer's changes to the run branch in the working copy.
This meets FR-15.

*Why:* a commit needs no judgment, so it's a step for the workflow's code (AD-2).

**TD-8.** The workflow makes the commits TD-7 calls for each time the implementer hands back its
result. This meets TR-3 and TR-4.

*Why:* each review diff is then the difference between two commits.

**TD-9.** The message of each commit TD-7 makes is the one the implementer's result holds. This
meets FR-15.

*Why:* the doc standards put a change's history in its commit message, and only the implementer
knows that history.

## T-SEC-6. Outside data

**TR-14.** When the workflow reads outside data other than a role's result, such as a reply from
GitHub or a project's settings, the workflow shall check it against a schema for that data before
acting on it.

**TR-15.** When a reply from GitHub doesn't fit its schema, the workflow shall end the run.

**TD-10.** The schemas that TR-1 and TR-14 call for are Pydantic models.

*Why:* one definition gives both the check and the type the code uses, so strict type checking
(AD-4) knows every field of the data.

**TD-11.** Each role's result schema, as the structured output in TD-1 takes it, is the JSON Schema
generated from the role's Pydantic model. This meets TR-1.

*Why:* the schema the Agent SDK gets and the check the workflow runs then can't drift apart.
