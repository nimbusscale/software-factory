# Sourced by each case's place-files.sh, in the repo it builds, before its first commit. Adds what
# a project that follows the doc standards has: the standards in docs/standards, with the doc check
# script in that folder, a settings file whose ignore list leaves them out of the doc check, and a
# CLAUDE.md whose doc map points to both.
# The standards are copied from the factory plugin in this repo as it is when the case runs,
# uncommitted changes included, whatever branch is checked out, so a case tests the ones you're
# working on.
factory=$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)
standards=$factory/plugin/skills/standards
[[ -f $standards/SKILL.md ]] || { echo "no doc standards at $standards" >&2; exit 1; }
[[ -f $standards/check_docs.py ]] || { echo "no doc check script at $standards/check_docs.py" >&2; exit 1; }
mkdir -p docs/standards
cp -R "$standards/." docs/standards/
rm -rf docs/standards/__pycache__
# The standards' example IDs aren't the test project's.
printf '[check_docs]\nignore = ["docs/standards/"]\n' > software-factory.toml
# The test project's CLAUDE.md. plugin eval doesn't load it, so run-docs-evals.sh also copies it
# into each case's append_system_prompt. The file is here for an agent that reads it.
cp "$(dirname "${BASH_SOURCE[0]}")/project-claude.md" CLAUDE.md
