# Discussion notes

What Joe and Claude agreed or noted while going through the step 3 themes. These feed
`findings.md`.

## Context for theme 4: why the PR copies the issue

- The copy exists so the CI reviewer knows what was asked without seeing the reasons behind the
  work. The reviewer starts from the PR description, and is barred from PR and issue comments,
  where the implementer's reasons are (`review-pr` skill, line 43; code review design, line 29).
- The rule came first with the CI reviewer, on 2026-10-16 (commit bf206d0), before issues or the
  fix loop existed. Issues later made the copy their Do and Done when.
- The reviewer may read an issue's body, but not its comments (`review-pr` skill, line 43). So
  the line drawn is "task, not reasons", and the copy is how the task was handed over.
- The copy leaves out the issue's Why. A reviewer that reads only the description doesn't get the
  reason for the work, unless it opens the issue.
- Joe doesn't want to keep copying the issue into the PR, if another way can give the reviewer
  the task without the reasons.
- Where the reason is written down: road-trip-agent `research/code-review/code-review-evaluation.md`
  section 5 ("Giving the reviewer the task"), and open item 13 in `plan/open-items.md`, settled
  2026-10-16.
- Section 5.2 names the common pattern: the PR links to its ticket, and the reviewer reads the
  ticket (CodeRabbit, Qodo, GitHub's Copilot agent). It wasn't used only because the project had
  decided on 2026-10-15 to stay with the markdown plan, with no tracker. The doc says "tickets are
  left for a later project."
- Three days later, on 2026-10-19, work moved to GitHub issues. The copy rule carried over, and
  nobody went back to section 5.2. So the reason for copying was gone from 2026-10-19 on.
- **Agreed:** copying the issue into the PR served no real purpose once issues existed.
  - PRs with no issue don't count, since there was nothing to copy.
  - As a filter for reasons, it leaked, because the reviewer could read the issue body.
  - Keeping the task as it stood when the PR opened isn't worth a second copy that can drift.

## Theme 1: what an issue is for

- **Joe's framing: two kinds of work, split by who works them.**
  - **Factory work:** well defined going in, so the loop can build it and we can trust the
    result.
  - **Interactive work:** worked with the main session because it can't be defined well enough
    for the factory yet. It's exploratory, a spike in effect, even when not called one (#209,
    #282). These are the issues that got big.
- Interactive work may belong in a research doc, not an issue log. Sub-issues aren't needed: a
  plain factory issue can be opened when a piece of the work is ready to build.
- **#53, the idea notepad, is out of scope.** It worked as a place to park notes that Joe and
  agents could point to ("log this in #53"), and Joe would likely do it again. Not every issue in
  a project needs a rule from the factory. In hindsight, many of its ideas should have been their
  own issues.
- **Agreed: interactive work goes in a research doc, not an issue log.**
  - Factory work goes in an issue that is a fixed contract. It ends in one PR, and its body
    doesn't change once work starts.
  - Interactive work gets a small issue: the goal, a link to a research doc, and what it ends in.
    The work happens in the doc, on that work's own branch. The doc holds results, decisions and
    next steps.
  - When interactive work turns up something buildable, open a plain factory issue that links
    back. No sub-issues.
  - When the interactive work is done, freeze the doc like other research, and move its lasting
    decisions into the design docs.

## Theme 2: scope, and breaking work down

- **Agreed: scope is judged by the choices an issue leaves open, not by line count.**
  - A factory issue is ready when the implementer won't have to make a choice Joe would care
    about. That's judged outside the factory, by Joe or the interactive session, when an issue
    moves from Backlog to Ready.
  - Splitting and bundling are also done before the factory, at issue creation. Later, the
    factory might split an issue into sub-issues itself. Not for the first version.
  - Every follow-up found while working an issue becomes its own issue. It carries the
    `agent-created` label, and says which issue it came from.
  - A skill helps the interactive session create, split and bundle issues.
- Evidence: bigger PRs listed more decisions (a median of 4 under 200 lines changed, 8.5 for 200
  to 999, and 11 for 1,000 to 2,999). #156's PR listed 38. 28 PRs in the later eras had no issue,
  some of them follow-up bundles asked for in chat.
- **Agreed: bundling needs no rule of its own.** The readiness test covers it: a bundle is fine
  when every item's fix is written out, and an item that still needs a choice splits out.
  Bundling was rare (about 6 of 110 later PRs), and it came from one review pass that produced
  many small findings.
- Findings set aside from a review each become their own issue, under the follow-up rule. For
  now they're treated like any other issue. Whether the interactive session bundles them or the
  factory takes them one by one is a later concern.

## Detour from theme 3: the issue's sections

- **Agreed, for a factory issue:**
  - **Why:** keep. It was in 83 of 85 later issues and almost always needed.
  - **Design:** keep, as pointers only. These become requirement IDs once the docs have them.
  - **Do:** keep. What to change, specific to this issue.
  - **Acceptance criteria:** replaces Done when. It says what must be true when the work is done,
    specific to this issue, and checkable from the outside. It lists the conditions the hidden
    acceptance checks will test, in plain words. Example: "`look_up_stay_weather`'s reply no
    longer lists the activities."
  - **Dropped:** Open questions (an issue with one isn't Ready), Ends in, and Settled in.
  - **"Starts once #N is merged"** becomes GitHub's own blocked-by link, which code can read.
- **Not in the issue:**
  - Rules that apply to every PR, such as "`npm run check` passes" or "the view file is rebuilt".
    These go in a skill or doc that implementers and reviewers read, and CI enforces them.
  - Instructions about the implementer's own tests. The dev standards and the code reviewer cover
    those. A case that matters, such as a bug's failing case, is written as behavior in the
    acceptance criteria.
- **Agreed, for an interactive issue:** a Goal, and a link to its research doc. No Ends in. It
  ends when Joe says it's done, and that can mean closing it with no change.
- **Agreed: a bug gets its own shape and a `bug` label.** The sections are What happened (what
  was seen, with links to the session, trace or failed check), Expected, Design, Do, and
  Acceptance criteria. The acceptance criteria include the failing case, written as behavior.
  The gap between What happened and Expected is the Why. Agents and code will open many bugs, so
  a fixed shape prompts them for the evidence.

## Theme 3: one home for each kind of text

- **Agreed: open questions are issue comments, one question per comment.** When a question is
  settled, write the answer into the body (Do, Acceptance criteria, or the design doc), and hide
  the comment with "Resolved" as the reason. GitHub issue comments can't be threaded or resolved,
  but code can see a hidden comment and its reason through the API. Discussions were the other
  option, but they sit apart from the issue.
- **Agreed: one home for each kind of text.**
  - **Task:** the issue body (Why, Design, Do, Acceptance criteria). It stays fixed once the
    issue is Ready.
  - **Settled answers:** before Ready, written into Do, Acceptance criteria, or the design doc
    they belong in. The question comment is hidden as Resolved. GitHub keeps every earlier
    version of the body.
  - **Decisions made during work:** the PR, never the issue. The decision reviewer labels them
    and reports on the PR. An accepted decision's doc change goes in the same PR. The issue is a
    contract, so decisions made after Ready don't go back into it.
  - **Results:** for factory work, the PR. For interactive work, the research doc.
  - **Status:** the board only, never the body. The loop's attempt reasons go in issue comments.
  - **Set-asides:** a new issue, labeled `agent-created`, that names the issue it came from.
- Evidence: in the sample, settled questions were 28% of issue words (about half the task,
  about a third history). Decisions comments listed 163 decisions, and 42% named a doc. Results
  sat in the body, comments and PRs, while agents read comments in only 5% of issue reads.
  Status lines were 7% of #209's body.

## Theme 4: what a PR is for

- **Joe's working assumption, not settled: the workflow brokers all GitHub access.** The
  implementer and reviewers have no GitHub API. The workflow reads from GitHub and writes back,
  and decides what each agent gets. So the old problem, stopping the reviewer from seeing some of
  an issue, becomes choosing what the workflow passes in. Two things follow:
  - Issue and PR text must be easy for code to read: fixed section headings in the issue, and a
    marker on each comment the workflow writes.
  - The workflow passes on only text from Joe's account, which covers the loop doc's risk of a
    stranger's comment steering an agent.
- **Agreed: choose each piece of PR text by who reads it.**
  - **Description:** `Closes #N`, and a few plain sentences on what changed, for anyone skimming
    PRs and for the loop's regular summary of merged work. No copy of the task.
  - **Comments, one per report, each with a marker:** the merge decision (with each acceptance
    criterion's result), the decision reviewer's report, protected-file reasons, and what the
    worker learned. On a later attempt, the workflow updates its own comment, found by its
    marker, instead of adding another.
  - **No decisions comment, and no set-aside list.** Decisions go to the decision reviewer.
    Set-asides become issues, and the description links them.
- Evidence: in the sample, PR descriptions were 53% copy and 38% results. The decisions comments'
  163 decisions were read by the fixer and Joe, and by nothing after the merge. 42% reached a
  doc, and those show in the diff.
