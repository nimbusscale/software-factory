# Issues and PRs for agent-built projects: findings from road-trip-agent

2026-11-12. A record of the GitHub retrospective on road-trip-agent, as of this date. It isn't
kept up to date.

This file says how road-trip-agent wrote, used and updated its GitHub issues and pull requests,
what worked and what didn't, and what any agent-built project should do instead. The last
sections say what this means for the Agentic Development Loop, and give draft shapes for issues
and PRs. The evidence is in `step1/` and `step2/`, and the agreed points are in `discussion.md`.

## Takeaways

1. **There are two kinds of issue work, and one issue shape fit only one of them.** Factory work
   is defined well enough to hand to agents. Interactive work is explored with the main session
   until it's understood. The interactive issues are the ones that grew into logs.
2. **A factory issue is a contract.** Once it's Ready, its body doesn't change. Questions are
   settled before that, and their answers go into the task, not under a struck-out question.
3. **Interactive work belongs in a research doc, not an issue.** The issue stays small: a goal,
   and a link to the doc. Results and decisions go in the doc.
4. **Judge an issue's scope by the choices it leaves open, not by its size.** An issue is ready
   when the implementer won't have to make a choice a person would care about.
5. **Give each kind of text one home.** Task, settled answers, decisions, results, status and
   set-asides each landed in two or three places. Each needs exactly one.
6. **Agents don't read comments.** They read an issue's comments in 5% of reads. A result left in
   a comment reaches people, but not later agents.
7. **Choose each piece of PR text by who reads it.** Half the PR text was a copy of the issue,
   and most of the rest had no reader once the PR merged.
8. **A rule can outlive its reason.** The PR copied the issue because there was no tracker. Three
   days later there was, and the copy went on for weeks. When a rule rests on a condition, write
   the condition down, so someone notices when it stops being true.

## 1. What happened

The practice grew on its own, in four steps. Details are in `step1/history.md`.

- **The plan in the repo (2026-10-15 to 10-19).** Work was tracked in two markdown files. `plan/`
  got 76 commits in five days. About a third of the PRs did nothing but update the plan, such as
  "Mark phase 4 done". Parallel branches all needed to change the same files.
- **Issues (from 2026-10-19).** Work moved to GitHub issues with a task template: Design, Open
  questions, Do, Done when, Ends in, Settled in. The status-only PRs stopped.
- **The Why section (from 2026-10-22).** An issue had said "Joe doesn't want to raise the limit",
  with no reason, so the agent worked on the wrong problem. The template gained a Why section and
  a test: could a new session, with only the repo and this issue, build it the way it's meant?
- **Autonomous work (from 2026-10-28).** Agents worked issues alone in worktrees, and merged
  under a rule. In about a week, 41 PRs merged and 26 issues closed, many from "please do this
  issue" alone.

By the end there were 121 issues and 174 PRs.

## 2. Two kinds of issue work

**Factory work** is defined well going in, so a loop of agents can build it and the result can be
trusted. **Interactive work** can't be defined that well yet, so a person works it with the main
session. It's a spike in effect, even when it isn't called one.

The data shows the split. Only 7 of 121 issues grew after their first PR, and all were
interactive: evals, spikes, or multi-step work on the review loop (`step2/growth.md`). #209, the
saving evaluation, went from 840 to 7,042 words over 41 versions and nine PRs. Each step's
status and results went into its Do list. By the end, results were 30% of the body, and two Do
items contradicted each other.

Small build issues held steady. #199, the workers' trip tools, was 296 words, never edited, and
had one PR. #151, the slimmer itinerary read, was 83% task, and nothing changed after its PR
opened.

**What to do instead:**

- A factory issue is a fixed contract. It ends in one PR.
- An interactive issue holds a goal and a link to a research doc. The work happens in the doc,
  on that work's own branch. Since one line of work owns the doc, it avoids the conflicts the
  shared plan files had.
- When interactive work turns up something buildable, open a plain factory issue that links
  back. No sub-issues are needed.
- An interactive issue ends when the person says it's done. That can mean closing it with no
  change.
- When the interactive work ends, the doc is frozen like other research, and its lasting
  decisions move into the design docs.

## 3. A factory issue is a contract

Before work started, issues grew because questions were settled in chat, and each answer was
written under its struck-out question. 27 of 121 issues at least doubled before their first PR.
#60, the stay researcher, went from 254 to 2,794 words. Its settled questions were 81% of the
body, and its Do list was 257 words.

In the sample, settled questions were 28% of issue words. The labelers marked 56% of those words
as needed to do the work, and 35% as history. So the task was split between Do and the question
section, and a fresh agent had to read all of it to tell which was which. In #169, the check-in
stop, the struck answers were the design itself. In #77, the fix loop in CI, most had already
been written into a design doc.

