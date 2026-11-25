#!/usr/bin/env python3
"""Checks a project's specs and blueprints against the rules in the doc standards.

Usage, from the repo root:

    python3 <this folder>/check_docs.py [--uncited] <docs folder> <base branch>

It needs git, and Python 3.10 or newer. A project with a settings file needs Python 3.11
or newer, the first Python that reads TOML without an extra package. It uses nothing
outside Python's standard library.

Docs are the specs and the blueprints. The specs are the .md files in the docs folder
with F-SEC or T-SEC headings. Blueprints are the .md files in <docs folder>/blueprints.
Source files are the other text files in the repo that git doesn't ignore, including
other docs such as CLAUDE.md and the skills in .claude/skills. Spec IDs cited in source
files are checked too. Neither takes in a path that `[check_docs] ignore` in the
project's software-factory.toml matches, if the project sets it. The patterns are
written like a .gitignore, and git matches them. The list is for files such as test
fixtures, whose IDs aren't the project's.

The history and copy checks look only at lines added since the base branch, uncommitted
ones included. A line someone kept on purpose is then never flagged again. The other
checks look at every doc.

A requirement that nothing cites is flagged only if something cited it on the base
branch. A requirement written before the code that meets it is normal, but one that lost
its last citation may have lost its code or its test. With --uncited, every requirement
that nothing cites is flagged instead, for a look at the docs and the code as a whole.

When a change adds an item to a section, or edits one in it, each citation of that
section from before the change is flagged. The citation now covers the item, and may not
fit it.

It writes no files, so it runs where nothing is writable, such as an eval sandbox.

Prints one line per thing it flags:  RULE|SIGNAL <file>:<line> <what>
RULE means a rule was broken. SIGNAL means only that something is worth a look.
It exits 0 whenever it ran. What happens to the findings is up to the project's workflow.
"""

import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

SETTINGS_FILE = "software-factory.toml"
TEMPLATES = Path(__file__).resolve().parent / "templates"

IDS = r"(?:FR|TR|AD|TD|CS)-[0-9]+"
SEC_IDS = r"[FT]-SEC-[0-9]+"
CITE = re.compile(rf"\b(?:{IDS}|{SEC_IDS})\b")
SHALL = re.compile(r"(?:^|[^A-Za-z])shall(?:[^A-Za-z]|$)")
CITES_REQ = re.compile(r"(?:^|[^A-Za-z])(?:FR|TR)-[0-9]+")
FENCE = re.compile(r"^[ \t>]*(?:```|~~~)")
BLANK = re.compile(r"^[ \t>]*$")
HEADING = re.compile(r"^(#+) ")
SPEC_HEADING = re.compile(rf"^#+ {SEC_IDS}", re.MULTILINE)
MONTHS = (
    "January|February|March|April|May|June|July|August|September|October|November"
    "|December"
)
DATE = re.compile(
    rf"\b20[0-9]{{2}}-[0-9]{{2}}-[0-9]{{2}}\b|\b(?:{MONTHS}) [0-9]{{1,2}}\b"
)
ISSUE = re.compile(r"(?:^|[^A-Za-z0-9&/])#[0-9]+\b")
MARKER = re.compile(
    r"(?<!\w)(?:settled|decided|drafted|assumption|for now|to come|in progress"
    r"|no longer|used to|the new)(?!\w)",
    re.IGNORECASE,
)
WAS_NOW = re.compile(r"(?<!\w)was\b.*\bnow(?!\w)", re.IGNORECASE)
RANGE = re.compile(rf"\b{IDS}(?: (?:to|through) | ?[-–—] ?)(?:{IDS}|[0-9]+)\b")
SRC_FILE = re.compile(r"\.(?:ts|tsx|js|mjs|cjs|py|sh|md|txt)$")
RUN_LENGTH = 8
MAX_TOKENS = 20000


class CheckError(Exception):
    pass


def git(*args: str) -> str:
    done = subprocess.run(
        ["git", *args], capture_output=True, text=True, errors="replace", check=False
    )
    if done.returncode != 0:
        raise CheckError(done.stderr.strip())
    return done.stdout


def git_paths(*args: str) -> list[str]:
    return [p for p in git(*args, "-z").split("\0") if p]


