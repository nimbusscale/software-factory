---
name: code-comments
description: How to write, change and review code comments, including doc comments on functions, types and fields, and the top comment of a file or script. Use this whenever you're about to add, change or delete a comment, move code that has comments, or review a change that adds or changes comments, even if the task is only a code change and says nothing about comments. The `project-docs` skill decides whether a fact belongs in a comment or a doc. This skill decides whether a comment is needed, and how to write it.
---

# Code comments

Most readers of comments are agents. An agent nearly always reads a file before it edits it, so a
comment next to a function is in view when the function changes. That makes a comment the best
home for a fact that one place in the code owns. It also means an agent reads every comment near
the code it changes, and follows a wrong one. Nothing fails when a comment is wrong, so it goes
stale quietly.

Work through the steps in order. When you're unsure whether a comment earns its place, read
`references/worked-examples.md`. It sorts real comments from an earlier project.

## 1. Decide whether to write one

The default is no comment. The test is to imagine the comment gone, and ask what the next reader
would get wrong. If you can't name something, don't write it.

The next reader is a caller or a maintainer. A caller sees the name, the signature and the types,
and won't read the body. A maintainer reads the body, and is about to change it.

Most of what a comment could say has a better home, one that can't go stale:

- **A better name,** such as one that carries its unit: `timeoutMilliseconds`.
- **A smaller function,** whose name says what a block does.
- **A type,** for what kind of value it is, which values are allowed, or whether items repeat. In
  TypeScript, a union or a `ReadonlySet`. In Python, a `Literal`, an `Enum` or a `NewType`, when
  the project runs a type checker such as mypy or pyright. In Go, a named type with constants.
- **An error with a clear name,** which explains itself to the caller who gets it.
- **A test,** for behavior an example would show.
- **The comment where the thing is defined.** If a field's comment says what null means, a function
  that passes the value along doesn't say it again.

When the code does less than its name says, such as a `saveAll` that skips items that haven't
changed, rename it. If you can't rename it, a comment says what it skips.

A declaration being exported isn't a reason to comment it. Neither is every other function in the
file having a comment. The exception is a comment a linter requires, such as Go's doc comment on
each exported name. Keep it to one short sentence.

## 2. Decide what it holds

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
  checks, a rule from a spec, or a line of a prompt. Cite the spec item's ID, or name the test.
- **Commented-out code, and TODOs.** Version control keeps the old code. Work left to do is an
  issue.
- **Terms a reader can't decode without a doc,** such as a doc's private marker. Say what the term
  means for this code.

## 3. Write only what you can show

Every claim in a comment needs a source you checked:

- **A reason** comes from where the choice was made: a spec item's Why, the task or issue, the
  owner, a measurement, or a test that fails without the code. Check any part of it that describes
  this code in the code itself.
- **A quirk** comes from the service's docs, or a saved response that shows it.
- **An ID** comes from the spec. Check that the item says what this code does.

The comment states the reason in the present tense. It doesn't cite the issue or the chat it came
from, since that's history.

When you write the code, you usually have the reason. When you comment code you didn't write, you
usually don't. Find it, or ask, and leave the comment out until you know. Don't write a reason that
only sounds right. If you can't explain clearly why the code is this way, the code may need to
change more than the comment does.

## 4. Place it

- Put it next to the smallest piece of code it explains.
- What a field means goes on that field, once. A type's comment holds only what spans its fields.
- A reason for one line goes right above that line.
- A file's top comment says what the module is for, when its name doesn't. A script's top comment
  says how to run it, so no doc has to.
- Follow the repo's comment syntax.

## 5. Write it

- Use plain words and full sentences, one idea per sentence, in the present tense.
- Use the code's names, and the terms the functional spec defines.
- Join a reason to what it explains with "so", "because" or "otherwise".
- Cite IDs, never section numbers or headings, since those change when a doc is reorganized.
- Never cite a blueprint or a research doc. A blueprint is archived once its code is built, and a
  research doc is frozen. State the fact the comment needs instead.
- A citation doesn't replace a reason. If the reason fits in a sentence, write the sentence. When
  it's a spec item, cite the ID too.

## 6. Keep comments true when the code changes

- When you change code, read the comments on it. Change or delete each one that no longer holds, in
  the same change. A wrong comment is a bug.
- When you move code, move its reasons with it.
- When a comment has nothing left that's true and needed, delete it.

## 7. Check the change

When you add or change comments, do these checks before you count the work as done. When you
review a change, do them on that change.

**Run the scripts.** If the project has the `project-docs` skill, its `scripts/check-docs.sh`
checks that each ID cited in the code resolves. It also flags text that a doc shares with a source
file. Then list history in the comment lines the change added:

```bash
git diff <base branch> -U0 -- . ':(exclude)*.md' \
  | awk '/^\+\+\+ /{f=substr($0,7)} /^\+[[:space:]]*(\/\/|#|\*|\/\*)/{print f": "substr($0,2)}' \
  | grep -iE '#[0-9]+|\b20[0-9]{2}-[0-9]{2}-[0-9]{2}\b|\b(settled|decided|for now|so far|no longer|used to|previously|the new)\b'
```

Each line it prints is only a signal. "The count no longer matches" can be a real use. Look at each
one, and fix it if it's history.

**Then read each comment the change added or changed:**

- If it were gone, what would the next reader get wrong? If nothing, delete it.
- Does it hold only what step 2 allows? Is each claim shown, as step 3 asks?
- Do the comments on the code the change touched still hold?

A wrong comment is a fix in the change, not a review note. So is a comment that only says what the
code does: delete it. How a reviewer reports what it found is up to the project's workflow.
