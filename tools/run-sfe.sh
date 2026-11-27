#!/usr/bin/env bash
# Starts a run in a new SFE (AD-12), or a review of one PR with --review (FR-47).
#
#   bash tools/run-sfe.sh [--factory PATH] [--image IMAGE] <owner/name> <issue number> [--rounds N]
#   bash tools/run-sfe.sh [--factory PATH] [--image IMAGE] --review <owner/name> <PR number>
#
# --factory mounts the checkout of the factory's repo at PATH at /factory, in place of the image's
# copy, to try a change before building an image. --image picks the image, which is
# software-factory-sfe:latest by default. --review runs the review command in place of the
# implementation loop's command. --entrypoint runs another command in the SFE, such as pytest.
# --env NAME passes the variable NAME from this command's environment into the SFE, when it's set.
# The other arguments go to the command the SFE runs.
#
# The Claude Code token comes from FACTORY_CLAUDE_CODE_OAUTH_TOKEN in the .env file at the repo's
# root, or in the file FACTORY_ENV_FILE names. The GitHub token comes from `gh auth token`.
# The name in .env isn't the CLAUDE_CODE_OAUTH_TOKEN that Claude Code reads, so a shell that sources
# .env never hands the token to an interactive Claude Code session.
#
# Each run gets a run folder, which holds its transcripts, the list of its roles, run.json with
# what the run used, and the --factory checkout's changes not committed (FR-39). It's made in the
# folder FACTORY_RUNS_FOLDER names in the same file, else in
# ${XDG_DATA_HOME:-~/.local/share}/software-factory/runs.
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
image=software-factory-sfe:latest
entrypoint=""
review=""
factory=""
version=""
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
    --review)
      review=1
      entrypoint=/opt/sfe/venv/bin/review
      docker_args+=(--entrypoint "$entrypoint")
      shift
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
# Docker refuses a mount whose path isn't absolute, with an error that doesn't name the setting.
if [[ "$runs_folder" != /* ]]; then
  echo "FACTORY_RUNS_FOLDER in $env_file is $runs_folder, which isn't a full path." \
    "Give one that starts with / or ~/." >&2
  exit 1
fi

# Claude Code in the SFE writes each file as its user, so the files would belong to someone else
# here, and could fail to be written, if the user IDs differed.
image_uid="$(docker image inspect --format '{{ index .Config.Labels "software-factory.sfe-uid" }}' "$image")"
if [[ "$image_uid" != "$(id -u)" ]]; then
  echo "The SFE's user in $image has user ID $image_uid, and yours is $(id -u)." \
    "Build the image as yourself with tools/build-sfe.sh." >&2
  exit 1
fi
if [[ -z "$version" ]]; then
  version="$(docker image inspect --format '{{ index .Config.Labels "software-factory.version" }}' "$image")"
fi

# The run folder's name says when the run started, which command the SFE ran when it isn't the
# implementation loop's, and what it ran on when the arguments name a repo and an issue or a PR.
read -r started_at run_name < <(date -u '+%Y-%m-%dT%H:%M:%SZ %Y%m%dT%H%M%SZ')
if [[ -n "$entrypoint" ]]; then
  run_name+="-$(basename "$entrypoint")"
fi
if [[ (-z "$entrypoint" || -n "$review") \
  && "${1:-}" =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ && "${2:-}" =~ ^[0-9]+$ ]]; then
  run_name+="-${1%%/*}-${1#*/}-$2"
fi
run_folder="$runs_folder/$run_name"
mkdir -p "$runs_folder"
# Without -p, so two runs started in the same second never share a folder. Only the owner can open
# it, since a transcript can hold a secret (FR-39).
mkdir --mode 700 "$run_folder"
mkdir "$run_folder/transcripts"
echo "The run folder is $run_folder" >&2
# Meets FR-44. Python, since it writes the arguments as JSON whatever they hold.
python3 -c '
import json, sys
started_at, version, image, entrypoint, *arguments = sys.argv[1:]
run = {
    "started_at": started_at,
    "factory_version": version,
    "image": image,
    "entrypoint": entrypoint or None,
    "arguments": arguments,
}
print(json.dumps(run, indent=2))
' "$started_at" "$version" "$image" "$entrypoint" "$@" > "$run_folder/run.json"
# Meets FR-45. Files git ignores, such as .env, are left out, since they aren't the factory's.
if [[ -n "$factory" ]]; then
  changes="$run_folder/factory-changes.diff"
  git -C "$factory" diff --binary HEAD > "$changes"
  while IFS= read -r -d '' path; do
    # git diff exits with 1 when the files differ, which they always do here.
    git -C "$factory" diff --binary --no-index /dev/null "$path" >> "$changes" || (($? == 1))
  done < <(git -C "$factory" ls-files --others --exclude-standard -z)
  if [[ ! -s "$changes" ]]; then
    rm "$changes"
  fi
fi
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
