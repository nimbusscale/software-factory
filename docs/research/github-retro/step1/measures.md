# Measures

Sources: `step1/raw/issues.jsonl` and `step1/raw/prs.jsonl` (pulled 2026-11-11), computed by
`scripts/measures.py` into `step1/measures.json`, and printed by `scripts/report.py`.

How to read it:

- **Kind of work** was set by hand from each issue's title, in `scripts/measures.py`. The kinds are
  feature (builds part of the app), fix (a bug or a wording fix), eval (an agent evaluation or its
  tooling), spike (research or an investigation), devloop (the review loop, CI and process), and
  recording (a simulated-user run).
- **Era** is when the issue or PR was opened (see `history.md`).
- **Edits** are body edits GitHub recorded. One edit can change many lines.
- **A PR counts for an issue** when it says `Closes #N` or `Part of #N`, ends its title with
  `(#N)`, or GitHub links it as closing the issue.
- **Decision items** are the list items in the PR's decisions comment.
- Everything is opened from Joe's account, by Joe or by Claude, so the author can't show who wrote
  what.


### Issues by kind of work

| group | n | median words | max words | median edits | edits total | median PRs | median days open | closed done | closed not planned | open |
|---|---|---|---|---|---|---|---|---|---|---|
| devloop | 17 | 424 | 2568 | 2 | 81 | 1 | 1.1 | 14 | 3 | 0 |
| eval | 17 | 972 | 7042 | 3 | 134 | 0 | 3.0 | 5 | 2 | 10 |
| feature | 46 | 808.0 | 2794 | 3.0 | 211 | 1.0 | 0.2 | 39 | 2 | 5 |
| fix | 19 | 347 | 3378 | 0 | 28 | 0 | 0.1 | 9 | 5 | 5 |
| recording | 9 | 438 | 539 | 3 | 34 | 0 | 0.2 | 8 | 0 | 1 |
| spike | 13 | 705 | 1763 | 2 | 39 | 1 | 0.6 | 11 | 2 | 0 |

### Issues by era created

| group | n | median words | max words | median edits | edits total | median PRs | median days open | closed done | closed not planned | open |
|---|---|---|---|---|---|---|---|---|---|---|
| A plan/ | 24 | 536.0 | 2794 | 6.5 | 196 | 1.0 | 7.3 | 22 | 0 | 2 |
| B issues | 12 | 491.5 | 2568 | 2.5 | 80 | 0.5 | 1.1 | 11 | 1 | 0 |
| C why | 42 | 717.0 | 3378 | 2.0 | 112 | 1.0 | 0.1 | 32 | 4 | 6 |
| D auto | 43 | 519 | 7042 | 2 | 139 | 0 | 0.1 | 21 | 9 | 13 |

### Top issues by words

- #209 eval, 7042 words, 41 edits (28 after its first PR), 9 PRs, 1 comments, In review: Saving to the right place: trip brief, itinerary, or trip memory, chec
- #156 fix, 3378 words, 9 edits (0 after its first PR), 1 PRs, 0 comments, Done: Coordinator prompt and tool description fixes
- #60 feature, 2794 words, 31 edits (0 after its first PR), 1 PRs, 0 comments, Done: The stay researcher
- #282 eval, 2774 words, 16 edits (0 after its first PR), 1 PRs, 2 comments, Done: General evaluator: grounded in the record
- #53 eval, 2769 words, 31 edits (0 after its first PR), 0 PRs, 0 comments, Triage: Agent evaluations
- #266 eval, 2740 words, 18 edits (13 after its first PR), 3 PRs, 8 comments, Done: The workers send keys their candidate tools refuse, checked with an ev
- #77 devloop, 2568 words, 32 edits (0 after its first PR), 1 PRs, 0 comments, Done: The fix loop in CI
- #76 devloop, 2452 words, 13 edits (10 after its first PR), 2 PRs, 0 comments, Done: A fix agent for review findings
- #142 feature, 1941 words, 4 edits (1 after its first PR), 1 PRs, 0 comments, Done: Rate and annotate chat turns and sessions, with links to their traces
- #66 feature, 1924 words, 8 edits (0 after its first PR), 1 PRs, 0 comments, Done: The simulated user
- #129 spike, 1763 words, 10 edits (7 after its first PR), 1 PRs, 0 comments, Done: Spike: whole itinerary reads of long trips
- #245 eval, 1628 words, 7 edits (0 after its first PR), 1 PRs, 0 comments, Done: Start a run from any turn of a recorded session

### PRs per issue

{0: 46, 1: 68, 2: 3, 3: 2, 5: 2}
issues with 3+ PRs: [(63, 6), (75, 3), (209, 9), (266, 3)]

### Edits after the first PR opened

issues with any: 10 total such edits: 76

