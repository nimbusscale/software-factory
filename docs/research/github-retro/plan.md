# GitHub retrospective: plan

The goal is one Markdown file, `scratch/github-retro/findings.md`. It holds what road-trip-agent
teaches about running agentic development through issues and pull requests: what each was used
for, how big an issue should be, where each kind of text belongs, and what kept the text useful or
let it turn into a dumping ground. The learnings should hold for any agentic project, the way the
docs retro's do. A last section says what they mean for the Agentic Development Loop.

This project's issues and PRs grew organically: work moved from a markdown file to issues, and
then to autonomous work driven by the issue and PR text. The point is to learn from that corpus,
not to grade it against the next project's standards.

This work stays in `scratch/`, which git ignores. Nothing here changes the repo, GitHub, or the
loop artifact. Notes from each step go in `scratch/github-retro/stepN/`. Agreed conclusions go in
`scratch/github-retro/discussion.md`.

## An example of the range

Two issues show how far apart issues got. They are examples, not the focus. The retro covers all
the issues and PRs.

- #199, "The workers' trip tools": 276 words, never edited, no comments, one PR. It worked from
  "please do this issue" alone.
- #209, "Saving to the right place": 7,155 words, 41 body edits, nine PRs so far, still open. It
  holds plans, status, results and decisions together.

## Step 1: Collect the facts

Pull every issue and PR from GitHub once, with `gh api graphql`, into `step1/raw/`, including body
edit history. Then write:

- **History** (`step1/history.md`). How the practice changed, and why: the markdown file, the move
  to issues on 2026-10-19, the Why section on 2026-10-22, autonomous work. Use git history of the
  template, DEVELOPMENT.md and CLAUDE.md, plus the plan files.
- **Measures** (`step1/measures.md`). Per issue: words, body edits, comments, PRs, days open, and
  the kind of work (build, wording fix, eval, research, infra). Per PR: words in the description,
  comments, and review rounds. Find which issues sit at each end, and whether the kind of work
  explains it.

Done when both files exist, and `step1/summary.md` lists the main facts with where each came from.

## Step 2: Look inside a sample

Pick the sample from step 1's measures: issues and PRs from each era and each kind of work, at
both ends of the range and in the middle. About 15 issues, plus a sample of their PRs. Sort the
text in each into kinds, the way the docs retro sorted doc commits: task, reason, decision,
status, result, run log, history, copy of a doc. For each kind, note who wrote it, when, and
whether anyone read it later. Write `step2/cases.md`, then a short summary of the patterns across
the whole sample.

Done when each picked issue and PR has its text sorted, with links, and the summary names the
patterns that show up in more than one case.

## Step 3: Talk through the themes

Go through these with Joe one at a time, using steps 1 and 2. Agreed points go in `discussion.md`.

- **What an issue is for.** Does one format fit both a build task and open-ended work like an
  eval? If not, what does open-ended work need instead?
- **Scope and breaking work down.** How big should an issue be? When should one split, and who
  decides?
- **Where each kind of text belongs.** Body, comment, PR, doc, or somewhere else, such as a
  results file. What should never be written down at all?
- **What PRs are for.** Who read the descriptions and decisions comments, and what they used them
  for.

Done when Joe and Claude have talked through every theme.

## Step 4: Write the findings file

Write `findings.md`: each learning in plain words with its evidence, then a short section on what
it means for the loop.

Done when `findings.md` covers steps 1 to 3, and Joe has read it.

## Progress

- Plan rewritten (2026-11-11) after Joe's feedback: universal learnings from the corpus, not a
  check of today's text against the loop's roles.
- Step 1: done (2026-11-11). `step1/summary.md` has the facts, the questions for step 2, and a
  proposed sample.
- Step 2: done (2026-11-12). 16 issues and their PRs, labeled by three agents from one brief
  (`step2/labeling-brief.md`). `step2/summary.md` has the patterns and the questions for step 3.
  Also added: body growth for all 121 issues (`step2/growth.md`) and agent reads from the local
  transcripts (`step2/reads-report.md`).
- Step 3: done (2026-11-12). Four themes talked through with Joe. Agreed points are in
  `discussion.md`, including a detour on the issue's sections.
- Step 4: done (2026-11-12). `findings.md` written, and Joe agreed with it as it stands, including takeaway 8 and the loop note on who writes the PR description.
