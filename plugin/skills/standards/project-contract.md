# Project contract

What a project's repo must hold for the software factory to run on it. When a run starts, the
factory checks the contract, and refuses the run when the project doesn't meet it.

## The specs

- The functional spec is at `docs/functional-spec.md`, and the technical spec at
  `docs/technical-spec.md`. Both must exist before a run. A spec made from its template in
  `templates/`, and still close to empty, is enough.
- Blueprints go in `docs/blueprints/`. A project can leave the folder out until it has a blueprint.

The paths are fixed, so a run and a person's own session find a project's docs the same way, with
nothing to look up first.

## The Makefile

A `Makefile` at the repo's root has two targets:

- `make setup` builds the project's environment in the folder it runs in, such as by installing the
  project's packages.
- `make check` runs the project's checks, such as its tests and its linter. It fails when one of
  them fails.

Neither target adds or changes a file that git doesn't ignore. Whatever `make setup` builds is
ignored, such as through `.gitignore`, and `make check` changes no file, such as by formatting the
code. A run commits every change in its copy of the repo, so such a file would be committed with
its work.

When a run starts, before it changes anything, the factory runs `make setup`, then `make check`, in
the run's copy of the repo. It refuses the run when either one fails, or adds or changes a file
that git doesn't ignore. Before each review, it also runs `make setup` in the quality reviewer's
copy, and ends the run when that fails.

Each target gets 10 minutes, and one that runs longer counts as failed. Every run waits for both
targets before any work starts, so a project whose targets take longer needs a faster setup or
check.

The targets get neither the GitHub token nor the Claude Code token in their environment.

## The settings file

A project sets any setting the factory offers in `software-factory.toml`, at the repo's root, such
as the number of rounds or the doc check's ignore list. A project that sets nothing needs no
settings file, and gets the factory's default for each setting. The factory refuses a run when a
setting isn't valid.

## What a run doesn't read

A project's CLAUDE.md and `.claude/` folder are for people working in the repo. A run never reads
them, so nothing in them changes how a run works.
