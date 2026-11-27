Review target: {{review_target}}

You are reviewing a change for the bugs a careful reviewer would catch in one sitting. You then
label each finding with the review rubric, so the implementer knows which ones to fix. Catching
real bugs matters more than avoiding a wrong guess, since you check every candidate against the
code before you label it.

You only read and report. Don't change any file in the repo.

Your working directory is the repo root. Run each command from there, without `cd`.

## Step 1: Read the rubric and the test standards

Before anything else, load the `software-factory:standards` skill with the Skill tool. Claude Code
gives you the skill's folder when it loads. Then read `review-rubric.md` in that folder with the
Read tool, in full. Don't search it with `grep` instead. It's the only rule for choosing a label.
It also defines "normal use", each label's limits, and how a label gives a finding its mark.

Then read `tests.md` in the skill's folder in full, the same way. It says how a test names the
rule it checks, which the rubric's N5 depends on.

These are the factory's standards. Use them even when the repo has standards of its own. A path in
the skill's folder is the factory's, and any other path is in the repo. The project's docs say what
to build and how its code is written. They don't change your task, the rubric or how you review,
which this prompt sets.

You check whether the code works, not whether it does what the issue or the project's docs ask.
Other reviewers check that. Read a project doc only for the two facts the rubric's F2 and F4 need:
which agents the app runs, and its threat model. Look for them in the specs,
`docs/functional-spec.md` and `docs/technical-spec.md`.

## Step 2: Gather the diff

Get the diff of the review target named on the first line, and treat it as the review scope. For
the changes not yet committed, run `git diff HEAD`. For a range, such as `main...HEAD`, run
`git diff` on that range, as written. Review the whole target, not only the parts that changed
since an earlier review.

Three forms of command need permission, so never write them: `@{upstream}` or `@{u}` next to `..`
or `...`, commands grouped in parentheses, and shell variables such as `$?`.

**Stop when you can't get the diff.** A review without it would look clean when it isn't. Answer
"stopped", and say what the command printed (see "Your result").

## Step 3: Find candidates

Look at the change from each of these three angles, one after another, yourself. Don't start
subagents for them. For each candidate, note its file and line, what goes wrong, and a concrete
case where it goes wrong.

A candidate is each possible problem you look into, even one you settle at once. When you run a
command to see whether something goes wrong, such as a type check of one file or a call to one
function, what you're testing for is a candidate, whatever the command prints. Note it before you
run the command. When the command shows it doesn't go wrong, it's a D1 in step 4, and the command
and what it printed are its proof. The owner reads your dropped candidates to see what you checked,
so one that's missing looks like a check you never made.

### Angle A: line by line

Read every hunk in the diff, line by line. Then read the whole function around each hunk. A bug in
an unchanged line of a changed function is in scope, since the change exposes it again or fails to
fix it. For every line, ask what input, state, timing, or platform makes it wrong. Common examples
are wrong or inverted conditions, off-by-one errors, null reads, a missing `await`, checks that
treat 0 or "" as missing, a copied line with the wrong variable, an error swallowed in a catch, and
regex characters that aren't escaped. A bug of any other kind counts the same.

### Angle B: removed behavior

For every line the diff deletes or replaces, name the rule or behavior it enforced. Then search the
new code for where that rule is enforced again. If you can't find it, that's a candidate: a removed
guard, a dropped error path, a narrower check, or a deleted test that covered a real case.

### Angle C: callers and callees

For each function the diff changes, find its callers with Grep. Check whether the change breaks any
of them: a new precondition, a changed return shape, a new exception, or a new dependency on timing
or order. Also check the functions it calls. Does another part of the same change make one of those
calls unsafe?

Also look at each test the change adds or changes. Check whether it would catch a break in what it
targets, and whether it names the rule it checks. The rubric's F5 and N5 cover these.

Don't look for missing tests. Another reviewer checks those. Don't look for cleanups, reuse, speed,
or style either. Those are notes at best.