Corrections also landed wherever the work happened, and the body went stale. #266 had two open
questions answered by the work but never struck. #236's closing comment says a claim in its body
was wrong, and the body was left as it was.

**What to do instead:**

- Settle every question before Ready. Each answer goes into Do, Acceptance criteria, or the
  design doc it belongs in, and the question is deleted.
- Open questions live in issue comments, one question per comment. Once settled, the comment is
  hidden with "Resolved" as the reason. GitHub issue comments can't be threaded or resolved, but
  code can see a hidden comment and its reason.
- GitHub keeps every version of an issue body, so deleting a settled question loses nothing.
  That history is how this retro measured growth.

## 4. Scope by the choices left open

The only scope rule was "one piece of work that ends in a PR or a decision". 68 of 121 issues
had exactly one PR, and that mostly worked. But bigger PRs left more choices to the implementer.
The median decisions listed in a PR's decisions comment were 4 under 200 lines changed, 8.5 for
200 to 999, and 11 for 1,000 to 2,999. #156 bundled 18 prompt fixes, and its PR listed 38
decisions.

Work also spilled out of issues. 28 PRs in the later eras had no issue. Some were bundles of
follow-ups asked for in chat after a merge, such as five unrelated changes in one PR.

**What to do instead:**

- An issue is ready when the implementer won't have to make a choice a person would care about.
  A person or the interactive session judges that, when an issue moves from Backlog to Ready.
- Split, bundle and set readiness before the factory. A skill can help the interactive session
  do it. Later, the factory might split issues itself.
- Bundling needs no rule of its own. A bundle is fine when every item's fix is written out. An
  item that still needs a choice splits out. Bundling was rare, about 6 of 110 later PRs, and it
  always came from one review that produced many small findings.
- Every follow-up becomes its own issue, labeled as agent-created, naming the issue it came from.
  Nothing reaches the factory from chat.

## 5. One home for each kind of text

| Kind of text | Where it went | Its one home |
|---|---|---|
| Task | Issue body, and copied into the PR | Issue body, fixed once Ready |
| Settled answers | Under struck-out questions | Do, Acceptance criteria, or a design doc, before Ready |
| Decisions made during work | The PR's decisions comment | The PR. An accepted decision's doc change goes in the same PR. |
| Results | Issue body, issue comments, or the PR | Factory work: the PR. Interactive work: the research doc. |
| Status | The board, plus lines in the body | The board only |
| Set-asides | Decisions comment, then an issue | A new issue |

Two facts drove this:

- **Agents read issue comments in 5% of reads** (105 of 2,000, from the local transcripts). The
  comments in the sample were 93% results, so those results reached people but rarely agents.
- **Decisions mostly didn't reach a doc.** The sample's decisions comments listed 163
  decisions, and 42% named the doc they went into. The rest stayed in a comment that nothing read
  after the merge.

## 6. PR text, chosen by reader

**The copy outlived its reason.** The PR description copied the issue's Do and Done when word for
word, and the reviewer started from it. The reason is in road-trip-agent's code review research,
section 5. The usual pattern, where the PR links to its ticket and the reviewer reads the ticket,
was set aside only because the project had no tracker. Three days later, work moved to GitHub
issues, and nobody went back to it. By the end, 53% of sampled PR description words were copy.
The copies drifted too: one PR shortened three Do items and dropped their reasons.

**The decisions comment had no reader after the merge.** The fixer and Joe read it while the PR
was open. The decisions that mattered reached a doc, and those show in the diff anyway.

**What to do instead:**

- **Before adding a section to a PR, name who reads it and when.** If nobody does, leave it out.
- **The description** says `Closes #N`, and a few plain sentences on what changed. Those
  sentences are for anyone skimming PRs, and for a regular summary of merged work.
