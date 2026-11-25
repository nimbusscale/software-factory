# Code comments

The standards for code comments, including doc comments on functions, types and fields, and the top
comment of a file or script: when a comment is needed, what it holds, and how it's written and
checked. Which facts have their home in a comment is decided by "Which doc a fact goes in", in
`project-docs.md` in this folder.

Most readers of comments are agents. An agent nearly always reads a file before it edits it, so a
comment next to a function is in view when the function changes. That makes a comment the best home
for a fact that one place in the code owns. It also means an agent reads every comment near the code
it changes, and follows a wrong one. Nothing fails when a comment is wrong, so it goes stale
quietly.

## When a comment is needed

The default is no comment. The test is to imagine the comment gone, and ask what the next reader
would get wrong. If you can't name something, don't write it. Test each claim in a comment on its
own, since one claim can pass while the rest of the comment fails.

The next reader is a caller or a maintainer. A caller sees the name, the signature and the types,
and won't read the body. A maintainer reads the body, and is about to change it.

Most of what a comment could say has a better home, one that can't go stale:

- **A better name,** such as one that carries its unit: `timeoutMilliseconds`. A name also fixes a
  call that looks like dead code, such as a lookup whose result is thrown away because it's only
  there to refuse a bad input.
- **A smaller function,** whose name says what a block does.
- **A type,** for what kind of value it is, which values are allowed, or whether items repeat. In
  TypeScript, a union or a `ReadonlySet`. In Python, a `Literal`, an `Enum` or a `NewType`, when
  the project runs a type checker such as mypy or pyright. In Go, a named type with constants says
  which values are meant. Go still accepts any other value of the base type, so check values where
  they come into the program. A comment on what a value is, such as "each once", usually means a type is
  missing.
- **An error with a clear name,** which explains itself to the caller who gets it. The code that
  throws it is its home. A function doesn't list the errors that come up from code it calls.
- **A test,** for behavior an example would show.
- **The comment where the thing is defined.** If a field's comment says what null means, a function
  that passes the value along doesn't say it again.

When the code does less than its name says, such as a `saveAll` that skips items that haven't
changed, rename it. If you can't rename it, a comment says what it skips.

A declaration being exported isn't a reason to comment it. Neither is every other function in the
file having a comment. The exception is a comment a linter requires, such as Go's doc comment on
each exported name. Keep it to one short sentence.

## What a comment holds

A comment that passes the test nearly always holds one of these, since no name or type can:

- **A reason:** why the code is this way, when a reader would otherwise change it. "Docker stops a
  container with SIGTERM. Node ignores it by default when it's the container's first process, so
  Docker would wait 10 seconds and then kill it." Name a rejected option only when an agent would
  likely change the code back to it.
- **A quirk of an outside service** that this code handles, in general terms. "Open-Meteo refuses
  requests sent all at once with 'Too many concurrent requests', so this asks for one year at a
  time." A test with a saved response, named after the quirk, checks the handling.
- **The ID of the requirement or decision this code carries out,** such as `FR-12` or `TD-4`, when
  this code is the place it's carried out.
- **In a test, the rule the asserts below it check:** a spec item's ID, such as `# FR-5.`, or
  `Bug:` and what went wrong. `tests.md` in this folder says how it's written.

Anything else has to pass the test on its own.

These stay out:

- **What the code does, at the code's own level.** "One worker's recorded calls" above
  `interface WorkerRecord` says nothing the name doesn't.
- **History:** issue and PR numbers, the date something was decided, and words such as "settled",
  "now", "no longer", "so far" and "the new". History goes in the commit message. The date a number
  was measured is fine, since a reader needs it to judge whether the number still holds.
- **Facts about the rest of the system today,** such as "no caller passes null yet". They go stale
  when other code changes, and nothing points back to the comment. If the code depends on the fact,
  make a type or a check enforce it.
- **A copy of text that has another home,** such as an example of output that a test already
  checks, a rule from a spec, or a line of a prompt. When the format changes, the test is fixed and
  the comment goes stale. Cite the spec item's ID. A test needs no pointer when a reader finds it by
  the code's name.
- **Commented-out code, and TODOs.** Version control keeps the old code. Work left to do is an
  issue.
- **Terms a reader can't decode without a doc,** such as a marker from a diagram in a design doc.
  Say what the term means for this code, then test the comment again. In plain words it often
  turns out to be a copy.

## Where a claim comes from

Every claim in a comment needs a source you checked:

- **A reason** comes from where the choice was made: a spec item's Why, the blueprint that held
  the decision until the code existed, the task or issue, the owner, a measurement, or a test that
  fails without the code. Check any part of it that describes this code in the code itself.
- **A quirk** comes from the service's docs, or a saved response that shows it.
- **An ID** comes from the spec. Check that the item says what this code does.

