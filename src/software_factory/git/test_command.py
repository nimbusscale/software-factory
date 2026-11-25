import asyncio
import base64
from typing import TYPE_CHECKING

import pytest

from software_factory.conftest import run_git
from software_factory.git.command import GitError, git

if TYPE_CHECKING:
    from pathlib import Path


def test_git_works_in_cwd_when_git_dir_points_elsewhere(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    run_git("init", "--quiet", str(tmp_path / "other"), cwd=tmp_path)
    run_git("init", "--quiet", str(tmp_path / "repo"), cwd=tmp_path)
    monkeypatch.setenv("GIT_DIR", str(tmp_path / "other" / ".git"))

    git_dir = run_git("rev-parse", "--absolute-git-dir", cwd=tmp_path / "repo")

    assert git_dir == str(tmp_path / "repo" / ".git")


def test_git_never_waits_for_a_username(tmp_path: Path) -> None:
    show = "alias.show-prompt=!printenv GIT_TERMINAL_PROMPT"

    assert run_git("-c", show, "show-prompt", cwd=tmp_path) == "0"


def test_git_gives_up_on_a_silent_server(tmp_path: Path) -> None:
    async def never_answer(
        reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        try:
            await reader.read()
        finally:
            writer.close()

    async def run() -> None:
        server = await asyncio.start_server(never_answer, "127.0.0.1", 0)
        port = server.sockets[0].getsockname()[1]
        url = f"http://127.0.0.1:{port}/dust-law.git"
        # Two seconds, not the code's 60, so the test runs quickly.
        fetch = git("-c", "http.lowSpeedTime=2", "ls-remote", url, cwd=tmp_path)
        try:
            with pytest.raises(GitError, match="too slow"):
                await asyncio.wait_for(fetch, 10)
        finally:
            server.close()

    asyncio.run(run())


GIT_LOGIN = "login-for-git"


def test_git_sends_the_token_when_the_remote_asks_for_one(tmp_path: Path) -> None:
    logins: list[str] = []

    async def ask_for_a_login(
        reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        request = (await reader.readuntil(b"\r\n\r\n")).decode()
        header = "authorization: "
        login = [
            line[len(header) :]
            for line in request.split("\r\n")
            if line.lower().startswith(header)
        ]
        logins.extend(login)
        status = "404 Not Found" if login else "401 Unauthorized"
        writer.write(
            f'HTTP/1.1 {status}\r\nWWW-Authenticate: Basic realm="git"\r\n'
            "Content-Length: 0\r\nConnection: close\r\n\r\n".encode()
        )
        await writer.drain()
        writer.close()

    async def run() -> None:
        server = await asyncio.start_server(ask_for_a_login, "127.0.0.1", 0)
        port = server.sockets[0].getsockname()[1]
        url = f"http://127.0.0.1:{port}/dust-law.git"
        try:
            with pytest.raises(GitError):
                await git("ls-remote", url, cwd=tmp_path, token=GIT_LOGIN)
        finally:
            server.close()

    asyncio.run(run())

    # AD-7.
    login = base64.b64encode(f"x-access-token:{GIT_LOGIN}".encode()).decode()
    assert logins == [f"Basic {login}"]


def test_git_runs_without_the_workflows_github_token(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("GH_TOKEN", "token-for-gh")
    monkeypatch.setenv("GITHUB_TOKEN", "token-for-gh")
    show = 'alias.show-tokens=!echo "[$GH_TOKEN$GITHUB_TOKEN]"'

    # AD-7.
    assert run_git("-c", show, "show-tokens", cwd=tmp_path) == "[]"
