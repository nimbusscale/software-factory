# Step 2 cases

One section per sampled issue. Each has the numbers from `issue-blocks.json` and `reads.json`, then the labeling agent's notes. Block ids such as `I209-36` point into `issue-blocks.json` and `pr-blocks.json`. The labels themselves are in `labels/`, and the totals are in `labels-report.md`.

Three labeling agents worked from one brief (`labeling-brief.md`), each on five or six issues. A spot check of eight random blocks found no wrong labels.

## #53: Agent evaluations

- Kind: eval. Era: A plan/. PRs: none.
- Words: 383 at first, 2769 when the first PR opened, 2769 at the end. Saved versions: 30.

Issue #53 was the umbrella for agent evaluations. It never got a PR or a comment. The body grew from 383 words on 2026-10-19 to 2,769 words over 31 versions, through 2026-11-06, as each new evaluation idea was parked in it. Open questions take the most words (about 1,160). Next is one 785-word block (I53-22) that holds a provisional plan for how the evaluations are built up, then struck-out questions (about 460). The Do and Done when items are about 275 words and barely changed. Surprising: the first open question still names promptfoo as the likely framework (I53-5), and the Do still says 'set up the framework' (I53-24), though the later blocks show Phoenix was chosen (I53-17, I53-22). Several open questions read as stale or half answered (I53-8, I53-11). The struck-out answers are history for this issue: four were moved to other issues (I53-12, I53-15, I53-16), and I53-9's answer is about other issues' scope. With no PR or comments, results and status went into the body: the #132 spike results (I53-13), the corpus counts and the Bar Harbor judge numbers inside I53-22, and the move of the first evaluator to #282 (I53-22).

## #57: The itinerary view

- Kind: feature. Era: A plan/. PRs: #164.
- Words: 122 at first, 168 when the first PR opened, 168 at the end. Saved versions: 2.

The issue asked for the itinerary view: an endpoint plus a panel beside the chat. Its body barely grew, from 122 to 168 words, and nothing was added after the PR opened. Task items are over half its words, and there were no open questions (I57-3). The PR description copied the Do and Done when word for word (P164-d0 to d2), then added a long results section from the deployed site, the tests, and a local hand check (P164-d4 to d14), so results went in the PR, not the issue. The decisions comment holds ten implementation choices, such as the endpoint path and times sent as text (P164-c1 to c10), and says none was written into a design doc (P164-c0). It set aside weather, the map, and option cards to their own issues (P164-c11). Nothing surprising, except that the PR merged seven minutes after it opened.

## #60: The stay researcher

- Kind: feature. Era: A plan/. PRs: #207.
- Words: 254 at first, 2794 when the first PR opened, 2794 at the end. Saved versions: 30.

Issue #60 built the stay researcher, the first worker agent. Its body grew from 254 words at creation on 2026-10-19 to 2,794 words, over 31 versions, all before the PR opened on 2026-10-28; nothing was added after. Settled questions take most of the words (about 2,250), led by the 884-word budget tier answer (I60-10); the Do and Done when items are about 350 words. The struck-out answers split two ways. Some are the task itself: the meal default (I60-9), how a worker searches (inside I60-10), and the candidate fields (I60-13, I60-14), which Do item I60-17 points to. Others are history, moved to other issues or already done (I60-6, I60-7, I60-8, I60-11, I60-12). The PR description copied every Do and Done when item word for word (P207-d1 to d12), including a struck item (d12), and added only results (P207-d13 to d20). The decisions comment held 13 decisions, and 11 of them say which spec section they went into (P207-c1 to c11, c13); the ones that don't are about code or the drafted brief outline (c12, c14 to c20). It also held the worker brief outline for review, an example brief, and set-asides that were moved into #61's and #64's Do. Results all went in the PR description, none in issue comments. Surprising: the decisions comment opens by saying the decisions were made without Joe, though the issue said 'Settled in: chat' (P207-c0). I60-15's answer was written into the body from the PR three minutes before the PR opened. P207-c8 shows a settled answer that told someone to write it into two specs had not been written in until this PR.

