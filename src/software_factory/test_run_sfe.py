"""Tests of tools/run-sfe.sh, with stand-ins for docker and gh on the PATH."""

import asyncio
import os
import re
import shutil
from pathlib import Path

import pytest

RUN_SFE = Path(__file__).parents[2] / "tools" / "run-sfe.sh"

# Hands back this user's ID as the image's, and writes the arguments of `docker run`
# to the file DOCKER_ARGS names, one a line.
FAKE_DOCKER = """#!/usr/bin/env bash
if [[ "$1" == image ]]; then id -u; exit 0; fi
shift
printf '%s\\n' "$@" > "$DOCKER_ARGS"
"""


def run_sfe(tmp_path: Path, env_file_text: str, *args: str) -> list[str]:
    """Runs run-sfe.sh, and hands back the arguments it gave `docker run`."""
    bin_folder = tmp_path / "bin"
    bin_folder.mkdir()
    for name, script in {
        "docker": FAKE_DOCKER,
        "gh": "echo token-for-github\n",
    }.items():
        (bin_folder / name).write_text(script)
        (bin_folder / name).chmod(0o755)
    env_file = tmp_path / ".env"
    env_file.write_text("FACTORY_CLAUDE_CODE_OAUTH_TOKEN=token\n" + env_file_text)
    docker_args = tmp_path / "docker-args"
    environment = {
        **os.environ,
        "PATH": f"{bin_folder}:{os.environ['PATH']}",
        "FACTORY_ENV_FILE": str(env_file),
        "DOCKER_ARGS": str(docker_args),
        "XDG_DATA_HOME": str(tmp_path / "data"),
    }
    bash = shutil.which("bash")
    assert bash is not None
    asyncio.run(run_script(bash, [str(RUN_SFE), *args], environment))
    return docker_args.read_text().splitlines()


async def run_script(bash: str, args: list[str], environment: dict[str, str]) -> None:
    process = await asyncio.create_subprocess_exec(
        bash,
        *args,
        env=environment,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await process.communicate()
    assert process.returncode == 0, stderr.decode()


def run_folder(runs_folder: Path) -> Path:
    [folder] = runs_folder.iterdir()
    return folder


def test_makes_the_run_folder_in_the_folder_the_env_file_sets(tmp_path: Path) -> None:
    runs = tmp_path / "runs"

    docker_args = run_sfe(
        tmp_path, f"FACTORY_RUNS_FOLDER={runs}\n", "nimbusscale/dust-law", "1"
    )

    folder = run_folder(runs)
    # FR-39.
    assert re.fullmatch(r"\d{8}T\d{6}Z-nimbusscale-dust-law-1", folder.name)
    assert f"{folder}:/home/sfe/run" in docker_args
    assert f"FACTORY_RUN_FOLDER={folder.name}" in docker_args
    # FR-40.
    assert f"{folder}/transcripts:/home/sfe/.claude/projects" in docker_args


def test_makes_the_run_folder_in_the_default_folder(tmp_path: Path) -> None:
    run_sfe(tmp_path, "", "nimbusscale/dust-law", "1")

    # FR-39.
    folder = run_folder(tmp_path / "data" / "software-factory" / "runs")
    assert (folder / "transcripts").is_dir()


@pytest.mark.parametrize("setting", ['"~/sfe-runs"', "~/sfe-runs"])
def test_runs_folder_can_start_from_the_home_folder(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, setting: str
) -> None:
    monkeypatch.setenv("HOME", str(tmp_path / "home"))

    run_sfe(tmp_path, f"FACTORY_RUNS_FOLDER={setting}\n", "nimbusscale/dust-law", "1")

    # FR-39.
    assert run_folder(tmp_path / "home" / "sfe-runs").is_dir()
