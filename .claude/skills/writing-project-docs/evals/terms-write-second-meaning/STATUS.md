# Status

Last run: 2026-11-18, on commit `380e60a`, 3 runs with the skill. It passed 1 of 3. Its last runs
without the skill passed 3 of 3.

## Known failure

`01-free-has-one-meaning` failed in 2 runs. Both writers defined a Free slot term, and also wrote a
requirement that bookings are "only free of charge", such as "The app shall book every room only
free of charge, never asking a member for payment."

`terms-review-word-uses` showed the same thing when issue 58 merged `terms-review-second-meaning`
into it. With the skill, reviewers let "free of charge" through, or mentioned it only in passing.
Without the skill, they flagged it 3 of 3. `terms-review-second-meaning` on its own still passes.
A likely cause is the set-phrase rule from issue 42, which says a set phrase no reader could take
for the term is fine. That rule hasn't been tested as the cause yet.