## #77: The fix loop in CI

- Kind: devloop. Era: B issues. PRs: #113.
- Words: 156 at first, 2568 when the first PR opened, 2568 at the end. Saved versions: 32.

Issue #77 ran the code review fix loop in CI, so an agent fixes review findings before Joe reads a PR. The body grew from 156 words on 2026-10-19 to 2,568 words over 32 versions, nearly all on 2026-10-22, the day the PR opened; nothing was added after. Settled questions take most of the words (about 1,980 of 2,568); the Do items are about 360. Most struck-out answers are history: they were already written into code review design 4.5 to 4.7 by PR #108 or done in other PRs (I77-5, I77-6, I77-14, I77-15, I77-16). Four are part of the task, since Do item I77-19 says to make the changes the settled questions say (I77-4, I77-9, I77-11, I77-12). The PR description copied the Do and Done when, but shortened three items and dropped their reasons (P113-d2, d5, d6). What it added was results (P113-d10 to d23). The decisions comment held 10 build decisions, and 8 name the code review design section they went into; c6 names only code and c9 is a config change. It also held a CI check result (c11), one set-aside (c12), and an accepted gap (c13). Results went in the PR description; a separate PR comment held the write-up of the hand runs on #109. Surprising: a Do item (I77-18) is mostly a status report of earlier runs, not an instruction.

## #87: Check which files the reviewer reads on each PR

- Kind: spike. Era: B issues. PRs: none.
- Words: 318 at first, 337 when the first PR opened, 337 at the end. Saved versions: 2.

Issue #87 was a spike to check which files the CI reviewer reads on each PR, since it seemed to skip DEVELOPMENT.md and design/README.md. The body was written once, at 337 words, and never grew (2 versions on 2026-10-21). All the work went into 14 issue comments, about 2,600 words, as the Done when asked (I87-9): one comment per PR review run with what it read and what it found (IC87-0 to IC87-12). So results take most of the words, all in comments. There was no PR. The skill change was made in another issue's PR (#109, commit 92cbf09), which IC87-11 reports. Surprising: a hold decision (IC87-4) was reversed a day later in chat, and the only record of the reversal is one sentence inside a result comment (IC87-11). The closing comment gives the reason in two sentences (IC87-13). No struck-out questions, PR description, or decisions comment exist, so those questions don't apply.

## #129: Spike: whole itinerary reads of long trips

- Kind: spike. Era: C why. PRs: #140.
- Words: 890 at first, 1194 when the first PR opened, 1763 at the end. Saved versions: 10.

