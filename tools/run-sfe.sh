#!/usr/bin/env bash
# Starts a run in a new SFE (AD-12).
#
#   bash tools/run-sfe.sh [--factory PATH] [--image IMAGE] <owner/name> <issue number> [--rounds N]
#
# --factory mounts the checkout of the factory's repo at PATH at /factory, in place of the image's
# copy, to try a change before building an image. --image picks the image, which is
# software-factory-sfe:latest by default. --entrypoint runs another command in the SFE, such as
# pytest. The other arguments go to the implementation loop's command.
#
# The Claude Code token comes from FACTORY_CLAUDE_CODE_OAUTH_TOKEN in the .env file at the repo's
# root, or in the file FACTORY_ENV_FILE names. The GitHub token comes from `gh auth token`.
# The name in .env isn't the CLAUDE_CODE_OAUTH_TOKEN that Claude Code reads, so a shell that sources
# .env never hands the token to an interactive Claude Code session.
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
image=software-factory-sfe:latest
docker_args=()

while (($# > 0)); do
  case "$1" in
    --factory)
      factory="$(cd "$2" && pwd)"
      version="$(git -C "$factory" rev-parse --short=12 HEAD)-local"
      docker_args+=(--volume "$factory:/factory:ro" --env "FACTORY_VERSION=$version")
      shift 2
      ;;
    --image)
      image="$2"
      shift 2
      ;;
    --entrypoint)
      docker_args+=(--entrypoint "$2")
      shift 2
      ;;
    *)
      break
      ;;
  esac
done

# Read, not sourced, so no other line of the file runs or reaches this shell.
env_file="${FACTORY_ENV_FILE:-$repo_root/.env}"
claude_token="$(sed -n 's/^FACTORY_CLAUDE_CODE_OAUTH_TOKEN=//p' "$env_file" | tail -n 1)"
claude_token="${claude_token%\"}"
claude_token="${claude_token#\"}"
if [[ -z "$claude_token" ]]; then
  echo "$env_file has no FACTORY_CLAUDE_CODE_OAUTH_TOKEN." >&2
  exit 1
fi
github_token="$(gh auth token)"

# The commits the workflow makes carry the owner's git identity.
for part in name email; do
  if ! value="$(git config --get "user.$part")"; then
    echo "git has no user.$part set. Set it with: git config --global user.$part <$part>" >&2
    exit 1
  fi
  docker_args+=(--env "GIT_AUTHOR_${part^^}=$value" --env "GIT_COMMITTER_${part^^}=$value")
done

# --env with a name and no value takes the value from this command's environment, so neither token
# is on a command line, where other users of the machine could see it.
CLAUDE_CODE_OAUTH_TOKEN="$claude_token" GH_TOKEN="$github_token" exec docker run \
  --rm --init \
  --env CLAUDE_CODE_OAUTH_TOKEN \
  --env GH_TOKEN \
  "${docker_args[@]}" \
  "$image" \
  "$@"
