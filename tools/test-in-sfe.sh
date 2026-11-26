#!/usr/bin/env bash
# Runs the tests that call Claude in an SFE, with this checkout mounted at /factory. They need the
# image, which tools/build-sfe.sh builds.
#
#   bash tools/test-in-sfe.sh [pytest arguments]
#
# With no arguments it runs every test marked claude. run-sfe.sh says where the tokens come from.
# Set FACTORY_TEST_MODEL to run the roles in the tests of a whole run on that model, such as
# claude-haiku-5-5, in place of Opus.
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
if (($# == 0)); then
  set -- -m claude /factory/src
fi
# No cache, since /factory is read-only.
exec bash "$repo_root/tools/run-sfe.sh" --factory "$repo_root" --env FACTORY_TEST_MODEL \
  --entrypoint /opt/sfe/venv/bin/pytest \
  -p no:cacheprovider --rootdir /factory "$@"