This was a spike on how to read the whole itinerary of a long trip, since a 14-day read was too big for Claude Code's tool result limit. The body started at 890 words, was 1,194 when PR #140 opened, and ended at 1,763 after 10 versions. Most of the growth came on 2026-10-26, after the PR opened. Six open questions were added and struck the same day with their answers (I129-15 to I129-22), and Do and Done when were written at 17:06, two minutes before the PR merged. Settled questions are half the words, and a section of #54's measurements (I129-4 to I129-13) is another 29%, as result. The answers under the struck questions are part of the remaining task, not history: they are the agreed design that the next session writes into the docs (I129-25), though several only rule out options (I129-17, I129-18, I129-19). The PR was a research doc, not code, so its description (P140-d0) is task text written fresh, not copied, since the issue had no Do yet. The decisions comment holds one real decision (P140-c1, not written into a design doc), a note that the issue body was fixed (P140-c2), and a forecast of the proposal (P140-c3). That forecast named version F at 17,546 tokens, but the settled read in I129-14 is 15,291, so the comment went out of date. Results went into the body (the #54 section and I129-14) and the research doc. Status went into struck Do items and done marks in Done when (I129-23, I129-24, I129-26).

## #151: Make the whole itinerary read smaller

- Kind: feature. Era: C why. PRs: #153.
- Words: 775 at first, 1027 when the first PR opened, 1027 at the end. Saved versions: 3.

The issue built the slimmer whole itinerary read that #129 settled on. It went from 775 to 1,027 words in 3 versions within about 30 minutes, all before PR #153 opened, and nothing was added after. It is almost all task (83% of its words). The Do items are long and exact: they name functions and files, and spell out the format details the design doc left open (I151-7, I151-8, I151-13). It has no open questions (I151-6) and no struck text. The PR description copies the Do and Done when word for word (P153-d0 to d13) and adds only results (P153-d14 to d19), so it adds nothing to the task. The decisions comment holds 8 implementation choices the issue didn't spell out, such as naming the new detail level "slim" (P153-c1) and where a test file goes (P153-c7). Only one of the 8 says it was written into a design doc (P153-c2, domain model 3.10). Results went only into the PR description.

## #156: Coordinator prompt and tool description fixes

- Kind: fix. Era: C why. PRs: #158.
- Words: 437 at first, 3378 when the first PR opened, 3378 at the end. Saved versions: 9.

The issue gathered 18 gaps in the coordinator's instructions and tool descriptions, from Joe's review of the view file, so they could be fixed in one PR. It grew from 844 to 3,378 words over 9 versions in about two hours on 2026-10-26, all before PR #158 opened. Nothing was added after the PR, which merged four minutes after it opened. About two thirds of the body's words are reason: each item spends most of its words on the problem and an example, then gives a short fix (for example I156-5, I156-11, I156-23). There were no struck questions. The open questions block (I156-40) just says none, since the wording was to be settled in the PR. The PR description added only results (P158-d7 to d9) and otherwise copies the Do and Done when word for word (P158-d0 to d5). The decisions comment is long (1,162 words). Half of it is a per-item log of what each fix became (P158-c1 to c18), which mostly names the doc sections changed. It also has 8 decisions beyond the issue, and only one says it went into a design doc (P158-c19, tool design 2.4). The rest is pointers for Joe's wording review (c27 to c32) and four items set aside into #56's Do (c33 to c36). Results went only into the PR description.

## #169: Check in at the stay before a later stop

- Kind: feature. Era: C why. PRs: #183.
- Words: 740 at first, 1625 when the first PR opened, 1625 at the end. Saved versions: 7.

The issue added a check-in stop, so a day can show the party checking in at the hotel before a later event. It started at 740 words and reached 1,625 by the time PR #183 opened, over 7 versions in about four hours on 2026-10-27. Nothing was added after. Half the words are settled questions (I169-12 to I169-16), each a struck proposal followed by Joe's answer. Those answers are clearly the task, not history. Do I169-17 says to write them into the design docs, and they hold the design, such as the new checkIn kind and how the stop-order check splits a day. A separate Decided section (I169-6, I169-7) holds two choices made outside questions. A "What happened" section records the live session that showed the bug (I169-3), and Done when points back to it (I169-20). The PR description copies Do and Done when (P183-d1 to d8) and adds detailed results (P183-d9 to d15). The decisions comment holds 11 decisions, and 4 name the doc they went into (P183-c0, c1, c2, c11). The rest are code-level choices. It also has wording pointers for Joe and one item set aside into #177 (P183-c14). Results went into the PR description only.

## #199: The workers' trip tools

- Kind: feature. Era: C why. PRs: #201.
- Words: 296 at first, 296 when the first PR opened, 296 at the end. Saved versions: 1.

The issue asked for three tool changes on the trip server for the workers: a facts read, two candidate tools, and moving activities out of the weather tool. The body was written once, at 296 words, and never changed. It is mostly task (63%) and a reason paragraph (I199-1), with no open questions (I199-5). The PR description copied the Do and Done when word for word (P201-d0 to d6) and added test results (P201-d8 to d12). The decisions comment is long, 996 words, almost three times the issue: twelve decisions about input shapes, reply layout, and error text, which is agent-facing work the issue left open. Seven of the twelve were written into tool design 2.1 (P201-c1 to c6, c10), and the other five say why not (P201-c7 to c9, c11, c12). A surprise: the issue said 'Settled in: chat', but Joe asked for the decisions to be made without him (P201-c0). One item was set aside to #60's open questions (P201-c13).

## #209: Saving to the right place: trip brief, itinerary, or trip memory, checked with an evaluation

- Kind: eval. Era: D auto. PRs: #287, #289, #290, #291, #292, #293, #294, #295, #297.
- Words: 840 at first, 3213 when the first PR opened, 7042 at the end. Saved versions: 41.

The issue set up an evaluation of whether the coordinator saves to the right place (trip brief, itinerary, or memory), then changed the instructions and measured the change. It grew from 840 words to 7,042 over 41 versions, and most of the growth came after the first PR (2026-11-10), as each of nine PRs finished a step and its status and results were written back into Do. Task is 42% of the body, but results are 30%, mostly tables and run numbers placed inside Do (I209-33 to I209-36, I209-49 to I209-56), plus status lines such as I209-28 and I209-48. The answers under the eight struck questions are all repeated in Do, so the struck text is history (I209-17 to I209-24). Most PR descriptions copied the Do step they covered; the new text in them is Joe's chat asks quoted as the task (P287-d1, P289-d1, P291-d3), and the last PR's list of what it changed (P297-d1 to d5). One copy differs from the final issue, so the issue was edited after (P294-d3 vs I209-46). The decisions comments hold 56 decisions; 23 say where they were written, mostly evals/saving/decisions.md and DEVELOPMENT.md section 5, and the #295 and #297 comments name no doc for any of their 20. Surprising: Do still says to make smaller changes if runs fail (I209-59), while the ending block says none follow (I209-57).

## #233: search_near drops places hundreds of miles away

- Kind: fix. Era: D auto. PRs: #239.
- Words: 534 at first, 608 when the first PR opened, 608 at the end. Saved versions: 2.

Issue #233 fixed search_near returning places hundreds of miles away, by dropping results beyond 100 miles. The body went from 534 to 608 words in 2 versions on 2026-10-30, and the PR opened and merged the same evening. The block data puts every block's first appearance at 19:51, before the PR, so it doesn't show which block grew. Task items and design pointers take the most words (about 180), then reasons (about 160), the session evidence (about 115) and the one settled question (126). The struck-out answer (I233-9) was part of the task: it set the 100-mile cutoff, as its own setting, that Do item I233-10 uses. The PR description copied the Do and Done when word for word (P239-d1 to d6) and added only results (P239-d7 to d9). The decisions comment held 8 numbered decisions: 5 say which doc they went into (P239-c0 to c3, c5), and the rest are the drafted description wording and test layout (c4, c6, c7). Its set-aside and config sections say nothing. Results went in the PR description. The evidence from the live session went in the issue body (I233-2 to I233-5), and the PR reused those numbers in the Google doc (P239-c5).

## #236: Look back at earlier option sets, and reopen a card after a pick

- Kind: feature. Era: D auto. PRs: none.
- Words: 547 at first, 814 when the first PR opened, 814 at the end. Saved versions: 4.

Issue #236 asked to let the user look back at earlier option sets and reopen a card after a pick. It lived about 25 minutes on 2026-10-30: the body went from 547 to 814 words in 4 versions, then it was closed as not planned. Reasons take about 250 words, and the two settled questions take the most (about 340). The Do and Done when were never written (I236-14, I236-16). The answers under the struck-out questions (I236-10, I236-11) were the task, not history: they are the spec for the card, and the closing comment says they stay in the body in case the issue comes back (IC236-0). Surprising: the closing comment says the body's claim that the agent needs no change (I236-6) was wrong, because the coordinator's instructions describe option cards. There was no PR. The decision and the last status went into the one issue comment (IC236-0).

## #266: The workers send keys their candidate tools refuse, checked with an evaluation

- Kind: eval. Era: D auto. PRs: #284, #285, #286.
- Words: 327 at first, 1035 when the first PR opened, 2740 at the end. Saved versions: 18.

The issue fixed workers sending keys their candidate tools refuse, and measured the fix with a code-scored evaluation. It grew the most of these five: 327 words at first, 1,035 when the first PR (#284) opened on 2026-11-09, and 2,740 at the end, over 18 versions. Most growth came on 2026-11-09 after #284 opened, as Joe settled questions in chat and the Do list took on new steps, decisions and results. By the end the Do section mixes all three. Three Do items are pure results (I266-29, I266-30, I266-33), and a struck Do item holds the decision to leave the rating key alone (I266-31). Two open questions were never struck, even though the work answered them (I266-10, I266-15). Results show up in all three places: the body's Do, issue comments (the corpus count IC266-4, the baseline IC266-6, and run counts in IC266-0 to IC266-3), and the PR descriptions (P285-d8 to d13, P286-d6 to d13). Most struck question answers are task (I266-12, I266-14, I266-16, I266-17), but some just say see Do (I266-11, I266-18). The PR descriptions copy Do items (P285-d2 to d7), but #284's also adds new material: Joe's request from chat (P284-d1), a log of test steps (P284-d13 to d17), and setup steps for running the evaluation (P284-d18 to d29). Across the three decisions comments, 5 of 14 decisions name a doc (P284-c0, P284-c1, P285-c0, P285-c1, P286-c0). One says outright that it was kept out of a doc (P284-c2). One decision that was written into a doc was later found wrong (P284-c1, fixed per I266-23).

## #273: Record the Montana trip - Claude Code

- Kind: recording. Era: D auto. PRs: none.
- Words: 361 at first, 350 when the first PR opened, 350 at the end. Saved versions: 3.

The issue asked for one simulated-user run of the Montana trip with the skeptic persona, recorded in Phoenix. Its body was written once and trimmed slightly, with no PR. Task items (55%) and reasons (37%) fill it; the reasons explain what the run adds to the corpus and why the final itinerary isn't compared to an expected one (I273-1, I273-2). All results went in one long issue comment (IC273-0), 816 words, more than twice the body, as the issue's Ends in asked (I273-12). That comment covers whether the run stuck to the trip file, refused tool calls, a memory mismatch from earlier runs, and the app bug it filed (#281). There were no struck questions and no decisions comment.

## #282: General evaluator: grounded in the record

- Kind: eval. Era: D auto. PRs: #283.
- Words: 1748 at first, 2774 when the first PR opened, 2774 at the end. Saved versions: 16.

The issue built the first general evaluator, 'grounded in the record', and was meant to teach the Phoenix judge process: rubric, golden set from two labelers, tuning a Haiku judge, and a corpus run. It grew from 1,772 to 2,774 words over 16 versions, all before the PR opened, as Joe's chat decisions were written into Do (for example I282-21, I282-25, I282-28 to I282-31). Task makes up 70% of the body, but many Do items are dated decisions with reasons and data folded in. The three struck questions' answers were already moved into Do or other blocks, so they are history (I282-13, I282-14), except I282-15, whose answer appears nowhere else. The PR description is 92% copy of the issue's Do and Done when (P283-d0 to d30), and its only new text is the results lines (P283-d32 to d36). Results went in two issue comments (IC282-0, IC282-1), not the body. The decisions comment is short: three of seven decisions say they were written into DEVELOPMENT.md section 5 (P283-c2 to c4), one went only into the issue (P283-c1), and two items were set aside with no issue (P283-c10, P283-c11).