def split_lines(text: str) -> list[str]:
    """The file's lines, numbered from 1 as grep and awk number them."""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def read_lines(path: str) -> list[str]:
    return split_lines(Path(path).read_text(encoding="utf-8", errors="replace"))


def realpath(path: str) -> str:
    return os.path.realpath(path)


class Repo:
    """The files the checks look at, and what changed since the base."""

    def __init__(self, docs_dir: str, base_branch: str, ignore: list[str]) -> None:
        self.docs_dir = docs_dir
        try:
            self.base = git("merge-base", base_branch, "HEAD").strip()
        except CheckError as error:
            message = f"can't find the base branch {base_branch}: {error}"
            raise CheckError(message) from error
        self.blueprints_dir = realpath(f"{docs_dir}/blueprints")
        self.research_dir = realpath(f"{docs_dir}/research")
        self.ignored = self._ignored(ignore)
        self._added: dict[str, set[int]] = {}

        md_files = sorted(p for p in self._md_files() if p not in self.ignored)
        texts = {
            p: Path(p).read_text(encoding="utf-8", errors="replace") for p in md_files
        }
        self.fspec = [
            p for p in md_files if re.search(r"^#+ F-SEC-[0-9]+", texts[p], re.M)
        ]
        self.tspec = [
            p for p in md_files if re.search(r"^#+ T-SEC-[0-9]+", texts[p], re.M)
        ]
        self.specs = list(dict.fromkeys(self.fspec + self.tspec))
        self.docs = sorted(
            set(self.specs) | {p for p in md_files if self.is_blueprint(p)}
        )
        docs = set(self.docs)
        tree = git_paths("ls-files", "--cached", "--others", "--exclude-standard")
        self.src = sorted(
            p
            for p in set(tree)
            if self.is_src(p) and p not in docs and os.path.isfile(p)
        )

    def _ignored(self, patterns: list[str]) -> set[str]:
        """Every path in the working tree or the base that the ignore list matches."""
        if not patterns:
            return set()
        excludes = [f"--exclude={pattern}" for pattern in patterns]
        working = git_paths("ls-files", "--cached", "--others", "--ignored", *excludes)
        base = git_paths(
            "ls-files", "--cached", "--ignored", *excludes, f"--with-tree={self.base}"
        )
        return set(working) | set(base)

    def _md_files(self) -> list[str]:
        found = []
        for folder, _, names in os.walk(self.docs_dir):
            for name in names:
                path = f"{folder}/{name}"
                if (
                    name.endswith(".md")
                    and os.path.isfile(path)
                    and not os.path.islink(path)
                ):
                    found.append(path.removeprefix("./"))
        return found

    def is_src(self, path: str) -> bool:
        if not SRC_FILE.search(path) or path in self.ignored:
            return False
        return not path.startswith(".claude/") or bool(
            re.match(r"^\.claude/skills/.*\.md$", path)
        )

    def is_blueprint(self, path: str) -> bool:
        return realpath(path).startswith(self.blueprints_dir + "/")

    def added_lines(self, path: str) -> set[int]:
        """The line numbers in a file that were added since the base. Every line, for a
        new file."""
        if path not in self._added:
            self._added[path] = self._find_added(path)
        return self._added[path]

    def _find_added(self, path: str) -> set[int]:
        in_base = subprocess.run(
            ["git", "cat-file", "-e", f"{self.base}:{path}"],
            capture_output=True,
            check=False,
        )
        if in_base.returncode != 0:
            return set(range(1, len(read_lines(path)) + 1))
        added = set()
        # Without these, a user's diff.external or color.diff setting changes the
        # output, and no hunk is found.
        diff = git("diff", "--no-ext-diff", "--no-color", "-U0", self.base, "--", path)
        for line in diff.split("\n"):
            hunk = re.match(r"^@@ \S+ \+(\d+)(?:,(\d+))?", line)
            if hunk:
                start, count = int(hunk[1]), int(hunk[2] or 1)
                added.update(range(start, start + count))
        return added

    def base_files(self) -> dict[str, list[str]]:
        """Each source file in the base commit, by the same rules, with its lines."""
        paths = [
            p
            for p in git_paths("ls-tree", "-r", "--name-only", self.base)
            if self.is_src(p)
        ]
        request = "".join(f"{self.base}:{p}\n" for p in paths).encode()
        out = subprocess.run(
            ["git", "cat-file", "--batch"],
            input=request,
            capture_output=True,
            check=True,
        ).stdout
        files, at = {}, 0
        for path in paths:
            header_end = out.index(b"\n", at)
            header = out[at:header_end].split()
            at = header_end + 1
            if len(header) != 3:
                continue
            size = int(header[2])
            if header[1] == b"blob":
                text = out[at : at + size].decode("utf-8", errors="replace")
                files[path] = split_lines(text)
            at += size + 1
        return files


