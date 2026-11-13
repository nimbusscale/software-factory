# Step 2 summary

What the sample shows across more than one case. Sources:

- `labels-report.md`: the labels, totaled by kind of text
- `cases.md`: one section per issue
- `reads-report.md`: how often agents read each issue, from the local transcripts
- `growth.md`: how every issue's body grew, for all 121 issues

The sample is 16 issues, about 31,000 words of issue body, 12,000 of PR descriptions, 10,000 of
decisions comments, and 5,800 of issue comments.

## Patterns

1. **Settling questions in chat made issues grow before work started.** 27 of 121 issues at
   least doubled before their first PR. #60, the stay researcher, went from 254 to 2,794 words.
   #77, the fix loop in CI, went from 156 to 2,568. Each time, the growth was answers written
   under struck-out questions. In the sample, settled questions are 28% of all issue words.
   (`growth.md`, `labels-report.md`)

2. **Those answers were often the task, sitting outside the Do list.** Of 8,600 words of settled
   questions, the labelers marked 56% as needed to do the work and 35% as not needed. Two
   examples:
   - In #169, the check-in stop, the struck answers hold the design itself.
   - In #77, most answers had already been written into the code review design, so they were
     history.

   A fresh agent can't tell the two apart without reading all of it. (`labels-report.md`,
   `cases.md`)

3. **Open-ended work turned the body into a log.** Only 7 of 121 issues grew after their first
   PR: #209, #266, #76, #177, #75, #63 and #129. All are evals, spikes or multi-step loop work.
   In #209, the saving evaluation, results are 30% of the body, as run tables inside the Do
   list. Its Do list now says two things that contradict each other (I209-57 and I209-59). Build
   tasks never grew after the PR opened. (`growth.md`, `cases.md`)

4. **Results had three homes, and no rule picked one.**
   - **The body:** #209, #129 and #53. The labelers marked 69% of the result words there as not
     needed for the work.
   - **Issue comments:** #87, #273, #282 and #266. 93% of comment words in the sample are
     results.
   - **The PR description:** most build issues. Results are 38% of PR description words.

   (`labels-report.md`)

5. **Agents almost never read comments.** Of 2,000 times an agent read an issue, 105 included
   its comments (5%). Results in comments reached Joe, but not later agents.
   (`reads-report.md`)

6. **PR descriptions are mostly a copy of the issue.** 53% of PR description words copy the
   issue, and 38% are results. The copies sometimes drifted:
   - #77's PR shortened three Do items and dropped their reasons.
   - One #209 PR quotes an older wording of a Do item.

   (`labels-report.md`, `cases.md`)

7. **Decisions comments held many choices, and most didn't reach a doc.** The sample's 12 PRs
   list 163 decisions, and 69 of them (42%) say which doc they went into. Some comments are
   longer than the issue: #199's is 996 words against a 296-word issue. In #60 and #199, the
   comment says the decisions were made without Joe, though the issue said "Settled in: chat".
   (`labels-report.md`, `cases.md`)

8. **An umbrella issue became a parking lot.**
   - #53, agent evaluations, was read 81 times in 34 sessions and edited 49 times by command. It
     never had a PR.
   - Its first open question still names promptfoo, and its Do list still says "set up the
     framework", though Phoenix was chosen weeks earlier.

   (`reads-report.md`, `cases.md`)

9. **Small issues with no open questions worked.** #199, #57 and #151 were 168 to 1,027 words
   and mostly task. None had a body change after the PR opened. Their PRs merged with only
   results added. (`labels-report.md`, `cases.md`)

10. **Corrections landed only where the work happened.**
    - In #87, a hold decision was reversed, and the only record is one sentence in a later result
      comment.
    - In #236, the closing comment says a claim in the body was wrong, and the body was left as
      it was.
    - In #266, two open questions were answered by the work but never struck out.

    (`cases.md`)

## Questions for step 3

These follow from the patterns, and map to the four themes in the plan.

- **What an issue is for.** Build tasks stayed small and stable. Evals and spikes grew into logs.
  Does open-ended work need a different container, such as a parent issue with one child issue
  per step, or a results file in the repo?
- **Scope and breaking work down.** #53 and #209 each held many steps. Where should the line be
  between one issue and several?
- **Where each kind of text belongs.** Settled answers, results, status and decisions each
  landed in two or three places. Should each have one home, and what is it?
- **What PRs are for.** The description copies the issue, and the decisions comment mostly
  doesn't reach a doc. What should a PR hold, and who reads it?
