#!/usr/bin/env bash
# Builds template/, the scratch repo the spike reviews: one "base" commit, then a change not yet
# committed that plants two bugs, as a review copy holds them.
# Run it from the folder that holds spike.py: bash make-template.sh
set -euo pipefail

rm -rf template
mkdir template
cd template
git init -q -b main
git config user.email spike@example.invalid
git config user.name spike

cat > pages.py <<'EOF'
"""Split a list of items into pages."""


def page_count(total: int, per_page: int) -> int:
    """Return how many pages hold `total` items at `per_page` items a page."""
    return (total + per_page - 1) // per_page


def page(items: list[str], number: int, per_page: int) -> list[str]:
    """Return the items on page `number`, counting pages from 1."""
    start = (number - 1) * per_page
    return items[start : start + per_page]
EOF

cat > test_pages.py <<'EOF'
from pages import page, page_count


def test_page_count() -> None:
    assert page_count(10, 3) == 4


def test_first_page() -> None:
    assert page(list("abcdefg"), 1, 3) == ["a", "b", "c"]
EOF

git add .
git commit -q -m base

# The change under review. Bug 1: page() now starts one page late, though its docstring still
# says pages count from 1. Bug 2: the new last_page() then always returns an empty list.
cat > pages.py <<'EOF'
"""Split a list of items into pages."""


def page_count(total: int, per_page: int) -> int:
    """Return how many pages hold `total` items at `per_page` items a page."""
    return (total + per_page - 1) // per_page


def page(items: list[str], number: int, per_page: int) -> list[str]:
    """Return the items on page `number`, counting pages from 1."""
    start = number * per_page
    return items[start : start + per_page]


def last_page(items: list[str], per_page: int) -> list[str]:
    """Return the items on the last page."""
    return page(items, page_count(len(items), per_page), per_page)
EOF

git status --short