def prose(lines: list[str], *, skip_scenarios: bool = False) -> list[str]:
    """The lines with fenced code blocks and inline code blanked out, and with
    skip_scenarios, Scenario paragraphs too."""
    out, fence, scenario = [], False, False
    for line in lines:
        if FENCE.match(line):
            fence = not fence
            out.append("")
            continue
        if fence:
            out.append("")
            continue
        if BLANK.match(line):
            scenario = False
        if skip_scenarios and re.match(r"^[ \t>]*\*Scenario:\*", line):
            scenario = True
        out.append("" if scenario else re.sub(r"`[^`]*`", "", line))
    return out


def numbered(lines: list[str]) -> list[tuple[int, str]]:
    return list(enumerate(lines, start=1))


# --- History ------------------------------------------------------------------------


def history(repo: Repo) -> list[str]:
    """Only the specs are checked, since a blueprint can hold history."""
    out = []
    for f in repo.specs:
        text = [
            re.sub(r"\]\([^)]*\)", "]", line)
            for line in prose(read_lines(f), skip_scenarios=True)
        ]
        found = [
            (n, f"date: {m[0]}")
            for n, line in numbered(text)
            for m in DATE.finditer(line)
        ]
        found += [
            (n, f"issue or PR number: {m[0][m[0].index('#') :]}")
            for n, line in numbered(text)
            for m in ISSUE.finditer(line)
        ]
        found += [
            (n, f"marker word: {m[0]}")
            for n, line in numbered(text)
            for m in MARKER.finditer(line)
        ]
        found += [
            (n, '"was ... now"') for n, line in numbered(text) if WAS_NOW.search(line)
        ]
        added = repo.added_lines(f)
        out += [
            f"SIGNAL {f}:{n} may be history: {' '.join(what.split())}"
            for n, what in found
            if n in added
        ]
    return out


# --- References ---------------------------------------------------------------------


def definitions(repo: Repo) -> list[tuple[str, int, str]]:
    defs = []
    for f in repo.specs:
        lines = numbered(read_lines(f))
        defs += [
            (f, n, m[1])
            for n, line in lines
            if (m := re.match(rf"^\*\*({IDS})\.\*\*", line))
        ]
        defs += [
            (f, n, m[1])
            for n, line in lines
            if (m := re.match(rf"^#+ ({SEC_IDS})", line))
        ]
    return defs


def citations(files: dict[str, list[str]]) -> list[tuple[str, int, str]]:
    return [
        (f, n, m[0])
        for f, lines in files.items()
        for n, line in numbered(lines)
        for m in CITE.finditer(line)
    ]


def terms_lines(lines: list[str]) -> set[int]:
    """The line numbers inside a spec's Terms section. A section ends at the next
    heading of its level or higher."""
    inside, terms = set(), 0
    for n, line in numbered(lines):
        heading = HEADING.match(line)
        if heading:
            level = len(heading[1])
            if terms and level <= terms:
                terms = 0
            if re.match(rf"^#+ {SEC_IDS}\. Terms[ \t]*$", line):
                terms = level
                continue
        if terms:
            inside.add(n)
    return inside


def counts(
    terms: set[tuple[str, int]], cites: list[tuple[str, int, str]]
) -> Counter[str]:
    """How often each ID appears outside Terms sections. A citation from Terms doesn't
    count, since a term only explains a word, so the requirement may still be unbuilt."""
    return Counter(cite_id for f, n, cite_id in cites if (f, n) not in terms)


