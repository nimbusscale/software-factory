import asyncio
import json
import sys
from typing import TYPE_CHECKING

import pytest

from software_factory.github.api import (
    GitHubError,
    GraphQL,
    Reply,
    Repo,
    ask,
    gh_graphql,
)
from software_factory.github.fake_github import FakeGitHub

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

    from pydantic import JsonValue


class Count(Reply):
    total_count: int


class CountReply(Reply):
    count: Count


def test_repo_is_read_from_owner_and_name() -> None:
    assert Repo.parse("nimbusscale/dust-law") == Repo("nimbusscale", "dust-law")


@pytest.mark.parametrize("text", ["dust-law", "/dust-law", "nimbusscale/", "a/b/c"])
def test_repo_that_isnt_owner_and_name_is_refused(text: str) -> None:
    with pytest.raises(ValueError, match="Give it as owner/name"):
        Repo.parse(text)


def replying(data: JsonValue) -> GraphQL:
    async def fake(_query: str, _variables: Mapping[str, JsonValue]) -> JsonValue:
        return {"data": data}

    return fake


def test_reply_is_read_from_githubs_camel_case_names() -> None:
    github = replying({"count": {"totalCount": 3}})

    reply = asyncio.run(ask(github, "query Count { }", {}, CountReply))

    assert reply.count.total_count == 3


def test_reply_that_doesnt_fit_its_schema_ends_the_run() -> None:
    github = replying({"count": {"totalCount": "3"}})

    with pytest.raises(GitHubError, match="doesn't fit its schema"):
        asyncio.run(ask(github, "query Count { }", {}, CountReply))


def test_reply_with_no_data_ends_the_run() -> None:
    github = FakeGitHub(broken={"Count"})

    with pytest.raises(GitHubError, match="doesn't fit its schema"):
        asyncio.run(ask(github, "query Count { }", {}, CountReply))


def fake_gh(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, script: str) -> None:
    """Puts a gh on the PATH that runs `script`, a Python program."""
    folder = tmp_path / "bin"
    folder.mkdir()
    gh = folder / "gh"
    gh.write_text(f"#!{sys.executable}\n{script}")
    gh.chmod(0o755)
    monkeypatch.setenv("PATH", str(folder))


def test_gh_sends_the_query_and_variables(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    echo = (
        "import json, os, sys\n"
        "request = json.load(sys.stdin)\n"
        "prompt = os.environ['GH_PROMPT_DISABLED']\n"
        "print(json.dumps({'args': sys.argv[1:], 'request': request, 'p': prompt}))\n"
    )
    fake_gh(tmp_path, monkeypatch, echo)

    reply = asyncio.run(gh_graphql("query Count { }", {"number": 7}))

    assert reply == {
        "args": ["api", "graphql", "--input", "-"],
        "request": {"query": "query Count { }", "variables": {"number": 7}},
        "p": "1",
    }


def test_gh_that_fails_ends_the_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    errors = {"errors": [{"message": "Could not resolve to a Repository"}]}
    fail = (
        "import sys\n"
        f"print({json.dumps(errors)!r})\n"
        "print('gh: Could not resolve to a Repository', file=sys.stderr)\n"
        "sys.exit(1)\n"
    )
    fake_gh(tmp_path, monkeypatch, fail)

    with pytest.raises(GitHubError, match="failed: gh: Could not resolve"):
        asyncio.run(gh_graphql("query Count { }", {}))


def test_gh_reply_that_isnt_json_ends_the_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fake_gh(tmp_path, monkeypatch, "print('<html>')\n")

    with pytest.raises(GitHubError, match="isn't JSON"):
        asyncio.run(gh_graphql("query Count { }", {}))
