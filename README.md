# software-factory

## Setup

Install [uv](https://docs.astral.sh/uv/), then run these once in each clone:

```sh
uv sync
uv run lefthook install
```

The second command adds the pre-commit hook, which runs `tools/check-code.sh` on any commit that
changes the code or the check's config.
