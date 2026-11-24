# Software factory

## Doc map

| Doc | Path |
|---|---|
| Doc standards | `docs/standards/` |
| Functional spec | `docs/functional-spec.md` |
| Technical spec | `docs/technical-spec.md` |
| Blueprints | `docs/blueprints/` |
| Doc check script | `tools/check-docs.sh` |
| Code check script | `tools/check-code.sh` |
| GitHub standards | `docs/standards/github.md` |
| Review rubric | `docs/standards/review-rubric.md` |
| Code comment standards | `docs/standards/code-comments.md` |

Before you write, change or review a doc, or code that a doc describes, read
`docs/standards/README.md`. If you can't find the standards, stop and say so in your report.
Don't write the docs from memory of them.

Work that changes the Python code in `src/` is done only when `bash tools/check-code.sh` passes.

Before you write an issue or the summary in a PR's description, or update an issue, read
`docs/standards/github.md`.

Before you add, change or delete a code comment, move code that has comments, or review a change
that does, read `docs/standards/code-comments.md`.
