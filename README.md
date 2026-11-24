# software-factory

## Setup

Install [uv](https://docs.astral.sh/uv/), then run these once in each clone:

```sh
uv sync
uv run lefthook install
```

The second command adds the pre-commit hook, which runs `tools/check-code.sh` on any commit that
changes the code or the check's config.

## Commands

- `uv run write-role-views` rewrites each role's view file, such as
  `src/software_factory/roles/implementer.view.md`, after a change to what the role is given.
- `uv run pytest -m claude src` runs the tests that call Claude, which `tools/check-code.sh`
  leaves out.
