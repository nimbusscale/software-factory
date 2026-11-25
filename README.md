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
- `uv run set-board-statuses <owner/name>` sets the statuses on a project's board from
  `src/software_factory/factory.toml`, the factory's own config. It uses the GitHub CLI's login,
  and keeps the board's other statuses.
- `uv run implementation-loop <owner/name> <issue number>` runs the implementation loop on one
  issue of a project, and opens a PR for its work. `--rounds <number>` sets the number of rounds
  for this run. It uses the GitHub CLI's login, and keeps each project's clone and each run's
  working copy in `~/.local/share/software-factory`, or in `$XDG_DATA_HOME/software-factory`
  when that's set.
- `uv run pytest -m claude src` runs the tests that call Claude, which `tools/check-code.sh`
  leaves out.

## A project's settings

A project can set the number of rounds and each role's turn cap in `software-factory.toml`, at
the root of its repo. The `[settings]` table in `src/software_factory/factory.toml` lists each
setting and the factory's default for it. A run reads the file from the project's default branch,
and uses the default for each setting the file leaves out. For example:

```toml
rounds = 2

[turn_caps]
implementer = 60
```

The factory can run on this repo too, since it's a project like any other.