### Section words, issues created after the Why section (era C and D)

- Why: in 83 of 85, median 136, max 578, total 14141
- Do: in 83 of 85, median 105, max 4532, total 21362
- Done when: in 82 of 85, median 34.0, max 165, total 3640
- Ends in: in 81 of 85, median 8, max 47, total 1224
- Open questions: in 79 of 85, median 65, max 888, total 12396
- Design: in 77 of 85, median 35, max 413, total 4278
- : in 31 of 85, median 7, max 148, total 508
- What happened: in 10 of 85, median 207.5, max 451, total 2293
- Settled in: in 9 of 85, median 17, max 24, total 112
- Decided: in 9 of 85, median 274, max 813, total 3432
- The fix to test: in 3 of 85, median 85, max 88, total 248
- Items: in 2 of 85, median 1632.5, max 3085, total 3265
- Where to look: in 2 of 85, median 69.0, max 88, total 138
- The cases: in 2 of 85, median 689.0, max 1276, total 1378

### Open questions

issues with open-question items: 96 items: 296 struck: 179

### Comments on issues

issues with comments: 29 comments total: 59 comment words: 13042
not planned closures with a comment: 14

### Open issues by status

Counter({('Triage', 'eval'): 8, ('Triage', 'feature'): 5, ('Triage', 'fix'): 5, ('In review', 'eval'): 1, ('Backlog', 'eval'): 1, ('Triage', 'recording'): 1})

### PRs by era opened

| group | n | merged | median desc words | max | no issue | closes # | decisions comment | median decision items | median review threads | median commits | median hours to merge |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A plan/ | 46 | 46 | 210.0 | 1512 | 46 | 0 | 6 | 7.5 | 0.0 | 1.0 | 0.1 |
| B issues | 20 | 12 | 260.0 | 1177 | 5 | 11 | 19 | 9 | 1.0 | 3.0 | 0.2 |
| C why | 56 | 54 | 459.5 | 1269 | 14 | 40 | 56 | 8.5 | 0.0 | 2.0 | 0.2 |
| D auto | 52 | 49 | 421.0 | 2179 | 14 | 27 | 47 | 7 | 0.0 | 1.0 | 0.1 |

### PRs with an issue, by kind of work

| group | n | merged | median desc words | max | no issue | closes # | decisions comment | median decision items | median review threads | median commits | median hours to merge |
|---|---|---|---|---|---|---|---|---|---|---|---|
| devloop | 14 | 13 | 390.0 | 1198 | 0 | 10 | 13 | 12 | 0.0 | 3.0 | 0.1 |
| eval | 17 | 16 | 483 | 2179 | 0 | 5 | 17 | 8 | 2 | 2 | 0.1 |
| feature | 44 | 39 | 619.0 | 1483 | 0 | 44 | 44 | 9.0 | 1.0 | 2.0 | 0.2 |
| fix | 9 | 9 | 363 | 1093 | 0 | 9 | 9 | 6 | 0 | 1 | 0.1 |
| recording | 4 | 2 | 325.5 | 762 | 0 | 4 | 4 | 3.5 | 0.0 | 1.0 | 0.3 |
| spike | 7 | 7 | 455 | 858 | 0 | 6 | 7 | 9 | 0 | 2 | 0.3 |

### Top PRs by description words

- PR #283 D auto, 2179 words, issues [282]: General evaluator: grounded in the record
- PR #6 A plan/, 1512 words, issues []: Phase 4: choose the libraries, and run the app locally
- PR #263 D auto, 1483 words, issues [66]: The simulated user
- PR #216 D auto, 1376 words, issues [64]: The weather worker
- PR #162 C why, 1269 words, issues [56]: Lay out days
- PR #116 C why, 1268 words, issues [47]: The memory server
- PR #217 D auto, 1243 words, issues [62]: Option cards
- PR #120 C why, 1207 words, issues [48]: The coordinator in the terminal

### Top PRs by decision items

- PR #158 C why, 38 items, 1195 words, issues [156]: Coordinator prompt and tool description fixes
- PR #83 B issues, 37 items, 1572 words, issues [75]: Our own review agent in the Code review workflow
- PR #205 D auto, 29 items, 1105 words, issues [198]: Worker setup: report_result, the hooks, and the result
- PR #91 B issues, 27 items, 916 words, issues [76]: A fix agent for review findings
- PR #162 C why, 22 items, 785 words, issues [56]: Lay out days
- PR #207 D auto, 22 items, 1571 words, issues [60]: The stay researcher
- PR #120 C why, 19 items, 820 words, issues [48]: The coordinator in the terminal
- PR #128 C why, 19 items, 726 words, issues [54]: Read the itinerary

decision comment words total: 50877 desc words total: 83755
PR desc edits: PRs with edits 44 total 110
