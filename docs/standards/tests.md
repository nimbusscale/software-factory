# Tests

The standards for a project's tests: which tests are written, how each one names the rule it
checks, and how an acceptance test is written. They cover each test a change adds or changes.
Tests already in a repo aren't changed to meet them.

A test is worth its cost when its expected value comes from somewhere the code's author didn't
write, such as a spec item or a test written before the work. A test written after the code copies
its expected values from that code. When the author misreads the issue, the code and the test are
wrong in the same way, and the test passes.

## Each test names the rule it checks

The rule is the ID of a spec item, such as an `FR`, `TR`, `TD` or `CS`, or the bug the test guards
against. For example, FR-5 says the loop refuses a run with fewer than 1 round. A test that passes
0 and checks for the refusal names FR-5.

The name goes in a comment right above the asserts that check the rule:

```python
# FR-5.
assert "at least 1 round" in str(error.value)
```

A comment can name several IDs, such as `# FR-5, FR-26.`, when the asserts below it check each of
them. When one test checks different rules in different asserts, each group of asserts gets its own
comment.

A test that guards against a bug names it with `Bug:` and a sentence that says what went wrong,
such as `# Bug: a settings file saved in Latin-1 was refused as invalid TOML.` The marker sets the
comment apart from other comments, so a reader can tell why the test is there. Like any comment,
it holds no issue number or date.

## A test with no rule to name isn't written

A test that checks a helper returns the same list it returns today names nothing, so it isn't
written.

*Why:* each test costs something to read, write and keep up to date. A test with no rule to name
checks only that the code does what it does today, so it pays back none of that cost.

## How an acceptance test is written

An acceptance test checks one of an issue's acceptance criteria. It's written before the work, from
the issue's acceptance criteria. It tests from the outside, through the project's commands, its API
or its files, never its internals. It names the `FR` or `TR` it checks, as above. It fails before
the work is done.
