"""Tests of tools/run-sfe.sh, with stand-ins for docker and gh on the PATH."""

import asyncio
import json
import os
import re
import shutil
from pathlib import Path

import pytest

from software_factory.conftest import commit_file, run_git

RUN_SFE = Path(__file__).parents[2] / "tools" / "run-sfe.sh"

IMAGE_VERSION = "0123456789ab"

# Hands back this user's ID as the image's, and IMAGE_VERSION as its factory version.
# Writes the arguments of `docker run` to the file DOCKER_ARGS names, one a line.
FAKE_DOCKER = f"""#!/usr/bin/env bash
if [[ "$1" == image && "$4" == *sfe-uid* ]]; then id -u; exit 0; fi
if [[ "$1" == image ]]; then echo {IMAGE_VERSION}; exit 0; fi
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
    asyncio.run(run_script(bash, [str(RUN_SFE), *args], environment, tmp_path))
    return docker_args.read_text().splitlines()


async def run_script(
    bash: str, args: list[str], environment: dict[str, str], cwd: Path
) -> None:
    process = await asyncio.create_subprocess_exec(
        bash,
        *args,
        env=environment,
        cwd=cwd,
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


def test_only_the_owner_can_open_the_run_folder(tmp_path: Path) -> None:
    run_sfe(tmp_path, "", "nimbusscale/dust-law", "1")

    folder = run_folder(tmp_path / "data" / "software-factory" / "runs")
    # FR-39.
    assert folder.stat().st_mode & 0o777 == 0o700


def test_runs_folder_that_isnt_a_full_path_is_refused(tmp_path: Path) -> None:
    with pytest.raises(AssertionError, match="isn't a full path"):
        run_sfe(tmp_path, "FACTORY_RUNS_FOLDER=runs\n", "nimbusscale/dust-law", "1")

    # Bug: a relative runs folder made a stray folder, and Docker then refused it.
    assert not (tmp_path / "runs").exists()


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


def test_records_the_factory_version_and_the_command(tmp_path: Path) -> None:
    run_sfe(tmp_path, "", "nimbusscale/dust-law", "1", "--rounds", "3")

    folder = run_folder(tmp_path / "data" / "software-factory" / "runs")
    run = json.loads((folder / "run.json").read_text())
    # FR-44.
    assert run["factory_version"] == IMAGE_VERSION
    assert run["arguments"] == ["nimbusscale/dust-law", "1", "--rounds", "3"]
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", run["started_at"])
    assert not (folder / "factory-changes.diff").exists()


def test_keeps_the_factory_checkouts_changes(tmp_path: Path) -> None:
    factory = tmp_path / "factory"
    factory.mkdir()
    run_git("init", "--quiet", cwd=factory)
    (factory / ".gitignore").write_text(".env\n")
    commit_file(factory, "README.md", "The factory.\n")
    (factory / "README.md").write_text("The factory, changed.\n")
    (factory / "new.py").write_text("print('new')\n")
    (factory / ".env").write_text("SECRET=1\n")

    run_sfe(tmp_path, "", "--factory", str(factory), "nimbusscale/dust-law", "1")

    folder = run_folder(tmp_path / "data" / "software-factory" / "runs")
    changes = (folder / "factory-changes.diff").read_text()
    # FR-45.
    assert "+The factory, changed." in changes
    assert "+print('new')" in changes
    assert "SECRET" not in changes
    # FR-44.
    commit = run_git("rev-parse", "--short=12", "HEAD", cwd=factory)
    assert json.loads((folder / "run.json").read_text())["factory_version"] == (
        f"{commit}-local"
    )


def test_review_runs_the_review_command(tmp_path: Path) -> None:
    docker_args = run_sfe(tmp_path, "", "--review", "nimbusscale/dust-law", "5")

    folder = run_folder(tmp_path / "data" / "software-factory" / "runs")
    # FR-47.
    entrypoint = docker_args.index("--entrypoint")
    assert docker_args[entrypoint + 1] == "/opt/sfe/venv/bin/review"
    assert docker_args[-2:] == ["nimbusscale/dust-law", "5"]
    # FR-39.
    assert re.fullmatch(r"\d{8}T\d{6}Z-review-nimbusscale-dust-law-5", folder.name)


def test_review_with_another_entrypoint_is_refused(tmp_path: Path) -> None:
    with pytest.raises(AssertionError, match="not both"):
        run_sfe(
            tmp_path,
            "",
            "--review",
            "--entrypoint",
            "pytest",
            "nimbusscale/dust-law",
            "5",
        )

    # Bug: --review with --entrypoint ran pytest in a run folder named for the PR.
    assert not (tmp_path / "data" / "software-factory" / "runs").exists()
