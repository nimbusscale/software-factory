#!/usr/bin/env bash
# Builds the SFE's image from this checkout's commit, and tags it with its factory version and as
# latest. Run it from anywhere in the checkout: bash tools/build-sfe.sh
#
# It refuses a checkout with changes not committed, since the factory version names a commit.
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ -n "$(git status --porcelain)" ]]; then
  echo "The checkout has changes not committed. Commit them, or try them with run-sfe.sh --factory." >&2
  exit 1
fi

version="$(git rev-parse --short=12 HEAD)"
# The build gets the commit's files from git, so no file git doesn't track, such as .env, is in it.
git archive --format=tar HEAD \
  | docker build \
      --build-arg "FACTORY_VERSION=$version" \
      --build-arg "SFE_UID=$(id -u)" \
      --tag "software-factory-sfe:$version" \
      --tag software-factory-sfe:latest \
      -
echo "Built software-factory-sfe:$version"
