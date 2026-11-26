# Sourced by each case's place-files.sh, in the repo it builds, before its first commit. Adds the
# test project's CLAUDE.md, which says to load the doc standards from the factory plugin.
# plugin eval doesn't load a CLAUDE.md, so run-docs-evals.sh also copies this text into each case's
# append_system_prompt. The file is here for an agent that reads it.
cp "$(dirname "${BASH_SOURCE[0]}")/project-claude.md" CLAUDE.md
