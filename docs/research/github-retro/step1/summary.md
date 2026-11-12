# Step 1 summary

Facts from the full pull of 121 issues and 174 PRs. "Measures" means `step1/measures.md`.
"History" means `step1/history.md`.

## Facts

1. **Moving to issues ended the status-only PRs.** Before issues, about 16 of 46 PRs only updated
   the plan, such as "Mark phase 4 done". 41 of the first 49 PRs touched `plan/`. (History, era A)

2. **Issue size follows the kind of work.** Median words: fix 347, devloop 424, recording 438,
   spike 705, feature 808, eval 972. Eval issues also stay open longest (median 3 days, against
   0.1 to 1.1 for the rest), and 10 of 17 are still open. (Measures, issues by kind)

3. **Open questions are where issues grow before work starts.** Across the 85 issues written after
   the Why section, open questions hold 12,396 words, as much as Why and Done when together. 296
   questions were asked and 179 struck out, with the answer left under the struck question. In
   #53, #60 and #77, open questions are 2,000 to 2,400 words, against a Do list of 220 to 364.
   (Measures, section words; `measures.json`)

4. **Few issues changed after work started, but those that did turned into logs.** 10 issues had
   body edits after their first PR, 76 edits in all. #209 had 28 of them. Its Do section is 4,532
   words, mostly items like "Settled by Joe on 2026-11-10, in chat", and it has 9 PRs so far.
   (Measures, top issues; `measures.json` for #209)

5. **Most issues are one PR.** 68 of 121 had one PR. Only 4 had three or more: #63, #75, #209 and
   #266. 46 had none: 21 open, 14 not planned, and 13 closed with no PR (recordings, spikes and
   process work, which ended in a result or a decision). (Measures, PRs per issue)

6. **Comments were used for results, and that mostly worked.** Only 29 issues had comments (59
   comments, 13,042 words). They held run results (every recording issue), run logs (#87 has 15,
   #266 has 8), and close reasons (all 14 not-planned closures have one). #209 put its results and
   decisions in the body instead. (`step1/raw/issues.jsonl`)

7. **New issue sections appeared without a template.** "What happened" in 10 issues (bug reports),
   "Decided" in 9, "Items" in 2 (#156's 3,085-word list of wording fixes), "The cases" in 2.
   (Measures, section words)

8. **PR descriptions doubled once they copied the issue.** Median words: 210 before issues, 260,
   then 460 after the Why section, and 421 in the autonomous era. They copy the issue's Do and Done
   when word for word. All PR descriptions come to 83,755 words. (Measures, PRs by era)

9. **Decisions comments are large.** 133 of 174 PRs have one, with a median of 7 to 9 items. They
   total 50,877 words, about 60% of all PR description text. The largest list 38, 37 and 29
   decisions (PRs #158, #83, #205). (Measures, top PRs by decision items)

10. **PRs without an issue never went away.** 28 PRs in the last two eras had no issue. Most are
    small follow-ups or chat requests, such as "Lint listed paths, not the whole folder".
    (`measures.json`)

11. **The Triage pile is mostly evals.** 19 issues are open in Triage: 8 eval, 5 feature, 5 fix,
    1 recording. (Measures, open issues by status)

Two limits on these facts. Every issue and PR came from Joe's account, so the data can't separate
Joe's text from Claude's. The kind of work was set by hand from titles.

## Questions for step 2

- Who read the struck-out questions and their answers once work started? Were they the task, or
  history?
- Does open-ended work, like an eval, need a different container than one issue with a Do list?
  #209, #266 and #282 handled it three ways.
- The PR description copies the issue. Who read the copy, and what for?
- What happened to the decisions in the comments? How many went into docs, and how many did Joe
  act on?
- Bugs grew a "What happened" section on their own. Do kinds of issue need their own shape?
- Where did the result of each issue that closed with no PR end up?

## Proposed sample for step 2

About 15 issues across eras, kinds and sizes, with their PRs:

| Era | Issues |
|---|---|
| A, plan moved to issues | #60 stay researcher (2,794 words, 31 edits), #57 itinerary view (168 words), #53 agent evaluations (still in Triage) |
| B, issues | #77 fix loop in CI (2,568 words, 32 edits), #87 what the reviewer reads (15 comments) |
| C, Why section | #129 itinerary read spike (edited after its PR), #156 prompt fixes (3,085-word item list), #151 smaller itinerary read (typical feature), #169 check in at the stay ("What happened" and "Decided") |
| D, autonomous | #199 workers' trip tools, #209 saving evaluation, #266 workers' refused keys (eval, results in comments), #282 general evaluator, #273 Montana recording, #233 search_near bug, #236 option set look-back (not planned) |
