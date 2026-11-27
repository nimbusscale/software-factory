# Software factory

## Doc map

| Doc | Path |
|---|---|
| Doc standards | `plugin/skills/standards/` |
| Functional spec | `docs/functional-spec.md` |
| Technical spec | `docs/technical-spec.md` |
| Blueprints | `docs/blueprints/` |
| Doc check script | `plugin/skills/standards/check_docs.py` |
| Code check script | `tools/check-code.sh` |
| GitHub standards | `plugin/skills/standards/github.md` |
| Review rubric | `plugin/skills/standards/review-rubric.md` |
| Code comment standards | `plugin/skills/standards/code-comments.md` |
| Test standards | `plugin/skills/standards/tests.md` |

Before you write, change or review a doc, or code that a doc describes, read
`plugin/skills/standards/SKILL.md`. If you can't find the standards, stop and say so in your report.
Don't write the docs from memory of them.

Work that changes the Python code in `src/` is done only when `bash tools/check-code.sh` passes.

Before you start work on an issue, write an issue or the summary in a PR's description, or update
an issue, read `plugin/skills/standards/github.md`.

Before you add, change or delete a code comment, move code that has comments, or review a change
that does, read `plugin/skills/standards/code-comments.md`.

Before you write or change a test, read `plugin/skills/standards/tests.md`.