- **Each report is its own comment, with a marker code can find.** The reports are the merge
  decision (with each acceptance criterion's result), the decision reviewer's report,
  protected-file reasons, and what the worker learned. On a later attempt, the writer updates its
  own comment instead of adding another.
- **No copy of the task, no decisions comment, and no set-aside list.**

## 7. The issue's sections

Today's template, section by section:

| Section | Keep? | Why |
|---|---|---|
| Why | Keep | In 83 of 85 later issues, and marked needed almost every time |
| Design | Keep, as pointers | Median 35 words of links to doc sections. These become requirement IDs. |
| Do | Keep | What to change |
| Done when | Becomes Acceptance criteria | It mixed three things. See below. |
| Open questions | Drop | An issue with one isn't Ready |
| Ends in, Settled in | Drop | The kind of issue says it. "Settled in" also went stale: twice a decisions comment said the decisions were made without Joe, while the issue still said "chat". |
| "Starts once #N is merged" | Replace | In 50 of 121 issues. Use GitHub's own blocked-by link, which code can read. |

Done when mixed three kinds of item:

- **Behavior checkable from the outside**, such as "`look_up_stay_weather`'s reply no longer
  lists the activities." This is specific to the issue, so it stays. It becomes Acceptance
  criteria: what must be true when the work is done, in plain words. These are the conditions
  that the hidden acceptance checks test.
- **Rules for every PR**, such as "`npm run check` passes." These go in a skill or doc that
  implementers and reviewers read, and CI enforces them.
- **Instructions about the implementer's own tests**, such as "the new lines are pinned by a
  test." The dev standards and the code reviewer cover these. A case that matters, such as a
  bug's failing case, is written as behavior in the acceptance criteria.

A "What happened" section also appeared on its own, in 10 issues, to hold a bug's evidence. So
bugs get their own shape and a `bug` label. Agents and code will open many bugs, and a fixed
shape prompts them for the evidence.

## 8. Notes for the Agentic Development Loop

These come from the findings above. The loop design isn't changed here.

- **The workflow brokers all GitHub access** (Joe's working assumption, not settled). Agents
  have no GitHub API. The workflow reads issues and PRs, decides what each agent gets, and writes
  back. So:
  - Issue text needs fixed section headings, and workflow comments need markers, so code can
    read them.
  - The workflow passes on only text from Joe's account. That covers the loop design's risk of a
    stranger's comment steering an agent.
  - Hiding text from a reviewer becomes a choice about what the workflow passes in, not a rule
    the reviewer has to follow.
- **The issue checker posts each question as its own comment.** The answer goes into the body,
  and the comment is hidden as Resolved.
- **Attempt reasons go in issue comments,** not the body, so the body stays a contract.
- **Acceptance criteria are their own section**, so the main session can turn each one into a
  hidden check.
- **Blocked-by is GitHub's own link**, which the workflow reads to skip blocked issues.
- **Report comments are updated in place on a later attempt**, found by their marker.
- **The implementer doesn't write a PR description beyond a short summary.** The workflow writes
  `Closes #N` and the reports.
- **A skill for the interactive session** creates, splits and bundles issues, and checks
  readiness before an issue moves to Ready.

## 9. Out of scope

- **#53, the idea notepad.** One issue collected ideas not ready for work. It was read 81 times
  in 34 sessions and never had a PR, and parts went stale. It still worked as a place to park
  notes that people and agents could point to. Not every issue in a project needs a rule from the
  factory. In hindsight, many of its ideas should have been their own issues.
- **What belongs in a doc versus an issue**, and how issues point to docs. The docs retro covers
  those.

## Appendix A: draft shapes

These are starting drafts, not reviewed templates.

### Factory task

```markdown
## Why
<!-- A few sentences: what the work is for. -->

## Design
<!-- Pointers only: the doc sections or requirement IDs this follows. -->

## Do
<!-- What to change, specific to this issue. No open questions. -->

## Acceptance criteria
<!-- What must be true when it's done, checkable from the outside, in plain words. -->
```

Blocked-by goes in GitHub's own link. Labels say whether the loop may take it.

### Factory bug

```markdown
## What happened
<!-- What was seen, with links to the session, trace or failed check. -->

## Expected
<!-- What should have happened instead. -->

## Design

## Do

## Acceptance criteria
<!-- Include the failing case, written as behavior. -->
```

Labeled `bug`. An agent-opened one is also labeled `agent-created`, and names the issue it came
from.

### Interactive issue

```markdown
## Goal
<!-- What we're trying to learn or decide. -->

## Research doc
<!-- A link to the doc where the work happens. -->
```

### PR

- **Description:** `Closes #N`, a few sentences on what changed, and links to any follow-up issues.
- **Comments, one per report, each with a marker:** merge decision with acceptance results,
  decision reviewer report, protected-file reasons, what the worker learned.

## Appendix B: method and sources

- **Step 1** pulled all 121 issues and 174 PRs, with every saved version of each issue body. It
  measured them by era and by kind of work. The kind was set by hand from titles.
  (`step1/summary.md`, `step1/measures.md`, `step1/history.md`)
- **Step 2** sampled 16 issues across eras, kinds and sizes, with their PRs. Three agents labeled
  each paragraph by kind (task, reason, settled question, decision, status, result, and so on)
  from one brief. A spot check of random labels found no wrong ones. Agent reads came from the
  local Claude Code transcripts. These don't include the CI agents. (`step2/summary.md`,
  `step2/cases.md`, `step2/labels-report.md`, `step2/reads-report.md`, `step2/growth.md`)
- **Step 3** went through four themes with Joe, one at a time. (`discussion.md`)
- **Limits:** every issue and PR came from Joe's account, so the data can't separate Joe's text
  from Claude's. It's one project, with small samples.