When you write the code, you usually have the reason. When you comment code you didn't write, you
usually don't. Find it, or ask for it in your report, and leave the comment out until you know.
Don't write a reason that only sounds right. If you can't explain clearly why the code is this way,
the code may need to change more than the comment does.

A comment a reader can't make sense of goes, even when part of it is true. Keep part of a reason
only when that part, on its own, tells a reader what not to change.

## Where it goes

- Put it next to the smallest piece of code it explains.
- What a field means goes on that field, once. A type's comment holds only what spans its fields.
- A reason for one line goes right above that line.
- A file's top comment says what the module is for, when its name doesn't. A script's top comment
  says how to run it, so no doc has to.
- Follow the repo's comment syntax.

## How it's written

- Use plain words and full sentences, one idea per sentence, in the present tense. A citation such
  as `// Meets FR-31.` can be that short.
- Use the code's names, and the terms the specs define.
- Join a reason to what it explains with "so", "because" or "otherwise". A comment has no `*Why:*`
  line.
- State the reason itself. Don't cite the issue or the chat it came from, since that's history.
- Cite IDs, never section numbers or headings, since those change when a doc is reorganized.
- Never cite a blueprint or a research doc. A blueprint is archived once its code is built, and a
  research doc is frozen. State the fact the comment needs instead.
- When a spec item holds the reason, cite its ID alone, such as `// Meets FR-31.` Don't restate
  the item, since a copy drifts when the item changes.
- When the point is something the code doesn't do, name that part, then cite the ID, such as
  `// A started trip can be deleted too (FR-12).` A bare ID wouldn't say which check not to add.
- When no spec item holds the reason, write the reason as a sentence.

## When the code changes

- When you change code, read the comments on it. Change or delete each one that no longer holds, in
  the same change. A wrong comment is a bug.
- When you move code, move its reasons with it.
- When a comment has nothing left that's true and needed, delete it.

## Examples

**A pointer on a "what".** The fields are named `model` and `effort`, and the type's name says whose
they are. The section number gives no reason, and it breaks when the spec is reorganized. Delete the
comment.

```ts
// The leg scout's own model and effort settings (technical spec section 10).
export interface LegScoutDefinitionGiven {
  model: string;
  effort: EffortLevel;
}
```

**A check the code doesn't make.** Most changes to a trip are refused once it has started, and a
requirement says a started trip can still be deleted. Before:

```ts
// Removes the trip and everything that belongs to it (persistence design, section 6).
// It isn't a write, so it runs on a started trip too. It waits for a write in
// progress, and refuses once that takes longer than the lock wait.
async deleteTrip(tripId: string): Promise<void> {
```

The first sentence restates a requirement, with a section number. The third describes waiting and
an error that are already written once, in the function that takes the lock. The second holds what
a maintainer needs: without it, they could add the started-trip check here to match. After:

```ts
// A started trip can be deleted too (FR-12).
async deleteTrip(tripId: string): Promise<void> {
```

**A reason a maintainer would otherwise undo.** Without it, a maintainer would likely split this
into two clearer errors, and so tell a caller which items exist.

```ts
// This is the same error for an ID that doesn't exist and for another user's or another
// trip's item, so it doesn't say whether someone else's item exists.
export const NO_SUCH_MEMORY_ITEM = "No such memory item.";
```

## Checking comments

Do these checks when you add, change or delete comments, or move code that has them, before you
count the work as done. When you review a change that does, do them on that change. "Your change or
someone else's" in `reviewing.md` says what to do with what you find.

Copy this checklist into your task list and tick off each check:

```
- [ ] Run the doc check script and the history check
- [ ] Each comment the change added or changed passes the test
- [ ] Each one holds only what a comment holds, from a source you checked
- [ ] The comments on the code the change touched still hold
```

**Run the doc check script,** at the path CLAUDE.md's doc map gives. It checks that each ID cited in
the code resolves, and flags text a spec shares with a source file. Then list history in the comment
lines the change added:

```bash
git diff <base branch> -U0 -- . ':(exclude)*.md' \
  | awk '/^\+\+\+ /{f=substr($0,7)} /^\+[[:space:]]*(\/\/|#|\*|\/\*)/{print f": "substr($0,2)}' \
  | grep -iE '#[0-9]+|\b20[0-9]{2}-[0-9]{2}-[0-9]{2}\b|\b(settled|decided|now|yet|so far|no longer|used to|previously|the new)\b'
```

Each line it prints is only a signal. "The count no longer matches" can be a real use. Look at each
one, and fix it if it's history. It only sees lines that start with a comment marker, so it misses a
comment at the end of a line of code, and Python docstrings. Read those yourself.

**Then read each comment the change added or changed:**

- If it were gone, what would the next reader get wrong? If nothing, it goes, unless a linter
  requires it.
- Does it hold only what "What a comment holds" allows? Is each claim from a source you checked?
- Do the comments on the code the change touched still hold?

A wrong comment is a problem in the change, not a matter of taste. So is a comment that only says
what the code does.
