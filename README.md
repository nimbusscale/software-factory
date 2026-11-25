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

## Running the factory

Each run happens in its own SFE, a Docker container that holds the factory at `/factory` and is
thrown away when the run ends.

- `bash tools/build-sfe.sh` builds the SFE's image from the checkout's commit. It tags the image
  with its factory version, which is the commit's short ID, and as `latest`. It refuses a checkout with changes
  not committed.
- `bash tools/run-sfe.sh <owner/name> <issue number>` runs the implementation loop on one issue of
  a project in a new SFE, and opens a PR for its work. `--rounds <number>` after the issue number
  sets the number of rounds for this run. `--factory <path>` before the repo mounts a checkout of
  this repo at `/factory` in place of the image's copy, to try a change before building an image.
  A change to the Python packages still needs a new image.
- `bash tools/test-in-sfe.sh` runs the tests that call Claude in an SFE, with this checkout
  mounted at `/factory`. `tools/check-code.sh` leaves those tests out.

`run-sfe.sh` gives the SFE two tokens. It reads the Claude Code token from the line
`FACTORY_CLAUDE_CODE_OAUTH_TOKEN=<token>` in `.env` at the repo's root, which git ignores, and
reads no other line of that file. Make the token with `claude setup-token`. Set `FACTORY_ENV_FILE`
to read another file, such as the `.env` of another checkout. The GitHub token comes from
`gh auth token`, so it's the GitHub CLI's login. The commits a run makes carry the git identity in
your git config.

## A project's settings

A project can set the number of rounds, each role's turn cap and the paths the doc check leaves
out in `software-factory.toml`, at the root of its repo. The `[settings]` table in `src/software_factory/factory.toml` lists each
setting and the factory's default for it. A run reads the file from the project's default branch,
and uses the default for each setting the file leaves out. For example:

```toml
rounds = 2

[turn_caps]
implementer = 60

[check_docs]
ignore = ["tests/fixtures/"]
```

## The factory plugin

The factory's standards, their templates and the doc check script are a Claude Code plugin, in
`plugin/`, with one skill, `software-factory:standards`. `.claude-plugin/marketplace.json` lists
the plugin, so a session on any machine can install it from this repo on GitHub. A run loads it
from `/factory/plugin` in the SFE.

A project asks for the plugin in its `.claude/settings.json`, so each person's session in the
project offers to install it:

```json
{
  "extraKnownMarketplaces": {
    "software-factory": {
      "source": { "source": "github", "repo": "nimbusscale/software-factory" }
    }
  },
  "enabledPlugins": { "software-factory@software-factory": true }
}
```

To install it by hand, run `/plugin install software-factory --marketplace
nimbusscale/software-factory` in Claude Code.
