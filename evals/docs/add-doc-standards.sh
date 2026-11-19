# Sourced by each case's place-files.sh, in the repo it builds, before its first commit. Adds what
# a project that follows the doc standards has: the standards in docs/standards, the doc check
# script in tools, and a CLAUDE.md whose doc map points to both.
# The standards and the script are copied from this repo as it is when the case runs, uncommitted
# changes included, whatever branch is checked out, so a case tests the ones you're working on.
factory=$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)
[[ -f $factory/docs/standards/README.md ]] || { echo "no doc standards at $factory/docs/standards" >&2; exit 1; }
[[ -f $factory/tools/check-docs.sh ]] || { echo "no doc check script at $factory/tools/check-docs.sh" >&2; exit 1; }
mkdir -p docs/standards tools
cp -R "$factory/docs/standards/." docs/standards/
cp "$factory/tools/check-docs.sh" tools/
# The test project's CLAUDE.md. plugin eval doesn't load it, so run-docs-evals.sh also copies it
# into each case's append_system_prompt. The file is here for an agent that reads it.
cp "$(dirname "${BASH_SOURCE[0]}")/project-claude.md" CLAUDE.md
