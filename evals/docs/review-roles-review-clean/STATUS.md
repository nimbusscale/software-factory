# Status

Last run: 2026-11-25, with the standards in the factory plugin and the skill description that
names the tasks it's for. It passed 2 of 3 runs. Every earlier run, from 2026-11-17 to
2026-11-19, passed, and so did 4 runs on main (`96d8a1e`) on 2026-11-25.

## Known failure

`03-reports-no-problems` fails when the reviewer says it found no problems, then adds a remark about
the code that the doc checks don't cover. The remarks seen so far:

- The repo has no tests, so nothing tests FR-3.
- `send_email` only adds the message to `outbox`, and nothing in the repo sends it.
- The docstring of `cancel_no_shows` repeats FR-3's rule next to its ID.
- FR-3's "the member the booking was for" differs from FR-1's "the member the booking is for",
  given as an optional tweak under "Problems in this change".

The judges take each one as a problem the reply reports. `reviewing.md` says a bug in the code that
doesn't make a doc wrong is left out of the review and not mentioned.

The first remark grew with the skill's description, which a reviewer reads first in `SKILL.md`. A
description that listed tests among what the standards cover led the reviewer to read `tests.md`
in 3 of 4 runs, and the case passed 1 of 4. A description about docs alone passed 3 of 3. One
that named the tasks and said to read only the files a task needs passed 3 of 4. The current one,
which names the tasks and leaves reading to the body of `SKILL.md`, passed 2 of 3, and no run read
`tests.md`.

If it keeps failing this way, two changes could fix it. `reviewing.md` could say that a missing
test isn't part of the doc checks either. Or the case's docstring could cite FR-2 and FR-3 alone,
which takes away the third remark.
