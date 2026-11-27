#!/usr/bin/env bash
# Starts a run in a new SFE (AD-12).
#
#   bash tools/run-sfe.sh [--factory PATH] [--image IMAGE] <owner/name> <issue number> [--rounds N]
#
# --factory mounts the checkout of the factory's repo at PATH at /factory, in place of the image's
# copy, to try a change before building an image. --image picks the image, which is
# software-factory-sfe:latest by default. --entrypoint runs another command in the SFE, such as
# pytest. --env NAME passes the variable NAME from this command's environment into the SFE, when
# it's set. The other arguments go to the implementation loop's command.
#
# The Claude Code token comes from FACTORY_CLAUDE_CODE_OAUTH_TOKEN in the .env file at the repo's
# root, or in the file FACTORY_ENV_FILE names. The GitHub token comes from `gh auth token`.
# The name in .env isn't the CLAUDE_CODE_OAUTH_TOKEN that Claude Code reads, so a shell that sources
# .env never hands the token to an interactive Claude Code session.
#
# Each run gets a run folder, which holds its transcripts and the list of its roles (FR-39, FR-40,
# FR-41). It's made in the folder FACTORY_RUNS_FOLDER names in the same file, else in
# ${XDG_DATA_HOME:-~/.local/share}/software-factory/runs.
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
image=software-factory-sfe:latest
entrypoint=""
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
      entrypoint="$2"
      docker_args+=(--entrypoint "$2")
      shift 2
      ;;
    --env)
      docker_args+=(--env "$2")
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

# The folder that holds the run folders is a setting of this machine, not of a project, so it's in
# .env. A project's software-factory.toml is read in the SFE, after the run folder has to exist.
runs_folder="$(sed -n 's/^FACTORY_RUNS_FOLDER=//p' "$env_file" | tail -n 1)"
runs_folder="${runs_folder%\"}"
runs_folder="${runs_folder#\"}"
if [[ "$runs_folder" == "~/"* ]]; then
  runs_folder="$HOME/${runs_folder#"~/"}"
fi
runs_folder="${runs_folder:-${XDG_DATA_HOME:-$HOME/.local/share}/software-factory/runs}"

# Claude Code in the SFE writes each file as its user, so the files would belong to someone else
# here, and could fail to be written, if the user IDs differed.
image_uid="$(docker image inspect --format '{{ index .Config.Labels "software-factory.sfe-uid" }}' "$image")"
if [[ "$image_uid" != "$(id -u)" ]]; then
  echo "The SFE's user in $image has user ID $image_uid, and yours is $(id -u)." \
    "Build the image as yourself with tools/build-sfe.sh." >&2
  exit 1
fi

# The run folder's name says when the run started, and what it ran on when the arguments name a
# repo and an issue.
run_name="$(date -u +%Y%m%dT%H%M%SZ)"
if [[ -n "$entrypoint" ]]; then
  run_name+="-$(basename "$entrypoint")"
elif [[ "${1:-}" =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ && "${2:-}" =~ ^[0-9]+$ ]]; then
  run_name+="-${1%%/*}-${1#*/}-$2"
fi
run_folder="$runs_folder/$run_name"
mkdir -p "$runs_folder"
# Without -p, so two runs started in the same second never share a folder.
mkdir "$run_folder" "$run_folder/transcripts"
echo "The run folder is $run_folder" >&2
# Claude Code writes each session's transcript under ~/.claude/projects as it goes, so mounting the
# run folder there keeps every step, even of a run that stops partway (FR-40). The SFE gets only
# this run's folder, so no role reads another run's transcripts (TR-21, TR-22).
docker_args+=(
  --volume "$run_folder:/home/sfe/run"
  --volume "$run_folder/transcripts:/home/sfe/.claude/projects"
  --env "FACTORY_RUN_FOLDER=$run_name"
)

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