def references(repo: Repo, *, all_uncited: bool) -> list[str]:
    out = []
    defs = definitions(repo)
    defined = {d[2] for d in defs}

    seen: Counter[tuple[str, str]] = Counter()
    for f, n, def_id in defs:
        seen[f, def_id] += 1
        if seen[f, def_id] > 1:
            out.append(f"RULE {f}:{n} {def_id} is defined twice in this doc")
    for f, n, def_id in defs:
        if f in repo.fspec and re.match(r"^(TR|AD|TD|CS|T-SEC)", def_id):
            out.append(f"RULE {f}:{n} {def_id} belongs in the technical spec")
        elif f in repo.tspec and re.match(r"^(FR|F-SEC)", def_id):
            out.append(f"RULE {f}:{n} {def_id} belongs in the functional spec")

    all_files = {f: read_lines(f) for f in repo.docs + repo.src}
    cites = citations(all_files)
    out += [
        f"RULE {f}:{n} cites {cite_id}, which isn't defined"
        for f, n, cite_id in cites
        if cite_id not in defined
    ]

    terms = {(f, n) for f in repo.specs for n in terms_lines(all_files[f])}
    once = {cite_id for cite_id, k in counts(terms, cites).items() if k == 1}
    cited_before = set() if all_uncited else cited_on_base(repo)
    for f, n, def_id in defs:
        if not re.match(r"^(FR|TR)-", def_id) or def_id not in once:
            continue
        if all_uncited:
            out.append(
                f"SIGNAL {f}:{n} {def_id} isn't cited anywhere, so it may be unbuilt or untested"
            )
        elif def_id in cited_before:
            out.append(
                f"SIGNAL {f}:{n} {def_id} was cited on the base branch and isn't now, so it"
                " may be unbuilt or untested"
            )

    out += grown_sections(repo, defs, cites)
    out += [
        f"RULE {f}:{n} cites a range: {m[0]}"
        for f, lines in all_files.items()
        for n, line in numbered(lines)
        for m in RANGE.finditer(line)
    ]
    out += links(repo)
    return out


def cited_on_base(repo: Repo) -> set[str]:
    """Requirements cited on the base: the definition and at least one citation."""
    files = repo.base_files()
    specs = [f for f, lines in files.items() if SPEC_HEADING.search("\n".join(lines))]
    terms = {(f, n) for f in specs for n in terms_lines(files[f])}
    return {cite_id for cite_id, k in counts(terms, citations(files)).items() if k > 1}


def spec_items(f: str) -> list[tuple[str, int, int, list[str]]]:
    """Each item in a spec, as its ID, first line, last line and sections. An item is
    its own paragraph. Its sections are the one it's in and the ones around that."""
    items: list[tuple[str, int, int, list[str]]] = []
    sections: dict[int, str] = {}
    item_id, first, last = "", 0, 0

    def flush() -> None:
        nonlocal item_id
        if item_id:
            secs = [sections[level] for level in range(1, 10) if sections.get(level)]
            items.append((item_id, first, last, secs))
            item_id = ""

    fence = False
    for n, line in numbered(read_lines(f)):
        if FENCE.match(line):
            flush()
            fence = not fence
            continue
        if fence:
            continue
        heading = HEADING.match(line)
        if heading:
            flush()
            level = len(heading[1])
            for lower in range(level, 10):
                sections.pop(lower, None)
            sec = re.search(SEC_IDS, line)
            if sec and sec.start() == level + 1:
                sections[level] = sec[0]
            continue
        if BLANK.match(line):
            flush()
            continue
        start = re.match(rf"^[ \t>]*\*\*({IDS})\.\*\*", line)
        if start:
            flush()
            item_id, first = start[1], n
        last = n
    flush()
    return items


def grown_sections(
    repo: Repo, defs: list[tuple[str, int, str]], cites: list[tuple[str, int, str]]
) -> list[str]:
    """Older citations of a section that this change adds an item to, or edits an item
    in. A citation of a section means whatever the section holds now, so it may now
    cover an item it shouldn't. A citation on an added line is left out, since it was
    written against the section as it is now."""
    grown: dict[str, list[str]] = {}
    for f in repo.specs:
        added = repo.added_lines(f)
        for item_id, first, last, secs in spec_items(f):
            if any(first <= n <= last for n in added):
                for sec in secs:
                    grown.setdefault(sec, [])
                    if item_id not in grown[sec]:
                        grown[sec].append(item_id)
    if not grown:
        return []
    out = []
    def_set = set(defs)
    section_cites = sorted(
        {c for c in cites if re.fullmatch(SEC_IDS, c[2])}, key=cite_key
    )
    for f, n, sec in section_cites:
        changed = grown.get(sec)
        if not changed or (f, n, sec) in def_set or n in repo.added_lines(f):
            continue
        out.append(
            f"SIGNAL {f}:{n} cites {sec}, which this change adds to or edits:"
            f" {', '.join(changed)}. Check that the citation still fits"
        )
    return out


