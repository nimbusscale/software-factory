Review target: {{review_target}}

`high effort → 3 inline angles (bugs) → dedup (no verify) → every finding`

You are reviewing for **recall** at high effort: catch every real bug a careful
reviewer would catch in one sitting. At this level, catching real bugs matters
more than avoiding false positives. Err on the side of surfacing.

## Phase 0 — Gather the diff

Get the unified diff of the review target named above, and treat it as the
review scope. For the changes not yet committed, run `git diff HEAD`. For a
range, such as `main...HEAD`, run `git diff` on that range, as written. Three
forms need permission, so never write them: `@{upstream}` or `@{u}` next to `..`
or `...`, commands grouped in parentheses, and shell variables such as `$?`.

## Phase 1 — Find candidates (3 correctness angles)

Run **3 independent finder angles** in sequence yourself, in THIS context — do NOT spawn subagents for them. Each
surfaces candidate findings with `file`, `line`, a short `summary`, and a
concrete `failure_scenario`.

### Angle A — line-by-line diff scan

Read every hunk in the diff, line by line. Then Read the enclosing function for
each hunk — bugs in unchanged lines of a touched function are in scope (the PR
re-exposes or fails to fix them). For every line ask: what input, state, timing,
or platform makes this line wrong? Look for inverted/wrong conditions,
off-by-one, null/undefined deref, missing `await`, falsy-zero checks,
wrong-variable copy-paste, error swallowed in catch, unescaped regex metachars.

### Angle B — removed-behavior auditor

For every line the diff DELETES or replaces, name the invariant or behavior it
enforced, then search the new code for where that invariant is re-established.
If you can't find it, that's a candidate: a removed guard, a dropped error
path, a narrowed validation, a deleted test that was covering a real case.

### Angle C — cross-file tracer

For each function the diff changes, find its callers (Grep for the symbol) and
check whether the change breaks any call site: a new precondition, a changed
return shape, a new exception, a timing/ordering dependency. Also check callees:
does a parallel change in the same PR make a call unsafe?

Pass every candidate with a nameable failure scenario through — finders that
silently drop half-believed candidates are the dominant cause of misses.

## Phase 2 — Dedup only (no verify)

Pool all candidates. Dedup near-duplicates only (same defect, same location, same reason → keep one). Do NOT run verifiers; do NOT re-judge. Give each finding that is left its `severity`, as Output defines it. Sort by severity.

## Output

Report every finding that is left, each candidate with a nameable failure
scenario, even if there are only one or two.

Return findings as a JSON array of objects:

```json
[
  {
    "id": "F1",
    "file": "path/to/file.ext",
    "line": 123,
    "summary": "the problem, where it happens and what sets it off. Fix: the change to make",
    "failure_scenario": "concrete inputs/state → wrong output/crash",
    "severity": "one of: important, nit, pre_existing"
  }
]
```

Every object carries every key shown above. Its `id` is `F` and its place in
the list, starting from `F1`. Its `severity` is one of:

- `important`: a bug that should be fixed before merging because this change
  adds it or makes it worse. If someone can hit it, a rare trigger does not
  lower the severity.
- `nit`: a minor issue, worth fixing but not blocking, such as a bug that harms
  nobody, like a misleading log line. A bug that a user of the code can hit is
  never a nit, even when a design doc describes the behavior that causes it.
- `pre_existing`: a bug that exists in the codebase but that this change did
  not introduce. A bug in unchanged lines is `pre_existing` if the change only
  fails to fix it, and `important` if the change re-exposes it.

A severity only labels and orders a finding: never drop one for its severity.
Most severe means `important`, then `pre_existing`, then `nit`.

Write each `summary` in two or three short sentences. Start with the problem as
a user of the code would see it. Next say where it happens and what sets it
off. End with "Fix:" and the change to make, or what to check if you are not
sure.

Beyond Phase 2's dedup, if the same mistake is repeated in several places,
report it once and name the other places in its `summary`. Different mistakes
stay separate findings, even when one change would fix them all.

Ranked most-severe first. If nothing survives, return `[]`. Do not call the
ReportFindings tool even if it is available - this review's
output contract is the JSON block above.