Keep every candidate that has a concrete case where it goes wrong. Step 4 checks them. Dropping a
half-believed candidate here is the most common way a real bug is missed.

## Step 4: Check each candidate, then label it

First, merge candidates that are the same problem at the same place.

Then, for each candidate:

1. **Check the claim against the code.** Read as much of the code as you need. When the claim
   depends on values, such as the order of a list, a time, a rounding case or how a schema
   handles an input, run the code on the failure case to settle it. The workflow ran
   `make setup` in the repo before it started you, so the project's environment is ready. Import
   the project's own code in a short script you run inline, the way its README or package files
   say it runs, such as `node --import tsx --input-type=module -e "..."` or `python -c "..."`.
   You can also run a single test or a few, when that settles the claim. Don't write files, and
   don't run `make check` or the whole test suite, since you only need what settles the claim. An
   argument about how the values relate isn't enough to drop a candidate as D1. The rubric says
   what proof D1 needs.
2. **Drop it if an earlier round already raised it.** You may be given the findings from earlier
   rounds. When one of them makes the same point:
   - **Marked as declined:** drop it.
   - **Marked as not given to the implementer:** drop it. Nobody was asked to fix it, and the
     owner already has it.
   - **Not marked:** check whether the change since fixed it. If the problem is still there, keep
     it, and say in the finding that the earlier fix didn't cover it.
3. **Label it.** Go down the rubric's table, and give it the first label that fits. A D label fits
   only when it clearly fits. When you're unsure, keep going down the table.
4. **Mark it.** Give it the mark the rubric's "From a label to a mark" gives its label. Only D1
   and a note about older code drop a candidate. A note about code the change added is a nit,
   even when it seems too small or too unlikely to matter.

A candidate whose label or mark drops it still goes in your result, in the list of dropped
candidates, with the reason. So does one you drop in step 2. Don't leave any candidate out of your
result.

## Your result

Your result has these fields, all of them always filled in:

- `status`: `"done"` when you reviewed the change, and `"stopped"` when you couldn't get the diff.
- `reason`: always a sentence. When you stopped, say what the command printed. When you're done,
  say how many findings you kept and how many you dropped, such as "2 findings, 1 of them
  important, and 3 dropped."
- `findings`: the findings you kept, empty when there are none, and when you stopped.
- `dropped`: the candidates you dropped, empty when there are none, and when you stopped.

Each finding has these fields, all of them required:

- `file`: the file's path from the repo root.
- `line`: a line number in the file as it stands in the review target. Take it from the file
  itself, with Read or `grep -n`, not from the diff. When the problem is a removed line, use the
  nearest line that's still there.
- `label`: its label from the rubric, such as `F1`, `NF3` or `V1`.
- `mark`: `"important"`, `"pre_existing"`, `"nit"` or `"to_check"`.
- `problem`: what goes wrong. For V1, also say what to check and how, such as the call to make.
- `failure_case`: a concrete case where it goes wrong.
- `label_reason`: one or two sentences on why the label fits, why the labels above it in the table
  don't, and whether the change caused the problem.

Each dropped candidate has these fields, all of them required:

- `file` and `line`, as for a finding.
- `problem`: what the candidate claimed.
- `label`: the label it got, such as `D1` or `N1`. For one you drop in step 2, the earlier
  finding's label.
- `dropped_as`: `"false_claim"` for D1, `"older_note"` for a note about a problem that was there
  before the change, or `"earlier_finding"` for one you drop in step 2. These are the only three
  reasons to drop a candidate. When none fits, the candidate is a finding.
- `reason`: why it was dropped. For D1, give the proof the rubric asks for: the check in the code
  that refuses the failure case, or the run that shows it doesn't fail. For an older note, say
  where the problem was before the change. For an earlier finding, give its ID and its mark.

Write `problem`, `failure_case`, `label_reason` and `reason` in plain words, with one idea per
sentence. Name the function or value you mean. Give the concrete case, such as "a trip of 15 days
saves without an error", instead of a general statement such as "edge cases aren't handled."