def cite_key(cite: tuple[str, int, str]) -> str:
    return f"{cite[0]}:{cite[1]}:{cite[2]}"


def links(repo: Repo) -> list[str]:
    out = []
    for f in repo.docs:
        for n, line in numbered(prose(read_lines(f))):
            for m in re.finditer(r"\]\([^)]+\)", line):
                target = m[0][2:-1].split("#", 1)[0].split(" ", 1)[0]
                if not target or re.match(r"^[a-z]+:", target):
                    continue
                # Joined as text, so a target that starts with / stays under the doc's folder.
                path = realpath(f"{os.path.dirname(f) or '.'}/{target}")
                if not os.path.exists(path):
                    out.append(f"RULE {f}:{n} links to {target}, which doesn't exist")
                if f in repo.fspec:
                    out.append(
                        f"RULE {f}:{n} the functional spec links out, to {target}"
                    )
                elif path.startswith(
                    repo.blueprints_dir + "/"
                ) and not repo.is_blueprint(f):
                    out.append(f"RULE {f}:{n} links to a blueprint, {target}")
    return out


# --- Item shape ---------------------------------------------------------------------


class ItemShape:
    """Checks the items in one spec, paragraph by paragraph."""

    def __init__(self, f: str) -> None:
        self.f = f
        self.out: list[str] = []
        self.why_id = ""
        self.why_line = 0
        self.td_id = ""
        self.td_line = 0
        self.td_ok = False
        self.req_id = ""
        self.req_body = ""

    def run(self) -> list[str]:
        para, start, fence = "", 0, False
        for n, line in numbered(read_lines(self.f)):
            if re.match(r"^[ \t]*(?:```|~~~)", line):
                fence = not fence
                para = self.flush(para, start)
                continue
            if fence:
                continue
            if BLANK.match(line):
                para = self.flush(para, start)
                continue
            text = re.sub(r"^[ \t>]+", "", line)
            if para:
                para = f"{para} {text}"
            else:
                para, start = text, n
        self.flush(para, start)
        self.check_td("")
        self.no_why()
        return self.out

    def flush(self, para: str, start: int) -> str:
        if para:
            self.check(para, start)
        return ""

    def no_why(self) -> None:
        if self.why_id:
            self.out.append(
                f"RULE {self.f}:{self.why_line} {self.why_id} has no Why line right after it"
            )
        self.why_id = ""

    def check_td(self, p: str) -> None:
        """A design decision cites the requirement it meets in its own line or its Why."""
        if not self.td_id:
            return
        if p.startswith("*Why:*") and CITES_REQ.search(p):
            self.td_ok = True
        if not self.td_ok:
            self.out.append(
                f"RULE {self.f}:{self.td_line} {self.td_id} cites no requirement, an FR or a"
                " TR, in its line or its Why"
            )
        self.td_id = ""

    def check(self, p: str, n: int) -> None:
        self.check_td(p)
        item = re.match(rf"^\*\*({IDS})\.\*\*", p)
        if item:
            self.check_item(item[1], p[item.end() + 1 :], n)
            return
        # Under a requirement, only labeled lines, and a table that the requirement text
        # points to. A "shall" paragraph is left to the no-ID check below, so one problem
        # gets one line.
        if p.startswith("#"):
            self.req_id = ""
        if self.req_id:
            if p.startswith("|"):
                if "table" not in self.req_body.lower():
                    self.out.append(
                        f"RULE {self.f}:{n} a table under {self.req_id}, whose text doesn't"
                        " point to it"
                    )
            elif not re.match(
                r"^\*(Why|Scenario|Accepted gap):\*", p
            ) and not SHALL.search(p):
                self.out.append(
                    f"RULE {self.f}:{n} a paragraph under {self.req_id} with no label, such as"
                    " Why or Scenario"
                )
        if p.startswith("*Why:*"):
            self.why_id = ""
            return
        self.no_why()
        if not re.match(r"^(#|\*[A-Z][a-z ]+:\*)", p) and SHALL.search(p):
            self.out.append(f'RULE {self.f}:{n} a "shall" sentence with no ID')

    def check_item(self, item_id: str, body: str, n: int) -> None:
        self.no_why()
        self.req_id = ""
        if item_id.startswith("TD"):
            self.td_id, self.td_line, self.td_ok = (
                item_id,
                n,
                bool(CITES_REQ.search(body)),
            )
        # A code standard gets a Why only when it needs one, as a requirement does.
        if item_id.startswith("CS"):
            return
        if item_id.startswith(("AD", "TD")):
            self.why_id, self.why_line = item_id, n
            return
        self.req_id, self.req_body = item_id, body
        f = self.f
        if not re.match(r"^(Where|While|When|The)[ ,]", body):
            self.out.append(
                f"RULE {f}:{n} {item_id} doesn't start with Where, While, When or The"
            )
        shalls = len(SHALL.findall(body))
        if shalls != 1:
            self.out.append(f'RULE {f}:{n} {item_id} has {shalls} "shall"s, not one')
        before = re.sub(r"[^a-z]shall[^a-z].*", "", body.lower(), count=1)
        order, last = "where while when", 0
        for word in re.split(r"[^a-z]+", before):
            if word in {"where", "while", "when"}:
                if order.index(word) + 1 <= last:
                    self.out.append(
                        f"RULE {f}:{n} {item_id} has Where, While and When out of order, or one"
                        " twice"
                    )
                    break
                last = order.index(word) + 1


# --- Blueprint status ---------------------------------------------------------------


def blueprint_status(f: str) -> list[str]:
    """A blueprint opens with front matter: a status, active or retired, and a retired
    date that's empty while it's active."""
    lines = read_lines(f)
    if lines and lines[0] != "---":
        return [f"RULE {f}:1 has no front matter with its status"]
    status, status_line, date, date_line = "", 0, None, 0
    for n, line in numbered(lines[1:]):
        if line == "---":
            break
        if line.startswith("status:"):
            status, status_line = (
                re.sub(r"^status:[ \t]*", "", line).rstrip(" \t"),
                n + 1,
            )
        if line.startswith("retired:"):
            date, date_line = re.sub(r"^retired:[ \t]*", "", line).rstrip(" \t"), n + 1
    else:
        return [f"RULE {f}:1 has front matter that isn't closed with ---"]
    out = []
    if status not in {"active", "retired"}:
        out.append(
            f'RULE {f}:{status_line or 1} has status "{status}", not active or retired'
        )
    if date is None:
        out.append(f"RULE {f}:1 has no retired line in its front matter")
    elif status == "active" and date:
        out.append(f"RULE {f}:{date_line} is active but has a retired date")
    elif status == "retired" and not re.fullmatch(
        r"20[0-9]{2}-[0-9]{2}-[0-9]{2}", date
    ):
        out.append(
            f"RULE {f}:{date_line} is retired but its retired date isn't a date like 2026-11-18"
        )
    return out


def is_retired(repo: Repo, f: str) -> bool:
    if not repo.is_blueprint(f):
        return False
    lines = read_lines(f)
    if not lines or lines[0] != "---":
        return False
    for line in lines[1:]:
        if line == "---":
            return False
        if re.match(r"^status:[ \t]*retired[ \t]*$", line):
            return True
    return False


# --- Copies -------------------------------------------------------------------------


def runs_of(f: str, added: set[int]) -> list[tuple[str, str, int, bool]]:
    """Every run of eight words in a file, with the line it starts on, and whether one
    of its words is on an added line."""
    words: list[tuple[str, int]] = []
    runs = []
    for n, line in numbered(read_lines(f)):
        lowered = line.translate(ASCII_LOWER)
        for word in re.sub(r"[^a-z0-9']+", " ", lowered).split():
            words.append((word, n))
            if len(words) >= RUN_LENGTH:
                window = words[-RUN_LENGTH:]
                run = " ".join(w for w, _ in window)
                runs.append(
                    (run, f, window[0][1], any(at in added for _, at in window))
                )
    return runs


ASCII_LOWER = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")


def copies(repo: Repo) -> list[str]:
    """For each pair of files sharing runs, where at least one is a doc and at least one
    copy of the run is on a line added since the base: how many, and the first. A copy
    someone kept on purpose is then never flagged again.

    Research docs in <docs folder>/research are left out. They're frozen records that no
    agent reads as a current rule, and specs are often written from them, so shared text
    there is expected. Retired blueprints are left out too. A retired blueprint is
    frozen, and the code was written from it. A template's text is meant to be in every
    doc made from it, so a run that's in a template is never flagged.
    """
    changed = set(git_paths("diff", "--name-only", "--no-renames", repo.base))
    changed |= set(git_paths("ls-files", "--others", "--exclude-standard"))
    template_runs = {
        run[0]
        for t in sorted(TEMPLATES.glob("*.md"))
        if t.is_file()
        for run in runs_of(str(t), set())
    }
    by_run: dict[str, list[tuple[str, int, bool]]] = {}
    for f in repo.docs + repo.src:
        if realpath(f).startswith(repo.research_dir + "/") or is_retired(repo, f):
            continue
        added = repo.added_lines(f) if f in changed else set()
        for run, _, line, new in runs_of(f, added):
            if run not in template_runs:
                by_run.setdefault(run, []).append((f, line, new))
    docs = set(repo.docs)
    count: Counter[tuple[str, str]] = Counter()
    first: dict[tuple[str, str], str] = {}
    for run in sorted(by_run):
        # The order sort gives the lines "<run> <file> <line> <new>", so the first pair
        # found is the same each time.
        entries = sorted(by_run[run], key=lambda e: (e[0], str(e[1]), e[2]))
        for a, line_a, new_a in entries:
            for b, line_b, new_b in entries:
                if a >= b or (a not in docs and b not in docs) or not (new_a or new_b):
                    continue
                first.setdefault((a, b), f'{a}:{line_a} and {b}:{line_b}: "{run}"')
                count[a, b] += 1
    return [f"SIGNAL {first[k]} ({count[k]} new shared 8-word runs)" for k in count]


# --- Running it ---------------------------------------------------------------------


def ignore_list() -> list[str]:
    """The patterns in `[check_docs] ignore` in the project's settings file."""
    if not os.path.isfile(SETTINGS_FILE):
        return []
    # Imported here, since Python 3.10 has no tomllib, and a project with no settings
    # file doesn't need it.
    try:
        import tomllib
    except ModuleNotFoundError as error:
        version = ".".join(str(part) for part in sys.version_info[:3])
        message = (
            f"reading {SETTINGS_FILE} needs Python 3.11 or newer, and this is {version}"
        )
        raise CheckError(message) from error
    try:
        settings = tomllib.loads(Path(SETTINGS_FILE).read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as error:
        message = f"{SETTINGS_FILE} isn't valid TOML: {error}"
        raise CheckError(message) from error
    table = settings.get("check_docs", {})
    patterns = table.get("ignore", []) if isinstance(table, dict) else None
    if not isinstance(patterns, list) or not all(isinstance(p, str) for p in patterns):
        message = f"[check_docs] ignore in {SETTINGS_FILE} isn't a list of strings"
        raise CheckError(message)
    return [p for p in patterns if p]


def check(docs_dir: str, base_branch: str, *, all_uncited: bool) -> list[str]:
    top = git("rev-parse", "--show-toplevel").strip()
    if realpath(top) != realpath(os.getcwd()):
        message = "check_docs.py runs from the repo root"
        raise CheckError(message)
    repo = Repo(docs_dir.rstrip("/") or "/", base_branch, ignore_list())
    out = history(repo)
    out += references(repo, all_uncited=all_uncited)
    for f in repo.specs:
        out += ItemShape(f).run()
    for f in repo.docs:
        if repo.is_blueprint(f):
            out += blueprint_status(f)
    out += sorted(copies(repo))
    for f in repo.docs:
        tokens = os.path.getsize(f) // 4
        if tokens > MAX_TOKENS:
            out.append(
                f"SIGNAL {f}:1 about {tokens} tokens, and the Read tool reads at most 25,000"
                " in one call"
            )
    return out


def main() -> int:
    args = sys.argv[1:]
    all_uncited = bool(args) and args[0] == "--uncited"
    if all_uncited:
        args = args[1:]
    usage = "usage: check_docs.py [--uncited] <docs folder> <base branch>, run from the repo root"
    if len(args) != 2 or not os.path.isdir(args[0]):
        print(usage, file=sys.stderr)
        return 2
    try:
        lines = check(args[0], args[1], all_uncited=all_uncited)
    except CheckError as error:
        print(f"check_docs.py: {error}", file=sys.stderr)
        return 2
    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
